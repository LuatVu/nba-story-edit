#!/usr/bin/env python3
"""Speed-ramp a footage clip for Shorts: normal speed for the action, slow motion for the
emotional beat, then back. Output is 9:16 (cover-cropped) with no audio (VO and music are
laid separately).

Usage:
  python shorts_speed.py in.mp4 out.mp4 "0-1.8:1, 1.8-3.2:0.35, 3.2-4.5:1"
  python shorts_speed.py in.mp4 out.mp4 "12.0-14.5:0.4" --smooth --x 0.62

Segments are SOURCE times "start-end:speed". speed 0.3-0.5 = slow-mo, 1 = normal,
1.5-2 = fast skip. Measured on the reference channel: the slow part is a dunk / celebration /
stare (~0.3-0.4x, 2-4 s on screen); play-by-play stays at 1x.
--smooth  motion-interpolates slow segments (minterpolate, slow to render). Without it,
          slow-mo duplicates frames: fine for 60 fps sources, juddery for 30 fps.
--x       horizontal centre of the 9:16 crop in the 16:9 source (0.5 = middle). Put the
          ball handler / subject in frame; split a clip into several calls if he moves a lot.
--zoom    extra punch-in (1.0 = none, 1.15 = 15 %).
"""
import argparse
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shorts_common import H, W, ffmpeg  # noqa: E402


def parse(segs):
    out = []
    for part in segs.split(","):
        rng, sp = part.strip().split(":")
        a, b = rng.split("-")
        out.append((float(a), float(b), float(sp)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("segments")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--smooth", action="store_true")
    ap.add_argument("--x", type=float, default=0.5)
    ap.add_argument("--zoom", type=float, default=1.0)
    a = ap.parse_args()
    segs = parse(a.segments)
    sh = int(H * a.zoom)
    sw = int(W * a.zoom)
    crop = (f"scale=-2:{sh},crop={sw}:{sh}:'min(max(0,iw*{a.x}-{sw}/2),iw-{sw})':0,"
            f"scale={W}:{H},setsar=1")
    parts = []
    tmp = tempfile.mkdtemp(prefix="speed_")
    for i, (s, e, sp) in enumerate(segs):
        f = [f"trim=start={s}:end={e}", "setpts=PTS-STARTPTS", crop]
        if sp != 1:
            f.append(f"setpts=PTS/{sp}")
        if a.smooth and sp < 0.8:
            f.append(f"minterpolate=fps={a.fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1")
        f.append(f"fps={a.fps}")
        p = os.path.join(tmp, f"p{i}.mp4")
        subprocess.run([ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-i", a.src,
                        "-vf", ",".join(f), "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", p],
                       check=True)
        parts.append(p)
        print(f"  {s:.2f}-{e:.2f}s @ {sp}x -> {(e - s) / sp:.2f}s on screen")
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p.replace(os.sep, '/')}'\n" for p in parts))
    subprocess.run([ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", a.out], check=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
