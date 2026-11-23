#!/usr/bin/env python3
"""Word timestamps from the finished VO, locally (faster-whisper), for shorts_captions.py
and for timing cutout entries in shorts_reveal.py.

The ElevenLabs MCP speech_to_text returns plain text only (no word times) and can only read
one configured folder, so this runs on the machine instead: free, nothing is uploaded.

  pip install faster-whisper          (one-off; first run downloads the model)
  python shorts_words.py vo.mp3 words.json [--model small.en] [--script script.txt]

--script  the text sent to TTS. Whisper's spelling of names is replaced word-for-word by the
          script's when the word count matches (Antetokounmpo, Jokić, numbers like 6'10").
Output: {"words":[{"text","start","end","type":"word"}...]}  (same shape as ElevenLabs STT)
"""
import argparse
import json
import re


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("out")
    ap.add_argument("--model", default="small.en", help="base.en is faster, small.en spells names better")
    ap.add_argument("--script")
    a = ap.parse_args()
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit("pip install faster-whisper")
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    # Decode with ffmpeg ourselves: faster-whisper's PyAV decoder breaks on av>=19.
    import os
    import subprocess
    import sys
    import numpy as np
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from shorts_common import ffmpeg
    pcm = subprocess.run([ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", a.audio, "-ac", "1",
                          "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    segs, _ = model.transcribe(audio, word_timestamps=True, language="en", vad_filter=False)
    words = [{"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "type": "word"}
             for s in segs for w in s.words if w.word.strip()]
    # whisper splits hyphenated / contracted words into two tokens ("8" "-0", "semi" "-final"):
    # glue a token that starts with - or ' back onto the previous one
    merged = []
    for w in words:
        if merged and w["text"][:1] in "-'’" and len(w["text"]) > 1:
            merged[-1]["text"] += w["text"]
            merged[-1]["end"] = w["end"]
        else:
            merged.append(w)
    words = merged
    if a.script:
        ref = re.findall(r"\S+", open(a.script, encoding="utf-8").read())
        if len(ref) == len(words):
            for w, r in zip(words, ref):
                w["text"] = r
            print("spelling taken from script")
        else:
            print(f"script has {len(ref)} words, whisper heard {len(words)}: kept whisper's spelling, check names")
    json.dump({"words": words}, open(a.out, "w", encoding="utf-8"), indent=1)
    print(f"{len(words)} words -> {a.out}  ({words[0]['start']:.2f}-{words[-1]['end']:.2f}s)")


if __name__ == "__main__":
    main()
