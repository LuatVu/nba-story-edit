#!/usr/bin/env python3
"""Turn On Hoops — Facebook meme/news post renderer (1 image, 1200x1200 by default).

    python fb_post.py spec.json post.jpg
    python fb_post.py --example            # print an example spec

Spec:
{
  "size": [1200, 1200],
  "layout": "stack2" | "single" | "side2" | "strip3_big" | "big_strip3" | "grid4" | "custom",
  "boxes": [[x0,y0,x1,y1], ...],          # only for layout "custom", fractions of the canvas
  "panels": [
    {"image": "photo.jpg",                 # real photo, meme template, face-swapped meme, screenshot
     "fit": "cover" | "contain",           # contain = sharp image on blurred fill (portrait / meme / low-res)
     "focus": [0.5, 0.3], "zoom": 1.0,     # cover only: point kept in frame
     "crop": [l, t, r, b],                 # optional fractional pre-crop
     "text": "LINE ONE **YELLOW WORDS**\\nLINE TWO",   # caption at the bottom of this panel (optional)
     "text_size": 64,
     "labels": [{"text": "DEFENSE", "x": 0.75, "y": 0.25, "size": 54, "color": "white"}]
    }
  ],
  "text": "optional caption over the bottom of the whole image (single / side2 / strip layouts)"
}
Text between ** ** is brand yellow; everything is drawn UPPERCASE with black outline + shadow.
Brand: yellow #FFC21A glow frame, navy #0C1B3A footer with FB + YouTube handles,
Turn On Hoops logo top-right. Fonts: Barlow Condensed ExtraBold (captions), Montserrat ExtraBold (footer).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(SKILL, "assets", "channel_logo_turn_on_hoops.png")
FONT_HEAD = os.path.join(SKILL, "assets", "fonts", "BarlowCondensed-ExtraBold.ttf")
FONT_FOOT = os.path.join(SKILL, "assets", "fonts", "Montserrat-ExtraBold.ttf")

YELLOW = (255, 194, 26)
NAVY = (12, 27, 58)
WHITE = (255, 255, 255)
COLORS = {"white": WHITE, "yellow": YELLOW, "black": (0, 0, 0), "red": (235, 50, 50)}
FB_URL = "facebook.com/turnonhoops"
YT_URL = "youtube.com/@turnonhoops"
FOOT_H = 96

LAYOUTS = {
    "single": [(0, 0, 1, 1)],
    "stack2": [(0, 0, 1, .5), (0, .5, 1, 1)],
    "side2": [(0, 0, .5, 1), (.5, 0, 1, 1)],
    "strip3_big": [(0, 0, 1/3, .5), (1/3, 0, 2/3, .5), (2/3, 0, 1, .5), (0, .5, 1, 1)],
    "big_strip3": [(0, 0, 1, .5), (0, .5, 1/3, 1), (1/3, .5, 2/3, 1), (2/3, .5, 1, 1)],
    "grid4": [(0, 0, .5, .5), (.5, 0, 1, .5), (0, .5, .5, 1), (.5, .5, 1, 1)],
}

EXAMPLE = {
    "size": [1200, 1200], "layout": "stack2",
    "panels": [
        {"image": "curry.jpg", "focus": [0.46, 0.36],
         "text": "STEPH CURRY HAS NOW MADE **4,000+ THREE-POINTERS**\nTHE MOST IN NBA HISTORY"},
        {"image": "shaq.jpg", "fit": "contain", "crop": [0, 0, 1, 0.62],
         "text": "SHAQ, WITH **EXACTLY 1 CAREER THREE**, PROBABLY:\n**\"WE'RE BASICALLY THE SAME SHOOTER\"**"}]}


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("impact.ttf", size)


def cover(img, w, h, focus=(0.5, 0.5), zoom=1.0):
    s = max(w / img.width, h / img.height) * zoom
    img = img.resize((max(w, round(img.width * s)), max(h, round(img.height * s))), Image.LANCZOS)
    cx, cy = focus[0] * img.width, focus[1] * img.height
    x = min(max(cx - w / 2, 0), img.width - w)
    y = min(max(cy - h / 2, 0), img.height - h)
    return img.crop((round(x), round(y), round(x) + w, round(y) + h))


def panel_image(p, pw, ph):
    src = Image.open(p["image"]).convert("RGB")
    if "crop" in p:
        l, t, r, b = p["crop"]
        src = src.crop((int(l * src.width), int(t * src.height), int(r * src.width), int(b * src.height)))
    if p.get("fit") == "contain":
        img = cover(src, pw, ph).filter(ImageFilter.GaussianBlur(28))
        img = Image.blend(img, Image.new("RGB", img.size, (0, 0, 0)), 0.35)
        s = min(pw / src.width, ph / src.height)
        fg = src.resize((max(1, round(src.width * s)), max(1, round(src.height * s))), Image.LANCZOS)
        img.paste(fg, (round(pw * p.get("x", 0.5) - fg.width / 2), round((ph - fg.height) * p.get("y", 1.0))))
        return img
    return cover(src, pw, ph, p.get("focus", (0.5, 0.5)), p.get("zoom", 1.0))


def bottom_shade(panel, frac=0.5, strength=230):
    w, h = panel.size
    g = Image.new("L", (1, h), 0)
    start = int(h * (1 - frac))
    for y in range(start, h):
        g.putpixel((0, y), int(strength * ((y - start) / max(1, h - start)) ** 1.4))
    return Image.composite(Image.new("RGB", (w, h)), panel, g.resize((w, h)))


def runs(line):
    return [(p, i % 2 == 1) for i, p in enumerate(line.split("**")) if p]


def strip_emoji(s):
    """The caption font has no emoji glyphs (they render as boxes): emoji belong in the post caption only."""
    return "".join(c for c in s if ord(c) < 0x2190 or 0x2E80 <= ord(c) < 0x1F000 and not 0x2600 <= ord(c) < 0x2800)


def draw_text_block(canvas, box, text, max_size=64, min_size=30, anchor="bottom", color=WHITE):
    x0, y0, x1, y1 = box
    lines = [l.strip() for l in strip_emoji(text).upper().split("\n") if l.strip()]
    maxw = (x1 - x0) - 40
    size = max_size
    while size > min_size:
        f = font(FONT_HEAD, size)
        if all(f.getlength("".join(t for t, _ in runs(l))) <= maxw for l in lines):
            break
        size -= 2
    f = font(FONT_HEAD, size)
    lh = int(size * 1.08)
    y = (y1 - lh * len(lines)) if anchor == "bottom" else (y0 + y1 - lh * len(lines)) / 2
    stroke = max(3, size // 14)
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    placed = []
    for l in lines:
        rr = runs(l)
        x = (x0 + x1) / 2 - sum(f.getlength(t) for t, _ in rr) / 2
        for t, hi in rr:
            placed.append((x, y, t, hi))
            sd.text((x + 4, y + 5), t, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
            x += f.getlength(t)
        y += lh
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4)))
    d = ImageDraw.Draw(canvas)
    for x, y, t, hi in placed:
        d.text((x, y), t, font=f, fill=YELLOW if hi else color, stroke_width=stroke, stroke_fill=(0, 0, 0))


def glow_frame(canvas, inset=22, radius=34):
    W, H = canvas.size
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle((inset, inset, W - inset, H - inset), radius, outline=YELLOW + (255,), width=10)
    glow = layer.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(glow)
    canvas.alpha_composite(glow)
    ImageDraw.Draw(canvas).rounded_rectangle((inset, inset, W - inset, H - inset), radius, outline=(255, 240, 200, 255), width=3)


def chevrons(canvas, x, y, up=True, n=2, s=16):
    d = ImageDraw.Draw(canvas)
    for i in range(n):
        yy = y + i * s * 0.8
        pts = [(x - s, yy + s / 2), (x, yy - s / 2), (x + s, yy + s / 2)] if up else \
              [(x - s, yy - s / 2), (x, yy + s / 2), (x + s, yy - s / 2)]
        d.line(pts, fill=YELLOW + (255,), width=5, joint="curve")


def icon(kind, size):
    w = size if kind == "fb" else int(size * 1.3)
    im = Image.new("RGBA", (w, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, size - 1), size // 4, fill=YELLOW)
    if kind == "fb":
        d.text((size * 0.56, size * 0.56), "f", font=font(FONT_FOOT, int(size * 0.8)), fill=NAVY, anchor="mm")
    else:
        cx, cy = w / 2 + 2, size / 2
        d.polygon([(cx - size * .18, cy - size * .24), (cx - size * .18, cy + size * .24), (cx + size * .24, cy)], fill=NAVY)
    return im


def footer(canvas):
    W, H = canvas.size
    g = Image.new("L", (1, FOOT_H))
    for y in range(FOOT_H):
        g.putpixel((0, y), int(235 * min(1, y / (FOOT_H * 0.45))))
    bar = Image.new("RGBA", (W, FOOT_H), NAVY + (255,))
    bar.putalpha(g.resize((W, FOOT_H)))
    canvas.alpha_composite(bar, (0, H - FOOT_H))
    d = ImageDraw.Draw(canvas)
    f = font(FONT_FOOT, int(26 * W / 1200))
    cy, isz = H - 44, 40
    for kind, url, x in (("fb", FB_URL, 70), ("yt", YT_URL, W // 2 + 30)):
        ic = icon(kind, isz)
        canvas.alpha_composite(ic, (x, cy - isz // 2))
        d.text((x + ic.width + 16, cy), url, font=f, fill=WHITE, anchor="lm")


def logo(canvas, size=150, margin=40):
    W, _ = canvas.size
    lg = Image.open(LOGO).convert("RGBA").resize((size, size), Image.LANCZOS)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((W - margin - size - 12, margin + 6, W - margin + 4, margin + size + 22), fill=(0, 0, 0, 160))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ring = Image.new("RGBA", (size + 16, size + 16), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, size + 15, size + 15), fill=NAVY + (255,))
    canvas.alpha_composite(ring, (W - margin - size - 16, margin))
    canvas.alpha_composite(lg, (W - margin - size - 8, margin + 8))


def render(spec, out):
    W, H = spec.get("size", [1200, 1200])
    layout = spec.get("layout", "stack2")
    fr = spec["boxes"] if layout == "custom" else LAYOUTS[layout]
    boxes = [(round(a * W), round(b * H), round(c * W), round(d * H)) for a, b, c, d in fr]
    panels = spec["panels"]
    if len(panels) != len(boxes):
        raise SystemExit(f"layout {layout} needs {len(boxes)} panels, spec has {len(panels)}")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    for p, (x0, y0, x1, y1) in zip(panels, boxes):
        img = panel_image(p, x1 - x0, y1 - y0)
        if p.get("text") or (spec.get("text") and y1 >= H - 2):
            img = bottom_shade(img, 0.5)
        canvas.paste(img, (x0, y0))
    d = ImageDraw.Draw(canvas)
    for x0, y0, x1, y1 in boxes:  # yellow dividers between panels
        if x0 > 0: d.rectangle((x0 - 3, y0, x0 + 3, y1), fill=YELLOW)
        if y0 > 0: d.rectangle((x0, y0 - 3, x1, y0 + 3), fill=YELLOW)
    for p, (x0, y0, x1, y1) in zip(panels, boxes):
        bottom = y1 - (FOOT_H + 14 if y1 >= H - 2 else 26)
        small = (x1 - x0) < W * 0.6
        if p.get("text"):
            draw_text_block(canvas, (x0 + 20, y0, x1 - 20, bottom), p["text"],
                            p.get("text_size", 44 if small else 64), 26 if small else 34)
        for lb in p.get("labels", []):
            cx, cy = x0 + lb["x"] * (x1 - x0), y0 + lb["y"] * (y1 - y0)
            hw = lb.get("w", 0.45) * (x1 - x0) / 2
            draw_text_block(canvas, (cx - hw, cy - 200, cx + hw, cy + 200), lb["text"], lb.get("size", 52), 22,
                            anchor="center", color=COLORS.get(lb.get("color", "white"), WHITE))
    if spec.get("text"):
        draw_text_block(canvas, (40, 0, W - 40, H - FOOT_H - 14), spec["text"], spec.get("text_size", 66))
    footer(canvas)
    glow_frame(canvas)
    chevrons(canvas, 46, 54, up=True)
    chevrons(canvas, W - 46, H * 0.66, up=False)
    logo(canvas, size=int(150 * W / 1200))
    canvas.convert("RGB").save(out, quality=92)
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--example":
        print(json.dumps(EXAMPLE, indent=1))
    elif len(sys.argv) == 3:
        sp = json.load(open(sys.argv[1], encoding="utf-8"))
        base = os.path.dirname(os.path.abspath(sys.argv[1]))
        for p in sp["panels"]:
            if not os.path.isabs(p["image"]):
                p["image"] = os.path.join(base, p["image"])
        render(sp, sys.argv[2])
    else:
        print(__doc__)
