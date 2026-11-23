#!/usr/bin/env python3
"""Render a 9:16 cutout-reveal shot for Shorts from a JSON spec.

The look measured on the reference channel:
  * players cut out of their photo, placed over a blurred/darkened background
  * the lead player enters first (rises from below while scaling up), the others
    follow one by one, sliding in from the sides BEHIND the lead
  * the whole composite keeps pushing in slowly so the frame is never still
  * optional mystery hook: lead starts as a dark silhouette, a lens glint reveals him
  * optional warm light-leak flash, optional big text pop ("+1ST ROUND PICKS")

Usage:
  python shorts_reveal.py spec.json out.mp4
  python shorts_reveal.py --example > spec.json     # print a starter spec

Spec keys (all positions are fractions of the 1080x1920 frame):
  dur, fps                     length in seconds, frame rate (30 default)
  bg: {src, blur, dark, zoom:[from,to], pan:[dx,dy]}
                               src = image or video; blur px; dark = brightness 0..1
  layers: list, drawn in the order given (first = furthest back). Each:
      src     cutout PNG with alpha (scripts/shorts_cutout.py)
      x       horizontal centre of the cutout (0.5 = middle)
      bottom  where the cutout's bottom edge sits (1.0 = frame bottom, can be >1)
      h       cutout height as a fraction of the frame height
      in      second the layer starts entering
      anim    rise | slide_left | slide_right | pop | fade | none
      len     entry duration (0.45 default)
      flip    true to mirror (make the player face the centre)
  silhouette: {layer, until, glint:true}   index (or list of indexes) into layers; reveal time
  flash: [{at, dur, color:"#ffb347"}]      additive light leak
  text:  [{t, in, y, size, color}]         big text pop (title font)
  push: 0.05                               total slow push-in over the shot
  shadow: true                             soft dark halo behind each cutout
"""
import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shorts_common import (H, TITLE_FONTS, W, clamp01, ease_in_out, ease_out,  # noqa: E402
                           ease_out_back, font, open_writer, read_video_frames)

EXAMPLE = {
    "dur": 4.0, "fps": 30,
    "bg": {"src": "bg_arena.jpg", "blur": 28, "dark": 0.45, "zoom": [1.0, 1.08], "pan": [0.0, -0.02]},
    "layers": [
        {"src": "jaylen.png", "x": 0.20, "bottom": 1.02, "h": 0.55, "in": 0.9, "anim": "slide_left"},
        {"src": "giannis.png", "x": 0.82, "bottom": 1.02, "h": 0.57, "in": 1.5, "anim": "slide_right", "flip": True},
        {"src": "lebron.png", "x": 0.50, "bottom": 1.04, "h": 0.66, "in": 0.0, "anim": "rise"},
    ],
    "silhouette": None,
    "flash": [{"at": 2.4, "dur": 0.5}],
    "text": [{"t": "+1ST ROUND\nPICKS", "in": 2.6, "y": 0.14, "size": 120}],
    "push": 0.05, "shadow": True,
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load_bg(spec, n, fps):
    """Return a function frame_index -> RGB Image (already blurred/darkened, not yet zoomed)."""
    src = spec["src"]
    blur, dark = spec.get("blur", 28), spec.get("dark", 0.45)

    def treat(im):
        if blur:
            im = im.filter(ImageFilter.GaussianBlur(blur))
        return ImageEnhance.Brightness(im).enhance(dark)

    if os.path.splitext(src)[1].lower() in (".mp4", ".mov", ".mkv", ".webm"):
        frames = []
        for b in read_video_frames(src, fps):
            frames.append(treat(Image.frombytes("RGB", (W, H), b)))
            if len(frames) >= n:
                break
        if not frames:
            raise SystemExit(f"could not read {src}")
        return lambda i: frames[min(i, len(frames) - 1)]
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height) * 1.15  # headroom for zoom/pan
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    still = treat(im.crop((l, t, l + W, t + H)))
    return lambda i: still


def zoom_pan(im, z, dx, dy):
    """Scale about the centre by z and shift by (dx, dy) fractions; output W x H."""
    if abs(z - 1) < 1e-4 and not dx and not dy:
        return im
    w, h = W / z, H / z
    cx, cy = W / 2 - dx * W, H / 2 - dy * H
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return im.transform((W, H), Image.EXTENT, box, Image.BICUBIC)


def prep_layer(L):
    im = Image.open(L["src"]).convert("RGBA")
    bb = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if bb:
        im = im.crop(bb)
    if L.get("flip"):
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    th = int(H * L.get("h", 0.6))
    im = im.resize((max(1, int(im.width * th / im.height)), th), Image.LANCZOS)
    L["_img"] = im
    # pad before blurring, otherwise the blur is clipped at the cutout's bounding box and
    # leaves a faint rectangle wherever the player touches the crop edge
    P = 60
    a = Image.new("L", (im.width + 2 * P, im.height + 2 * P), 0)
    a.paste(im.getchannel("A"), (P, P))
    a = a.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.65))
    L["_shadow"] = Image.merge("RGBA", [Image.new("L", a.size, 0)] * 3 + [a])
    L["_pad"] = P
    return L


def paste_rgba(dst, im, x, y):
    """alpha_composite that tolerates negative / off-frame offsets."""
    sx, sy = max(0, -x), max(0, -y)
    if sx >= im.width or sy >= im.height:
        return
    if sx or sy:
        im = im.crop((sx, sy, im.width, im.height))
    dst.alpha_composite(im, (max(0, x), max(0, y)))


def layer_state(L, t):
    """Return (scale, dx_px, dy_px, alpha) for a layer at time t."""
    t0, ln, anim = L.get("in", 0.0), L.get("len", 0.45), L.get("anim", "rise")
    if t < t0:
        return None
    p = (t - t0) / ln
    e = ease_out(p)
    if anim == "rise":
        return 0.86 + 0.14 * e, 0, (1 - e) * 0.22 * H, clamp01(p * 3)
    if anim == "slide_left":
        return 1.0, -(1 - e) * 0.65 * W, 0, clamp01(p * 2.5)
    if anim == "slide_right":
        return 1.0, (1 - e) * 0.65 * W, 0, clamp01(p * 2.5)
    if anim == "pop":
        return 0.55 + 0.45 * ease_out_back(p), 0, 0, clamp01(p * 4)
    if anim == "fade":
        return 1.0, 0, 0, clamp01(p)
    return 1.0, 0, 0, 1.0


def silhouette(im, amount):
    """Darken RGB toward a near-black silhouette, keep alpha. amount 1 = full silhouette."""
    if amount <= 0:
        return im
    dark = ImageEnhance.Brightness(im).enhance(0.06)
    dark.putalpha(im.getchannel("A"))
    return Image.blend(im, dark, clamp01(amount))


def radial(size, color, strength):
    import numpy as np
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    # elliptical, zero at the rim, cubic falloff (PIL's radial_gradient is not zero at the edge)
    mask = Image.fromarray((np.clip(1 - r, 0, 1) ** 3 * 255 * strength).astype("uint8"), "L")
    return Image.merge("RGB", [Image.new("L", (w, h), c) for c in color]), mask


def glint(frame, cx, cy, amt):
    """Lens-flare style star glint, additive."""
    if amt <= 0:
        return frame
    r = int(260 * (0.6 + 0.4 * amt))
    layer = Image.new("RGB", (W, H), 0)
    col, m = radial((2 * r, 2 * r), (255, 255, 255), amt)
    layer.paste(col, (int(cx - r), int(cy - r)), m)
    d = ImageDraw.Draw(layer)
    for ang, ln in ((0, 3.2), (90, 1.6)):
        dx, dy = math.cos(math.radians(ang)) * r * ln, math.sin(math.radians(ang)) * r * ln
        d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=tuple(int(255 * amt * 0.8) for _ in range(3)), width=5)
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    return ImageChops.add(frame, layer)


def leak(frame, t, fl):
    at, dur = fl["at"], fl.get("dur", 0.5)
    if not (at <= t <= at + dur):
        return frame
    p = (t - at) / dur
    s = math.sin(math.pi * p)  # 0 -> 1 -> 0
    col, m = radial((int(W * 1.6), int(H * 1.2)), hex_rgb(fl.get("color", "#ffb347")), s)
    layer = Image.new("RGB", (W, H), 0)
    layer.paste(col, (int(W * (0.1 + 0.4 * p)) - col.width // 2, -int(H * 0.1)), m)
    return ImageChops.add(frame, layer)


def draw_text(frame, T, t):
    if t < T.get("in", 0):
        return frame
    p = (t - T["in"]) / 0.3
    sc = 0.6 + 0.4 * ease_out_back(p)
    f = font(TITLE_FONTS, int(T.get("size", 110) * sc))
    lines = T["t"].upper().split("\n")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = int(H * T.get("y", 0.14))
    for ln in lines:
        d.text((W // 2 + 4, y + 6), ln, font=f, fill=(0, 0, 0, 160), anchor="mt")
        d.text((W // 2, y), ln, font=f, fill=hex_rgb(T.get("color", "#ffffff")) + (255,), anchor="mt")
        y += int(f.size * 1.02)
    if p < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * clamp01(p * 3))))
    frame = frame.convert("RGBA")
    frame.alpha_composite(layer)
    return frame.convert("RGB")


def render(spec, out):
    fps, dur = spec.get("fps", 30), spec["dur"]
    n = int(round(dur * fps))
    bgs = spec["bg"]
    bg_at = load_bg(bgs, n, fps)
    z0, z1 = bgs.get("zoom", [1.0, 1.08])
    pdx, pdy = bgs.get("pan", [0.0, 0.0])
    layers = [prep_layer(dict(L)) for L in spec.get("layers", [])]
    sil = spec.get("silhouette") or {}
    push = spec.get("push", 0.05)
    w = open_writer(out, fps)
    for i in range(n):
        t = i / fps
        u = i / max(1, n - 1)
        frame = zoom_pan(bg_at(i), z0 + (z1 - z0) * ease_in_out(u), pdx * u, pdy * u).convert("RGBA")
        comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for k, L in enumerate(layers):
            st = layer_state(L, t)
            if st is None:
                continue
            sc, dx, dy, a = st
            im = L["_img"]
            if sil and k in (sil["layer"] if isinstance(sil.get("layer"), list) else [sil.get("layer")]):
                until = sil.get("until", 1.5)
                im = silhouette(im, 1 - clamp01((t - until) / 0.35))
            if sc != 1:
                im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
            x = int(W * L.get("x", 0.5) - im.width / 2 + dx)
            y = int(H * L.get("bottom", 1.0) - im.height + dy)
            if a < 1:
                im = im.copy()
                im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
            if x >= W or x + im.width <= 0 or y >= H:
                continue
            if spec.get("shadow", True):
                sh, pad = L["_shadow"], L["_pad"]
                if sc != 1:
                    sh = sh.resize((max(1, int(sh.width * sc)), max(1, int(sh.height * sc))))
                    pad = int(pad * sc)
                if a < 1:
                    sh = sh.copy()
                    sh.putalpha(sh.getchannel("A").point(lambda v: int(v * a)))
                paste_rgba(comp, sh, x + 10 - pad, y + 14 - pad)
            paste_rgba(comp, im, x, y)
        # whole composite pushes in slowly; background has its own zoom
        comp = zoom_pan(comp, 1 + push * ease_in_out(u), 0, 0)
        frame.alpha_composite(comp)
        frame = frame.convert("RGB")
        if sil and sil.get("glint", True):
            until = sil.get("until", 1.5)
            g = 1 - abs(t - until) / 0.25
            if g > 0:
                frame = glint(frame, W * 0.30, H * 0.12, g)
        for fl in spec.get("flash", []):
            frame = leak(frame, t, fl)
        for T in spec.get("text", []):
            frame = draw_text(frame, T, t)
        w.stdin.write(frame.tobytes())
    w.stdin.close()
    w.wait()
    print(f"wrote {out}  ({n} frames, {dur}s @ {fps}fps)")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2))
    elif len(sys.argv) == 3:
        render(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
