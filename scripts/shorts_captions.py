#!/usr/bin/env python3
"""Word-by-word "auto captions" for Shorts, in the reference channel's style.

Measured look (1080x1920): 1-2 words per caption, UPPERCASE, heavy geometric sans
(Montserrat ExtraBold), white, ~54 px, on a semi-transparent dark box with a soft shadow,
centred horizontally at ~63 % of the frame height (just under the face, above the
YouTube UI). Each caption pops in (80 % -> 100 % in 80 ms) and is replaced, never faded.

Input: word timestamps as JSON. Accepted shapes:
  * ElevenLabs speech_to_text output: {"words":[{"text","start","end","type"}...]}
  * faster-whisper / generic: [{"word" or "text", "start", "end"}, ...]
Get them from the finished VO (not from the script) so captions match what is heard:
  ElevenLabs MCP `speech_to_text` on vo.mp3, save the JSON.

Usage:
  python shorts_captions.py words.json caps.ass [--max-words 2] [--max-chars 14] [--y 0.63]
  python shorts_captions.py words.json caps.ass --burn in.mp4 out.mp4
Keywords (names, numbers) can be coloured: --hl "WARRIORS,BOOKER" --hl-color "#FFD400"
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shorts_common import CAPTION_FONTS, FONT_DIR, H, W, ffmpeg, find_font  # noqa: E402

PUNCT_BREAK = re.compile(r"[.,!?;:—]$")


def load_words(path):
    d = json.load(open(path, encoding="utf-8"))
    if isinstance(d, dict):
        d = d.get("words") or d.get("segments") or []
    out = []
    for w in d:
        if w.get("type", "word") != "word":
            continue
        txt = (w.get("text") or w.get("word") or "").strip()
        if txt:
            out.append((txt, float(w["start"]), float(w["end"])))
    if not out:
        raise SystemExit("no words found in " + path)
    return out


def chunk(words, max_words, max_chars):
    chunks, cur = [], []
    for w in words:
        cand = cur + [w]
        text = " ".join(x[0] for x in cand)
        if cur and (len(cand) > max_words or len(text) > max_chars):
            chunks.append(cur)
            cand = [w]
        cur = cand
        if PUNCT_BREAK.search(w[0]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    res = []
    for i, c in enumerate(chunks):
        start = c[0][1]
        end = chunks[i + 1][0][1] if i + 1 < len(chunks) else c[-1][2] + 0.25
        if end - c[-1][2] > 0.6:  # long pause: don't leave a stale word on screen
            end = c[-1][2] + 0.3
        text = " ".join(x[0] for x in c)
        text = re.sub(r"[\"“”]", "", text).strip(" ,.;:").upper()
        res.append((start, max(end, start + 0.12), text))
    return res


def ts(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def ass_color(hexs, alpha=0):
    h = hexs.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


def build_ass(chunks, y, size, hl, hl_color):
    font_path = find_font(CAPTION_FONTS)
    from PIL import ImageFont
    family = ImageFont.truetype(font_path, 20).getname()[0]
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{family},{size},{ass_color('#FFFFFF')},{ass_color('#FFFFFF')},{ass_color('#101010', 0x50)},{ass_color('#000000', 0x80)},-1,0,0,0,100,100,1,0,3,12,4,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    hlset = {w.strip().upper() for w in hl.split(",") if w.strip()}
    lines = []
    for s, e, text in chunks:
        words = []
        for w in text.split(" "):
            if w.strip(".,!?'") in hlset:
                words.append(r"{\c" + ass_color(hl_color) + "}" + w + r"{\c" + ass_color("#FFFFFF") + "}")
            else:
                words.append(w)
        pop = r"{\pos(%d,%d)\fscx80\fscy80\t(0,80,\fscx100\fscy100)}" % (W // 2, int(H * y))
        lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{pop}{' '.join(words)}")
    return head + "\n".join(lines) + "\n", font_path


def burn(ass_path, font_path, src, dst):
    # libass in this ffmpeg build has no fontconfig: point it at a folder holding the font.
    # Copy just the one font so libass does not scan all of C:\Windows\Fonts.
    import shutil
    fdir = os.path.join(os.path.dirname(os.path.abspath(ass_path)), "_capfont")
    os.makedirs(fdir, exist_ok=True)
    shutil.copy(font_path, fdir)

    def esc(p):
        return p.replace("\\", "/").replace(":", r"\:")

    vf = f"ass='{esc(os.path.abspath(ass_path))}':fontsdir='{esc(fdir)}'"
    cmd = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-vf", vf,
           "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "copy", dst]
    subprocess.run(cmd, check=True)
    print("burned", dst)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words")
    ap.add_argument("ass")
    ap.add_argument("--max-words", type=int, default=2)
    ap.add_argument("--max-chars", type=int, default=14)
    ap.add_argument("--y", type=float, default=0.63, help="caption centre, fraction of height")
    ap.add_argument("--size", type=int, default=54)
    ap.add_argument("--hl", default="", help="comma list of words to colour")
    ap.add_argument("--hl-color", default="#FFD400")
    ap.add_argument("--burn", nargs=2, metavar=("IN", "OUT"))
    a = ap.parse_args()
    chunks = chunk(load_words(a.words), a.max_words, a.max_chars)
    text, font_path = build_ass(chunks, a.y, a.size, a.hl, a.hl_color)
    open(a.ass, "w", encoding="utf-8").write(text)
    print(f"{len(chunks)} captions -> {a.ass}  (font {os.path.basename(font_path)})")
    if a.burn:
        burn(a.ass, font_path, *a.burn)


if __name__ == "__main__":
    main()
