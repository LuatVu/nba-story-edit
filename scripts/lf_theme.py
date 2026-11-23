"""Turn On Hoops long-form theme ("Vice neon"): the house style for every long-form video.

Extracted from "How GTA 6 Took Over the NBA" (Nov 2026). Spec: references/longform-theme.md.

What it gives you
  * tokens: PINK #FF40A0, TEAL #28E1D7, INK..., fonts (Anton, Montserrat ExtraBold)
  * frame_overlay(): the 82 % rounded footage window on a dark 48 px grid with a thin pink edge
  * GRADE[...]: ffmpeg colour strings for footage ("" normal, "arch" archival)
  * chapter_card(), title_card(), end_card(): 1920x1080 PNGs
  * 8 animated graphic templates (stat, bars, timeline, org, map, threshold, flywheel, quote),
    rendered from a JSON spec over a blurred, darkened, Ken-Burns photo background.

Usage
  python lf_theme.py --example                      # print an example graphics spec (JSON)
  python lf_theme.py spec.json OUTDIR [ids...]      # render graphics -> OUTDIR/<id>.mp4 + <id>_final.png
  python lf_theme.py spec.json OUTDIR --still       # final frame only (fast layout check)
  python lf_theme.py --card "CHAPTER 3" "THE\\nTEST RUNS" bg.png out.png
  python lf_theme.py --title "HOW GTA 6\\nTOOK OVER\\nTHE NBA" bg.png out.png
  python lf_theme.py --frame out.png                # write the footage frame overlay

Spec format: {"graphics": [ {id, kind, bg, dur, kicker, source, ...template fields} ]}
Every "t" is seconds from the start of that clip. Make each clip start LEAD (0.5 s) before its cue word
and put each element's t on the word that names it (take times from the VO word timestamps).
In Python you can also `import lf_theme` and call render(g, outdir) with the same dicts.
"""
import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
FONTS = os.path.join(SKILL, "assets", "fonts")
ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
MONT = os.path.join(FONTS, "Montserrat-ExtraBold.ttf")
LAND = os.path.join(SKILL, "assets", "data", "ne_110m_land.geojson")
W, H, FPS = 1920, 1080, 30
LEAD = 0.5

# ---------------------------------------------------------------- tokens
PINK = (255, 64, 160)            # #FF40A0  primary accent: kicker boxes, hero bars, nodes, arcs, highlights, frame edge
TEAL = (40, 225, 215)            # #28E1D7  secondary: offset shadow under big numbers/titles, key node, multipliers, gaps
INK, INK2, INK3 = (255, 255, 255), (225, 220, 232), (170, 164, 180)  # number / label / source text
STROKE = (10, 6, 16)             # #0A0610  outline on big type
CONTEXT = (190, 184, 200)        # #BEB8C8  comparison bars / the "other side"
PANEL = (18, 10, 26)             # #120A1A  box fills (82-85 % alpha)
CARD_SHADE = (8, 4, 20)          # #080414  left gradient on chapter cards
FRAME_BG, FRAME_GRID = (10, 9, 14), (22, 20, 30)   # #0A090E / #16141E
WX, WY, WW, WH = 173, 97, 1574, 886                 # 82 % footage window
GRADE = {"": "eq=contrast=1.06:saturation=0.96",
         "arch": "eq=contrast=1.08:saturation=0.62,noise=alls=16:allf=t"}

_fc = {}
def font(path, size):
    k = (path, int(size))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, int(size))
    return _fc[k]

def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3

def prog(t, t0, dur=0.45):
    return ease((t - t0) / dur) if t >= t0 else 0.0

def alpha(c, a):
    return (c[0], c[1], c[2], int(255 * max(0, min(1, a))))

def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

# ---------------------------------------------------------------- type helpers
def text(d, xy, s, f, fill, a=1.0, anchor="la", stroke=0, shadow=None, spacing=6):
    """Theme text: optional teal (or any) shadow offset +7/+7, dark stroke."""
    if a <= 0:
        return
    x, y = xy
    al = "center" if anchor[0] == "m" else ("right" if anchor[0] == "r" else "left")
    if shadow:
        d.multiline_text((x + 7, y + 7), s, font=f, fill=alpha(shadow, a), anchor=anchor, stroke_width=stroke,
                         stroke_fill=alpha(shadow, a), spacing=spacing, align=al)
    d.multiline_text((x, y), s, font=f, fill=alpha(fill, a), anchor=anchor, stroke_width=stroke,
                     stroke_fill=alpha(STROKE, a), spacing=spacing, align=al)

def kicker(d, s, a=1.0, x=120, y=96):
    """Pink label box, top left: the title of every graphic."""
    if not s or a <= 0:
        return
    f = font(MONT, 40)
    w = d.textlength(s, font=f)
    d.rectangle([x, y, x + w + 40, y + 64], fill=alpha(PINK, a))
    text(d, (x + 20, y + 32), s, f, INK, a, anchor="lm")

def footnote(d, s, a=1.0):
    if s:
        text(d, (120, H - 70), s, font(MONT, 24), INK3, a * 0.95, anchor="ls")

def count_text(final, p):
    """Count-up for 27, 230K, $975,000, 1.1M+, ~90 MIN. Anything else pops as-is."""
    m = re.match(r"^([^0-9]*)([0-9][0-9,]*\.?[0-9]*)(.*)$", final)
    if not m or p >= 1:
        return final
    pre, num, suf = m.groups()
    dec = len(num.split(".")[1]) if "." in num else 0
    v = float(num.replace(",", "")) * ease(p)
    s = f"{v:,.{dec}f}" if "," in num else f"{v:.{dec}f}"
    return pre + s + suf

def bar_top_rounded(d, x0, y0, x1, y1, fill, r=4):
    if y1 - y0 < 1:
        return
    d.rounded_rectangle([x0, y0, x1, y1], min(r, (y1 - y0) / 2), fill=fill)
    d.rectangle([x0, max(y0, y1 - r), x1, y1], fill=fill)

def arrow_head(d, tip, ang, size, fill):
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.polygon([tip, (tip[0] + size * math.cos(a1), tip[1] + size * math.sin(a1)),
               (tip[0] + size * math.cos(a2), tip[1] + size * math.sin(a2))], fill=fill)

def partial_poly(d, pts, p, fill, width):
    """Draw the first fraction p of a polyline (path-draw reveal). Returns (tip, angle)."""
    if p <= 0 or len(pts) < 2:
        return None
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg) * p; out = [pts[0]]
    for i, s in enumerate(seg):
        if L >= s:
            out.append(pts[i + 1]); L -= s
        else:
            f = L / s if s else 0
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f))
            break
    d.line(out, fill=fill, width=width, joint="curve")
    a, b = out[-2], out[-1]
    return b, math.atan2(b[1] - a[1], b[0] - a[0])

def bezier(p0, p1, p2, n=60):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

# ---------------------------------------------------------------- backgrounds
class Background:
    """Real photo, blurred 30 px, 45 % brightness, +15 % colour, vignette, slow zoom 100->106 % + drift."""
    def __init__(self, path, focus=(0.5, 0.5), zoom_in=True):
        im = Image.open(path).convert("RGB")
        bw, bh = int(W * 1.12), int(H * 1.12)
        s = max(bw / im.width, bh / im.height)
        im = im.resize((max(bw, int(im.width * s)), max(bh, int(im.height * s))), Image.LANCZOS)
        l = int((im.width - bw) * focus[0]); t = int((im.height - bh) * focus[1])
        im = im.crop((l, t, l + bw, t + bh)).filter(ImageFilter.GaussianBlur(30))
        im = ImageEnhance.Color(ImageEnhance.Brightness(im).enhance(0.45)).enhance(1.15)
        self.im, self.zoom_in = im, zoom_in
        g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
        for i in range(60):
            gd.rectangle([i * 6, i * 4, W - i * 6, H - i * 4], outline=int(150 * (1 - i / 60) ** 2), width=7)
        self.vig = Image.merge("RGBA", [Image.new("L", (W, H), 8)] * 3 + [g.filter(ImageFilter.GaussianBlur(40))])

    def frame(self, p):
        z = 1.0 + 0.06 * (p if self.zoom_in else 1 - p)
        cw, ch = int(W * 1.12 / z), int(H * 1.12 / z)
        cx = (self.im.width - cw) / 2 + (p - 0.5) * 0.02 * W
        cy = (self.im.height - ch) / 2
        f = self.im.crop((int(cx), int(cy), int(cx) + cw, int(cy) + ch)).resize((W, H), Image.BILINEAR).convert("RGBA")
        f.alpha_composite(self.vig)
        return f

def frame_overlay(out):
    """82 % rounded window (radius 22) cut out of a #0A090E panel with a #16141E 48 px grid and a thin pink edge.
    Overlay it on footage scaled+cropped to 1574x886 at (173, 97)."""
    im = Image.new("RGBA", (W, H), FRAME_BG + (255,)); d = ImageDraw.Draw(im)
    for x in range(0, W, 48):
        d.line([(x, 0), (x, H)], fill=FRAME_GRID + (255,), width=1)
    for y in range(0, H, 48):
        d.line([(0, y), (W, y)], fill=FRAME_GRID + (255,), width=1)
    m = Image.new("L", (W * 2, H * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([WX * 2, WY * 2, (WX + WW) * 2, (WY + WH) * 2], 44, fill=255)
    m = m.resize((W, H), Image.LANCZOS)
    im.putalpha(Image.composite(Image.new("L", (W, H), 0), im.split()[3], m))
    e = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    ImageDraw.Draw(e).rounded_rectangle([WX * 2 - 3, WY * 2 - 3, (WX + WW) * 2 + 3, (WY + WH) * 2 + 3], 46,
                                        outline=PINK + (150,), width=4)
    im.alpha_composite(e.resize((W, H), Image.LANCZOS))
    im.save(out)
    return out

def footage_filter(opt="", slow=False):
    """ffmpeg filter_complex for framed footage: input 0 = clip, input 1 = frame_overlay PNG (-loop 1)."""
    return (f"[0:v]{'setpts=2*PTS,' if slow else ''}fps={FPS},scale={WW}:{WH}:force_original_aspect_ratio=increase,"
            f"crop={WW}:{WH},setsar=1,{GRADE[opt]}[f];color=c=0x0a090e:s={W}x{H}:r={FPS}[bg];"
            f"[bg][f]overlay={WX}:{WY}:shortest=1[x];[x][1:v]overlay=0:0,format=yuv420p[o]")

# ---------------------------------------------------------------- cards
def _cover(path):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))

def _left_shade(im):
    grad = Image.new("L", (W, H)); gd = ImageDraw.Draw(grad)
    for x in range(W):
        gd.line([(x, 0), (x, H)], fill=int(max(0, 190 - x * 0.16)))
    return Image.composite(Image.new("RGB", (W, H), CARD_SHADE), im, grad)

def _poster_title(d, xy, title, size):
    f = font(ANTON, size)
    x, y = xy
    d.multiline_text((x + 8, y + 8), title, font=f, fill=TEAL, stroke_width=10, stroke_fill=STROKE, spacing=10)
    d.multiline_text((x, y), title, font=f, fill=INK, stroke_width=10, stroke_fill=STROKE, spacing=10)

def chapter_card(kicker_txt, title, bg, out):
    """Full image (AI art or photo) + left shade + pink 'CHAPTER N' box + Anton title, white/black stroke, teal offset."""
    im = _left_shade(_cover(bg)); d = ImageDraw.Draw(im)
    y = 250 if kicker_txt else 200
    if kicker_txt:
        fk = font(MONT, 46)
        d.rectangle([120, y - 90, 120 + d.textlength(kicker_txt, font=fk) + 40, y - 20], fill=PINK)
        d.text((140, y - 85), kicker_txt, font=fk, fill=INK)
    _poster_title(d, (120, y), title, 170)
    im.save(out); return out

def title_card(title, bg, out):
    im = _left_shade(_cover(bg)); d = ImageDraw.Draw(im)
    _poster_title(d, (120, 200), title, 190)
    im.save(out); return out

def end_card(bg, out, headline="WHO'S NEXT?", sub="TELL ME IN THE COMMENTS", left="WATCH NEXT", right=""):
    """End-screen layout: two 760x428 video slots (pink outline) + subscribe ring (teal). Hold 5-20 s."""
    im = ImageEnhance.Brightness(_cover(bg).filter(ImageFilter.GaussianBlur(6))).enhance(0.55).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.text((960 + 6, 150 + 6), headline, font=font(ANTON, 84), fill=TEAL, anchor="mm")
    d.text((960, 150), headline, font=font(ANTON, 84), fill=INK, anchor="mm", stroke_width=6, stroke_fill=STROKE)
    d.text((960, 235), sub, font=font(MONT, 34), fill=INK2, anchor="mm")
    for x0, lab in ((150, left), (1010, right)):
        d.rounded_rectangle([x0, 330, x0 + 760, 758], 18, fill=(12, 8, 18, 200), outline=PINK, width=5)
        if lab:
            d.text((x0 + 380, 790), lab, font=font(MONT, 30), fill=INK2, anchor="mm")
    d.ellipse([960 - 95, 845, 960 + 95, 1035], outline=TEAL, width=6)
    im.convert("RGB").save(out); return out

# ---------------------------------------------------------------- graphic templates
def draw_stat(d, t, g, lay=None):
    """items: [{v, label, t, color?, shadow?, count?}] · sep? · vsize? · cy? · dividers?"""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    items = g["items"]; n = len(items)
    colw = (W - 240) / n
    vsize = g.get("vsize", 230 if n <= 2 else 200)
    cy = g.get("cy", 520)
    for i, it in enumerate(items):
        p = prog(t, it["t"], 0.5)
        if p <= 0:
            continue
        cx = 120 + colw * (i + 0.5)
        val = count_text(it["v"], (t - it["t"]) / 0.8) if it.get("count", True) else it["v"]
        dy = (1 - p) * 50
        text(d, (cx, cy - 20 + dy), val, font(ANTON, vsize), tuple(it.get("color", INK)), p, anchor="ms", stroke=6,
             shadow=tuple(it.get("shadow", TEAL)))
        text(d, (cx, cy + 40 + dy), it["label"], font(MONT, 40), INK2, p, anchor="ma", spacing=10)
        if i > 0 and g.get("dividers", True):
            x = 120 + colw * i
            d.line([(x, cy - vsize * 0.75), (x, cy + 90)], fill=alpha(INK, 0.25 * p), width=2)
    if g.get("sep") and n > 1:
        text(d, (W / 2, cy - 40), g["sep"], font(ANTON, 160), INK3, prog(t, items[1]["t"]), anchor="ms")
    footnote(d, g.get("source"), prog(t, 0.3))

def draw_bars(d, t, g, lay=None):
    """bars: [{cat, v, label, color?, t}] (2-4 bars, hero bar PINK, others CONTEXT) · mult? {v, label, t} · notes?"""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    base, top = 860, 300
    bars = g["bars"]; nb = len(bars)
    vmax = max(b["v"] for b in bars)
    bw = 300 if nb <= 2 else 220; gap = 220 if nb <= 2 else 120
    span = nb * bw + (nb - 1) * gap
    x0 = W / 2 - span / 2
    d.line([(x0 - 120, base), (x0 + span + 120, base)], fill=alpha(INK, 0.35), width=2)
    for i, b in enumerate(bars):
        p = prog(t, b["t"], 0.9)
        bx = x0 + i * (bw + gap)
        text(d, (bx + bw / 2, base + 24), b["cat"], font(MONT, 40), INK2, prog(t, b["t"] - 0.2), anchor="ma", spacing=8)
        if p <= 0:
            continue
        hgt = (base - top) * b["v"] / vmax * p
        bar_top_rounded(d, bx, base - hgt, bx + bw, base, alpha(tuple(b.get("color", PINK)), 1))
        val = b["label"] if p >= 1 else count_text(b["label"], p)
        text(d, (bx + bw / 2, base - hgt - 22), val, font(ANTON, 96), INK, prog(t, b["t"]), anchor="ms", stroke=5)
    for nt in g.get("notes", []):
        p = prog(t, nt["t"])
        text(d, (120, 400 + (1 - p) * 30), nt["v"], font(ANTON, 120), INK, p, anchor="ls", stroke=5, shadow=TEAL)
        text(d, (124, 424), nt["label"], font(MONT, 30), INK2, p, anchor="la", spacing=8)
    if "mult" in g:
        p = prog(t, g["mult"]["t"], 0.35)
        if p > 0:
            s = 0.6 + 0.4 * p
            text(d, (x0 + span + 60, 470), g["mult"]["v"], font(ANTON, int(130 * s)), TEAL, p, anchor="ls", stroke=6)
            text(d, (x0 + span + 64, 500), g["mult"].get("label", ""), font(MONT, 30), INK2, p, anchor="la")
    footnote(d, g.get("source"), prog(t, 0.3))

def draw_timeline(d, t, g, lay=None):
    """nodes: [{year, label, t, color?, big?}] - last/key node TEAL + big."""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    nodes = g["nodes"]; n = len(nodes)
    y = 560; xs = [260 + i * (W - 520) / max(1, n - 1) for i in range(n)]
    for i, nd in enumerate(nodes):
        if i > 0:
            p = prog(t, nd["t"] - 0.35, 0.4)
            if p > 0:
                d.line([(xs[i - 1], y), (xs[i - 1] + (xs[i] - xs[i - 1]) * p, y)], fill=alpha(INK, 0.6), width=4)
    for i, nd in enumerate(nodes):
        p = prog(t, nd["t"], 0.4)
        if p <= 0:
            continue
        c = tuple(nd.get("color", PINK)); r = (26 if nd.get("big") else 18) * (0.5 + 0.5 * p)
        d.ellipse([xs[i] - r - 6, y - r - 6, xs[i] + r + 6, y + r + 6], fill=alpha((20, 12, 28), p))
        d.ellipse([xs[i] - r, y - r, xs[i] + r, y + r], fill=alpha(c, p))
        text(d, (xs[i], y - 60 + (1 - p) * 30), nd["year"], font(ANTON, 120 if nd.get("big") else 104), INK, p,
             anchor="ms", stroke=5, shadow=c)
        text(d, (xs[i], y + 60), nd["label"], font(MONT, 36), INK2, p, anchor="ma", spacing=10)
    footnote(d, g.get("source"), prog(t, 0.3))

def draw_org(d, t, g, lay=None):
    """top {title, sub, t} (TEAL box) -> kids [{title, sub, t}] (PINK boxes, 2-3)."""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    def box(cx, cy, w, h, title, sub, c, p):
        if p <= 0:
            return
        dy = (1 - p) * 40
        d.rounded_rectangle([cx - w / 2, cy - h / 2 + dy, cx + w / 2, cy + h / 2 + dy], 18, fill=alpha(PANEL, 0.82 * p))
        d.rounded_rectangle([cx - w / 2, cy - h / 2 + dy, cx + w / 2, cy + h / 2 + dy], 18, outline=alpha(c, p), width=5)
        text(d, (cx, cy + 10 + dy), title, font(ANTON, 84), INK, p, anchor="ms")
        text(d, (cx, cy + 30 + dy), sub, font(MONT, 34), c, p, anchor="ma")
    top, kids = g["top"], g["kids"]
    pt = prog(t, top["t"]); ty, ky = 360, 760
    nk = len(kids); kx = [W / 2 + (i - (nk - 1) / 2) * (860 if nk == 2 else 600) for i in range(nk)]
    kw = 620 if nk == 2 else 520
    lp = prog(t, top["t"] + 0.25, 0.5)
    if lp > 0:
        mid = (ty + ky) / 2
        for x in kx:
            partial_poly(d, [(W / 2, ty + 95), (W / 2, mid), (x, mid), (x, ky - 95)], lp, alpha(INK, 0.7), 4)
    box(W / 2, ty, 760, 190, top["title"], top["sub"], TEAL, pt)
    for x, k in zip(kx, kids):
        box(x, ky, kw, 190, k["title"], k["sub"], PINK, prog(t, k["t"]))
    footnote(d, g.get("source"), prog(t, 0.3))

_land = {}
def land_dots(box, step=13):
    key = (box, step)
    if key not in _land:
        gj = json.load(open(LAND, encoding="utf-8"))
        x0, y0, x1, y1, lat0, lat1 = box
        m = Image.new("L", (W, H), 0); md = ImageDraw.Draw(m)
        pj = lambda lon, lat: (x0 + (lon + 180) / 360 * (x1 - x0), y0 + (lat0 - lat) / (lat0 - lat1) * (y1 - y0))
        for f in gj["features"]:
            geo = f["geometry"]
            for poly in ([geo["coordinates"]] if geo["type"] == "Polygon" else geo["coordinates"]):
                md.polygon([pj(*c) for c in poly[0]], fill=255)
        dots = [(x, y) for y in range(int(y0), int(y1), step) for x in range(int(x0), int(x1), step) if m.getpixel((x, y))]
        _land[key] = (dots, pj)
    return _land[key]

def draw_map(d, t, g, lay=None):
    """origin {name, ll:[lon,lat], t} (pulsing PINK) · cities [{name, ll, t}] (PINK arcs -> TEAL dots) · stats [{v, label, t}]."""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    dots, pj = land_dots((560, 230, 1840, 230 + int(1280 / 360 * 140), 82, -58))
    pm = prog(t, 0.0, 0.8)
    for (x, y) in dots:
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=alpha(INK, 0.28 * pm))
    o = pj(*g["origin"]["ll"]); po = prog(t, g["origin"]["t"])
    if po > 0:
        r = 10 + 30 * ((t * 0.8) % 1)
        d.ellipse([o[0] - r, o[1] - r, o[0] + r, o[1] + r], outline=alpha(PINK, po * (1 - (t * 0.8) % 1)), width=3)
        d.ellipse([o[0] - 10, o[1] - 10, o[0] + 10, o[1] + 10], fill=alpha(PINK, po))
        text(d, (o[0] - 18, o[1] + 14), g["origin"].get("name", ""), font(MONT, 30), INK, po, anchor="ra")
    for c in g.get("cities", []):
        p = prog(t, c["t"], 0.8)
        if p <= 0:
            continue
        dst = pj(*c["ll"])
        tip = partial_poly(d, bezier(o, ((o[0] + dst[0]) / 2, min(o[1], dst[1]) - 140), dst), p, alpha(PINK, 0.95), 4)
        if p >= 0.98:
            pa = prog(t, c["t"] + 0.75, 0.3)
            d.ellipse([dst[0] - 9, dst[1] - 9, dst[0] + 9, dst[1] + 9], fill=alpha(TEAL, pa))
            text(d, (dst[0], dst[1] + 18), c["name"], font(MONT, 30), INK, pa, anchor="ma")
    for i, s in enumerate(g.get("stats", [])):
        p = prog(t, s["t"], 0.5); y = 330 + i * 300
        text(d, (120, y + 150 + (1 - p) * 40), count_text(s["v"], (t - s["t"]) / 0.8), font(ANTON, 200), INK, p,
             anchor="ls", stroke=6, shadow=TEAL)
        text(d, (124, y + 172), s["label"], font(MONT, 34), INK2, p, anchor="la", spacing=8)
    footnote(d, g.get("source"), prog(t, 0.3))

def draw_threshold(d, t, g, lay=None):
    """max · value {v, label, sub, t} (PINK bar) · line {label, t} (dashed limit) · gap {label, t} (TEAL bracket)."""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    x0, x1, y = 200, 1440, 600
    sx = lambda v: x0 + (x1 - x0) * v / g["max"]
    d.line([(x0, y + 70), (x1 + 120, y + 70)], fill=alpha(INK, 0.3), width=2)
    val = g["value"]; pv = prog(t, val["t"], 1.0)
    if pv > 0:
        d.rounded_rectangle([x0, y - 60, sx(val["v"] * pv), y + 60], 4, fill=alpha(PINK, 1))
        text(d, (x0, y - 110), count_text(val["label"], (t - val["t"]) / 1.0), font(ANTON, 170), INK, prog(t, val["t"]),
             anchor="ls", stroke=6, shadow=TEAL)
        text(d, (x0 + 8, y + 95), val.get("sub", ""), font(MONT, 34), INK2, prog(t, val["t"]), anchor="la")
    if "line" in g:
        pl = prog(t, g["line"]["t"], 0.5)
        if pl > 0:
            for yy in range(int(y - 220), int(y - 220 + 440 * pl), 26):
                d.line([(x1, yy), (x1, min(yy + 14, y + 220))], fill=alpha(INK, 0.95), width=5)
            text(d, (x1 + 24, y - 200), g["line"]["label"], font(MONT, 34), INK, pl, anchor="la", spacing=10)
    if "gap" in g:
        pg = prog(t, g["gap"]["t"], 0.4)
        if pg > 0:
            a, b = sx(val["v"]), x1; yb = y + 95
            for seg in (((a, yb), (b, yb)), ((a, yb - 16), (a, yb + 16)), ((b, yb - 16), (b, yb + 16))):
                d.line(seg, fill=alpha(TEAL, pg), width=5)
            text(d, (b, y + 125), g["gap"]["label"], font(ANTON, 96), TEAL, pg, anchor="ra", stroke=4)
    footnote(d, g.get("source"), prog(t, 0.3))

def draw_flywheel(d, t, g, lay=None):
    """center {v, t} · left/right {v, sub, color, t} · arrows [{dir: lr|rl, label, color, t}] · winners [{v, who, t}]."""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    cy, r = 400, 150
    L, R = (W / 2 - 360, cy), (W / 2 + 360, cy)
    if "center" in g:
        text(d, (W / 2, cy + 14), g["center"]["v"], font(MONT, 34), INK2, prog(t, g["center"]["t"]), anchor="mm", spacing=8)
    for c, n in ((L, g["left"]), (R, g["right"])):
        p = prog(t, n["t"], 0.5)
        if p <= 0:
            continue
        rr = r * (0.6 + 0.4 * p); col = tuple(n.get("color", PINK))
        d.ellipse([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], fill=alpha(PANEL, 0.85 * p), outline=alpha(col, p), width=7)
        text(d, (c[0], c[1] + 8), n["v"], font(ANTON, 96), INK, p, anchor="mm")
        text(d, (c[0], c[1] + rr + 24), n.get("sub", ""), font(MONT, 30), INK2, p, anchor="ma")
    for a in g.get("arrows", []):
        p = prog(t, a["t"], 0.9)
        if p <= 0:
            continue
        top = a["dir"] == "lr"; col = tuple(a.get("color", PINK))
        s, e = ((L[0] + 60, cy - r - 10), (R[0] - 60, cy - r - 10)) if top else ((R[0] - 60, cy + r + 70), (L[0] + 60, cy + r + 70))
        res = partial_poly(d, bezier(s, (W / 2, cy - r - 150) if top else (W / 2, cy + r + 200), e), p, alpha(col, 1), 7)
        if res:
            arrow_head(d, res[0], res[1], 30, alpha(col, 1))
        text(d, (W / 2, (cy - r - 112) if top else (cy + r + 150)), a["label"], font(MONT, 30), INK, prog(t, a["t"] + 0.4), anchor="mm")
    ws = g.get("winners", [])
    for i, wnr in enumerate(ws):
        p = prog(t, wnr["t"], 0.45)
        if p <= 0:
            continue
        cx = 120 + (W - 240) / len(ws) * (i + 0.5); y = 900 + (1 - p) * 40
        text(d, (cx, y - 8), wnr["v"], font(ANTON, 96), INK, p, anchor="ms", stroke=5, shadow=TEAL)
        text(d, (cx, y + 18), wnr["who"], font(MONT, 32), INK2, p, anchor="ma")
    footnote(d, g.get("source"), prog(t, 0.3))

_avc = {}
def avatar(spec, size=300):
    """spec = [path, cx, cy, half] (relative coords of the face in a real photo) -> round crop."""
    key = tuple(spec)
    if key not in _avc:
        path, cx, cy, half = spec
        im = Image.open(path).convert("RGB"); h = half * im.height
        im = im.crop((int(cx * im.width - h), int(cy * im.height - h), int(cx * im.width + h), int(cy * im.height + h)))
        im = im.resize((size, size), Image.LANCZOS)
        m = Image.new("L", (size * 4, size * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
        im.putalpha(m.resize((size, size), Image.LANCZOS)); _avc[key] = im
    return _avc[key]

def draw_quote(d, t, g, lay=None):
    """text · wt [time per word] (from VO; if missing, words appear every 0.22 s from 0.4) · hl [word indexes, PINK]
    · name · role · avatar? [path, cx, cy, half] · marks? (big pink quote mark when no avatar) · size? · attr_t?"""
    kicker(d, g.get("kicker"), prog(t, 0.1))
    has_av = bool(g.get("avatar"))
    x0 = 620 if has_av else 260
    maxw = W - x0 - 160
    f = font(MONT, g.get("size", 68))
    sp = d.textlength(" ", font=f); lh = int(f.size * 1.3)
    words_ = g["text"].split()
    wt = g.get("wt") or [0.4 + 0.22 * i for i in range(len(words_))]
    lines, cur, w = [], [], 0
    for i, wd in enumerate(words_):
        ww = d.textlength(wd, font=f)
        if cur and w + sp + ww > maxw:
            lines.append(cur); cur, w = [], 0
        cur.append((i, wd, ww)); w += (sp if len(cur) > 1 else 0) + ww
    lines.append(cur)
    th = len(lines) * lh
    y0 = 540 - (th + 170) / 2
    if g.get("marks", True) and not has_av:
        text(d, (x0 - 150, y0 + 210), "“", font(ANTON, 280), PINK, prog(t, 0.2), anchor="ls")
    hl = set(g.get("hl", []))
    for li, line in enumerate(lines):
        x = x0
        for (i, wd, ww) in line:
            p = prog(t, wt[i] - 0.05, 0.22)
            if p > 0:
                text(d, (x, y0 + li * lh + (1 - p) * 18), wd, f, PINK if i in hl else INK, p, anchor="la")
            x += ww + sp
    pa = prog(t, g.get("attr_t", 0.5))
    ya = y0 + th + 50
    d.rectangle([x0, ya, x0 + 80 * pa, ya + 6], fill=alpha(TEAL, pa))
    text(d, (x0, ya + 30), g.get("name", ""), font(ANTON, 64), INK, pa, anchor="la")
    text(d, (x0, ya + 112), g.get("role", ""), font(MONT, 30), INK2, pa, anchor="la")
    if has_av and lay is not None:
        pv = prog(t, 0.15, 0.5)
        if pv > 0:
            s = int(300 * (0.85 + 0.15 * pv))
            a2 = avatar(g["avatar"]).resize((s, s), Image.LANCZOS)
            a2.putalpha(a2.split()[3].point(lambda v: int(v * pv)))
            cx, cy = 310, 540
            d.ellipse([cx - s / 2 - 8, cy - s / 2 - 8, cx + s / 2 + 8, cy + s / 2 + 8], fill=alpha(PINK, pv))
            lay.alpha_composite(a2, (int(cx - s / 2), int(cy - s / 2)))
    footnote(d, g.get("source"), prog(t, 0.3))

DRAW = {"stat": draw_stat, "bars": draw_bars, "timeline": draw_timeline, "org": draw_org, "map": draw_map,
        "threshold": draw_threshold, "flywheel": draw_flywheel, "quote": draw_quote}

# ---------------------------------------------------------------- render
def render(g, outdir, still=False, base=""):
    os.makedirs(outdir, exist_ok=True)
    bgp = g["bg"] if os.path.isabs(g["bg"]) else os.path.join(base, g["bg"])
    bg = Background(bgp, tuple(g.get("focus", (0.5, 0.5))), zoom_in=g.get("zoom_in", hash(g["id"]) % 2 == 0))
    if g.get("avatar") and not os.path.isabs(g["avatar"][0]):
        g = dict(g, avatar=[os.path.join(base, g["avatar"][0])] + list(g["avatar"][1:]))
    n = int(round(g["dur"] * FPS))
    def frame(i):
        t = i / FPS
        f = bg.frame(i / max(1, n - 1))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        DRAW[g["kind"]](ImageDraw.Draw(lay), t, g, lay)
        f.alpha_composite(lay)
        return f.convert("RGB")
    frame(n - 1).save(os.path.join(outdir, f"{g['id']}_final.png"))
    if still:
        return
    cmd = [ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
           os.path.join(outdir, f"{g['id']}.mp4")]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        pr.stdin.write(frame(i).tobytes())
    pr.stdin.close(); pr.wait()

EXAMPLE = {"graphics": [
    {"id": "G01_statline", "kind": "stat", "bg": "images/frame_giannis.jpg", "dur": 6.0,
     "kicker": "GIANNIS VS. HIS OLD TEAM", "source": "Source: NBC Miami · Nov 18, 2026",
     "items": [{"v": "27", "label": "POINTS", "t": 0.5}, {"v": "14", "label": "REBOUNDS", "t": 1.3},
               {"v": "9", "label": "ASSISTS", "t": 2.1}]},
    {"id": "G02_sales", "kind": "bars", "bg": "images/poster.jpg", "dur": 7.0, "kicker": "DAY-ONE SALES",
     "source": "Source: Take-Two", "bars": [{"cat": "GTA V\n2013", "v": 0.8, "label": "~$800M", "color": list(CONTEXT), "t": 0.6},
                                            {"cat": "GTA VI\n2026", "v": 3.79, "label": "~$3.79B", "t": 2.0}],
     "mult": {"v": "~4.7×", "label": "GTA V'S DAY ONE", "t": 3.2}},
    {"id": "G03_timeline", "kind": "timeline", "bg": "images/jersey.jpg", "dur": 6.0, "kicker": "SAME ROOT, FOUR DECADES",
     "nodes": [{"year": "1984", "label": "MIAMI VICE", "t": 0.5}, {"year": "2002", "label": "GTA: VICE CITY", "t": 1.2},
               {"year": "2026", "label": "VICE CITY HEAT", "t": 2.4, "color": list(TEAL), "big": True}]},
    {"id": "Q01_quote", "kind": "quote", "bg": "images/artwork.png", "dur": 5.0, "kicker": "DEC 5, 2023 · ON X",
     "text": "GTA6 looks INSANE!!!! SHEESH.", "hl": [2, 3], "name": "LEBRON JAMES", "role": "@KINGJAMES",
     "avatar": ["images/lebron.jpg", 0.48, 0.30, 0.22]},
]}

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); sys.exit(0)
    if a[0] == "--example":
        print(json.dumps(EXAMPLE, indent=1, ensure_ascii=False)); sys.exit(0)
    if a[0] == "--card":
        print(chapter_card(a[1], a[2].replace("\\n", "\n"), a[3], a[4])); sys.exit(0)
    if a[0] == "--title":
        print(title_card(a[1].replace("\\n", "\n"), a[2], a[3])); sys.exit(0)
    if a[0] == "--frame":
        print(frame_overlay(a[1])); sys.exit(0)
    spec, outdir = a[0], a[1]
    ids = [x for x in a[2:] if not x.startswith("--")]
    G = json.load(open(spec, encoding="utf-8"))["graphics"]
    base = os.path.dirname(os.path.abspath(spec))
    for g in G:
        if ids and not any(g["id"].startswith(i) for i in ids):
            continue
        print(f"{g['id']:<28} {g['kind']:<9} {g['dur']:5.1f}s", flush=True)
        render(g, outdir, still="--still" in a, base=base)
