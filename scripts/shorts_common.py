"""Shared helpers for the Shorts scripts: ffmpeg path, fonts, easing, frame piping."""
import os
import shutil
import subprocess

from PIL import ImageFont

W, H = 1080, 1920
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(SKILL, "assets", "fonts")
WINFONTS = r"C:\Windows\Fonts"

# Preferred font first; Windows fallbacks that look close enough.
CAPTION_FONTS = ["Montserrat-ExtraBold.ttf", "Montserrat-Black.ttf", "seguibl.ttf", "ariblk.ttf"]
TITLE_FONTS = ["Anton-Regular.ttf", "BebasNeue-Regular.ttf", "impact.ttf", "ariblk.ttf"]


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit("ffmpeg not found: put it in PATH or `pip install imageio-ffmpeg`")


def find_font(candidates):
    for name in candidates:
        for d in (FONT_DIR, WINFONTS):
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    raise SystemExit(f"No font found among {candidates}; drop one into {FONT_DIR}")


def font(candidates, size):
    return ImageFont.truetype(find_font(candidates), size)


def clamp01(x):
    return max(0.0, min(1.0, x))


def ease_out(x):  # cubic
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_out_back(x, s=1.6):  # small overshoot, for "pop"
    x = clamp01(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def ease_in_out(x):
    x = clamp01(x)
    return 3 * x * x - 2 * x * x * x


def open_writer(out, fps, w=W, h=H, crf=18):
    """Return a Popen whose stdin takes raw RGB frames."""
    cmd = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", out]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def read_video_frames(path, fps, w=W, h=H):
    """Yield RGB frames (bytes) of a video, cover-cropped to w x h."""
    vf = f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    p = subprocess.Popen([ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", path,
                          "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield b
    p.wait()
