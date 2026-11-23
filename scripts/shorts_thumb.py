#!/usr/bin/env python3
"""Shorts cover / thumbnail in the reference channel's style.

Measured from 3 covers: flat team-colour background with a radial glow (lighter at the
top-centre, darker at the edges); 1-2 word title, ALL CAPS, very heavy condensed sans
(Anton-like), white, two stacked lines filling ~85 % of the width in the upper third;
one player cutout, chest-up, centred, his head overlapping the bottom of the title
(player in FRONT of the text). Nothing else: no logo, no arrow, no emoji, no border.

The Shorts shelf shows a 2:3 centre crop of the 9:16 frame (1080x1607 of 1080x1920),
so title and face must sit inside y = 156..1763. --preview writes that crop too.

Usage:
  python shorts_thumb.py cutout.png "WARRIORS\\nTRADE" out.png --team GSW
  python shorts_thumb.py cutout.png "LAST\\nCHANCE" out.png --color "#1D428A" --preview
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shorts_common import H, TITLE_FONTS, W, font  # noqa: E402

# Primary-ish background colour per team (deep enough for white text).
TEAM = {
    "ATL": "#C8102E", "BOS": "#007A33", "BKN": "#2B2B2B", "CHA": "#1D1160", "CHI": "#CE1141",
    "CLE": "#860038", "DAL": "#00538C", "DEN": "#0E2240", "DET": "#C8102E", "GSW": "#1D428A",
    "HOU": "#CE1141", "IND": "#002D62", "LAC": "#1D428A", "LAL": "#552583", "MEM": "#5D76A9",
    "MIA": "#98002E", "MIL": "#00471B", "MIN": "#0C2340", "NOP": "#0C2340", "NYK": "#006BB6",
    "OKC": "#007AC1", "ORL": "#0077C0", "PHI": "#006BB6", "PHX": "#1D1160", "POR": "#E03A3E",
    "SAC": "#5A2D81", "SAS": "#2B2B2B", "TOR": "#CE1141", "UTA": "#002B5C", "WAS": "#002B5C",
}


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def background(color):
    c = rgb(color)
    base = Image.new("RGB", (W, H), tuple(int(v * 0.35) for v in c))
    g = Image.radial_gradient("L").resize((int(W * 2.2), int(H * 1.5)))
    mask = g.point(lambda v: max(0, 255 - int(v * 1.15)))
    bright = Image.new("RGB", g.size, tuple(min(255, int(v * 1.25 + 20)) for v in c))
    base.paste(bright, ((W - g.width) // 2, -int(H * 0.45)), mask)
    return base


def fit_title(lines, maxw, maxh_line):
    size = 400
    while size > 40:
        f = font(TITLE_FONTS, size)
        b = f.getbbox("H")
        if all(f.getlength(ln) <= maxw for ln in lines) and b[3] - b[1] <= maxh_line:
            return f
        size -= 6
    return font(TITLE_FONTS, size)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cutout")
    ap.add_argument("title", help=r'use "\n" between the two lines')
    ap.add_argument("out")
    ap.add_argument("--team", choices=sorted(TEAM))
    ap.add_argument("--color", help="background hex, overrides --team")
    ap.add_argument("--head", type=float,
                    help="y of the top of the head (fraction). Default: just above the bottom of the "
                         "title so the head overlaps the last line, as on the reference covers")
    ap.add_argument("--overlap", type=float, default=0.045, help="how far the head rises into the title")
    ap.add_argument("--height", type=float, default=0.66, help="cutout height (fraction)")
    ap.add_argument("--preview", action="store_true", help="also write the 2:3 shelf crop")
    a = ap.parse_args()
    color = a.color or TEAM.get(a.team or "", "#1D428A")
    img = background(color).convert("RGBA")

    lines = a.title.replace("\\n", "\n").upper().split("\n")
    # cap height up to 300 px: measured titles are ~15 % of the shelf height per line
    f = fit_title(lines, W * 0.88, 300)
    cb = f.getbbox("H")
    cap = cb[3] - cb[1]
    pitch = int(cap * 1.1)
    y0 = int(H * 0.17)  # top of the first line's capitals
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    for i, ln in enumerate(lines):
        d.text((W // 2, y0 + i * pitch - cb[1]), ln, font=f, fill=(255, 255, 255, 255), anchor="ma")
    title_bottom = y0 + (len(lines) - 1) * pitch + cap
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow.putalpha(txt.getchannel("A").filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * 0.55)))
    img.alpha_composite(glow)
    img.alpha_composite(txt)

    p = Image.open(a.cutout).convert("RGBA")
    bb = p.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    p = p.crop(bb)
    th = int(H * a.height)
    p = p.resize((int(p.width * th / p.height), th), Image.LANCZOS)
    y = int(H * a.head) if a.head is not None else int(title_bottom - H * a.overlap)
    x = (W - p.width) // 2
    sh = Image.new("RGBA", p.size, (0, 0, 0, 0))
    sh.putalpha(p.getchannel("A").filter(ImageFilter.GaussianBlur(24)).point(lambda v: int(v * 0.5)))
    if x < 0:  # cutout wider than the frame: trim both sides evenly
        sh, p = sh.crop((-x, 0, p.width + x, p.height)), p.crop((-x, 0, p.width + x, p.height))
        x = 0
    img.alpha_composite(sh, (x, y + 12))
    img.alpha_composite(p, (x, y))
    # bottom fade so the cut at the chest is not a hard edge
    fade = Image.linear_gradient("L").resize((W, int(H * 0.18)))
    img.alpha_composite(Image.merge("RGBA", [Image.new("L", fade.size, int(v * 0.35)) for v in rgb(color)] + [fade]),
                        (0, H - fade.height))
    out = img.convert("RGB")
    out.save(a.out, quality=95)
    print("wrote", a.out, "bg", color, "title font", os.path.basename(f.path))
    if a.preview:
        top = (H - 1607) // 2
        pv = os.path.splitext(a.out)[0] + "_shelf.png"
        out.crop((0, top, W, top + 1607)).resize((418, 622), Image.LANCZOS).save(pv)
        print("wrote", pv)


if __name__ == "__main__":
    main()
