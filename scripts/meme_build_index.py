#!/usr/bin/env python3
"""Rebuild assets/memes/meme_index.json from assets/memes/catalog_raw.json + the tag files.

    python scripts/meme_build_index.py

Run after editing meme_semantics.py (CATS / CURATED / AUTO_RULES / SENSITIVE) or the
meme_extra_tags*.py files. Images live in assets/memes/templates/<imgflip id>.jpg|png
(compressed: long side <= 1200 px, JPEG q88; PNG only when the template has transparency).
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MEMES = os.path.join(os.path.dirname(HERE), "assets", "memes")
sys.path.insert(0, HERE)
from meme_semantics import CATS, CURATED, AUTO_RULES, is_sensitive  # noqa: E402
from meme_extra_tags import EXTRA_CATS  # noqa: E402
from meme_extra_tags2 import SENSITIVE_IDS, parse_all  # noqa: E402

CATS = {**CATS, **EXTRA_CATS}
EXTRA = parse_all()   # hand tags by id (ids = order of first appearance in catalog_raw.json)
FILES = {os.path.splitext(f)[0]: f for f in os.listdir(os.path.join(MEMES, "templates"))}

raw = json.load(open(os.path.join(MEMES, "catalog_raw.json"), encoding="utf-8"))
seen, out = set(), []
for rank, it in enumerate(raw):
    if it["slug"] in seen:
        continue
    seen.add(it["slug"])
    name = it["name"].replace("&#039;", "'").replace("&amp;", "&").replace("&quot;", '"')
    tail = it["slug"].rsplit("/", 1)[-1]
    stem = os.path.splitext(it["url"].rsplit("/", 1)[-1])[0]
    fn = FILES.get(stem)
    w = h = None
    if fn:
        with Image.open(os.path.join(MEMES, "templates", fn)) as im:
            w, h = im.size
    cur = CURATED.get(tail)
    if cur:
        cats, meaning, nba = cur[0].split(), cur[1], cur[2]
    else:
        low = name.lower()
        cats = {c for rx, c in AUTO_RULES if re.search(r"\b(?:" + rx + r")", low)}
        cats = sorted(cats | set(EXTRA.get(len(out), [])))
        meaning, nba = "", ""
    out.append({
        "id": len(out), "rank": rank, "name": name, "slug": it["slug"],
        "file": f"templates/{fn}" if fn else None, "url": it["url"],
        "imgflip_page": f"https://imgflip.com/meme/{it['slug']}",
        "w": w, "h": h, "cats": cats, "meaning": meaning, "nba_use": nba,
        "curated": bool(cur), "sensitive": is_sensitive(it["slug"], name) or len(out) in SENSITIVE_IDS,
    })

json.dump({"cats": {k: {"en": v[0], "vi": v[1]} for k, v in CATS.items()}, "memes": out},
          open(os.path.join(MEMES, "meme_index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(out)} memes | curated {sum(m['curated'] for m in out)} | with groups {sum(bool(m['cats']) for m in out)}"
      f" | sensitive {sum(m['sensitive'] for m in out)} | images {sum(m['file'] is not None for m in out)}")
