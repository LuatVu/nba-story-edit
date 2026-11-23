#!/usr/bin/env python3
"""Cut a player out of a photo -> PNG with transparent background, trimmed and edge-softened.

Needs rembg (one-off):  pip install "rembg[cpu]"
The first run downloads the model (~170 MB) into ~/.u2net.

Usage:
  python shorts_cutout.py photo.jpg out.png
  python shorts_cutout.py photo.jpg out.png --model isnet-general-use --crop 0.1,0,0.7,1
  python shorts_cutout.py *.jpg --outdir cutouts/

--crop l,t,r,b  (fractions) crop the photo to ONE player before removing the background.
                Group photos confuse the model: always isolate the player you want.
--model         u2net_human_seg (default, people) | isnet-general-use (sharper edges,
                keeps the ball) | birefnet-portrait (best hair, slower).
Check the result on a contrasting colour (--check writes out_check.png on magenta):
jersey numbers, hands and the ball are where the mask fails most.
"""
import argparse
import os
import sys

from PIL import Image, ImageFilter


def largest_blob(alpha, keep_ratio=0.2):
    """Zero every connected region smaller than keep_ratio x the largest one."""
    import numpy as np
    from scipy import ndimage
    a = np.asarray(alpha)
    lab, n = ndimage.label(a > 128)
    if n <= 1:
        return alpha
    sizes = ndimage.sum(np.ones_like(a), lab, range(1, n + 1))
    keep = np.isin(lab, 1 + np.flatnonzero(sizes >= sizes.max() * keep_ratio))
    keep = ndimage.binary_dilation(keep, iterations=3)  # keep the soft edge around kept regions
    return Image.fromarray(np.where(keep, a, 0).astype("uint8"), "L")


def fill_holes(alpha):
    """Close holes fully enclosed by the body: the model often drops jersey logos, flags and
    sponsor patches (seen on a Nike swoosh and the US flag of a Team USA jersey)."""
    import numpy as np
    from scipy import ndimage
    a = np.asarray(alpha)
    filled = ndimage.binary_fill_holes(a > 128)
    return Image.fromarray(np.where(filled & (a <= 128), 255, a).astype("uint8"), "L")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--outdir")
    ap.add_argument("--model", default="u2net_human_seg")
    ap.add_argument("--crop")
    ap.add_argument("--feather", type=float, default=1.2, help="edge blur px")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--keep-islands", action="store_true",
                    help="keep every masked region (default keeps the main body only: drops stray "
                         "hands, specks and other players' limbs at the crop edge)")
    a = ap.parse_args()
    try:
        from rembg import new_session, remove
    except ImportError:
        sys.exit('rembg is not installed. Run:  pip install "rembg[cpu]"')
    if a.outdir:
        os.makedirs(a.outdir, exist_ok=True)
        pairs = [(p, os.path.join(a.outdir, os.path.splitext(os.path.basename(p))[0] + ".png")) for p in a.inputs]
    elif len(a.inputs) == 2 and a.inputs[1].lower().endswith(".png"):
        pairs = [(a.inputs[0], a.inputs[1])]
    else:
        sys.exit("give `in out.png` or `--outdir DIR`")
    sess = new_session(a.model)
    for src, dst in pairs:
        im = Image.open(src).convert("RGB")
        if a.crop:
            l, t, r, b = (float(v) for v in a.crop.split(","))
            im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
        out = remove(im, session=sess, post_process_mask=True)
        alpha = out.getchannel("A")
        if not a.keep_islands:
            alpha = largest_blob(alpha)
        alpha = fill_holes(alpha)
        out = im.convert("RGBA")  # rembg blanks the colour under dropped pixels: take it from the photo
        if a.feather:
            alpha = alpha.filter(ImageFilter.GaussianBlur(a.feather))
        out.putalpha(alpha)
        bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb:
            out = out.crop(bb)
        out.save(dst)
        warn = "  ! under 1000 px tall: will look soft at full-frame size, crop a larger photo" \
            if out.size[1] < 1000 else ""
        print(f"{src} -> {dst}  {out.size[0]}x{out.size[1]}{warn}")
        if a.check:
            bg = Image.new("RGBA", out.size, (255, 0, 255, 255))
            bg.alpha_composite(out)
            bg.convert("RGB").save(os.path.splitext(dst)[0] + "_check.png")


if __name__ == "__main__":
    main()
