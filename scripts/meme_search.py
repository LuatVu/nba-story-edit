"""Find meme templates by meaning, from a Vietnamese or English prompt.

    python scripts/meme_search.py "cầu thủ đòi trade nhưng không ai muốn"
    python scripts/meme_search.py "superteam plan fails" --top 12 --sheet pick.jpg
    python scripts/meme_search.py --cat no_trophy --top 20
    python scripts/meme_search.py --list-cats
    python scripts/meme_search.py --name "drake"

Prints: score, name, groups, meaning / NBA use, file path. --sheet builds a labelled contact
sheet so the template can be picked by eye. Sensitive templates (9/11, race, drugs, politics,
religion, adult) are hidden unless --allow-sensitive.
"""
import sys as _sys
_sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import argparse, json, os, re, unicodedata
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "memes")  # skill/assets/memes
IDX = json.load(open(os.path.join(HERE, "meme_index.json"), encoding="utf-8"))


def norm(s):
    s = unicodedata.normalize("NFD", s.lower()).replace("đ", "d")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def grams(text):
    w = norm(text).split()
    return set(w) | {" ".join(w[i:i + 2]) for i in range(len(w) - 1)}


STOP = set("the a an of to in is it and or for on with my your his her their x y he she they team player players".split())
# Vietnamese syllables that are too common / ambiguous on their own (only count inside a 2-word phrase):
# e.g. "đồng" in "đồng đội" must not hit alliance via "đồng minh".
STOP |= set(("la cua va cho khi thi nhung mot cac duoc co khong bi lam ra di ve len xuong tran the nay do voi trong "
             "ngoai hon nhat rat qua lai van con da se dang cung nhu de tu theo sau truoc gi ai nao sao ban toi minh "
             "anh em hay ma nen vi neu hoac ca moi doi dong cau thu mua choi nguoi vien tro ngay nam lan dau cuoi "
             "het moi tat ca nhieu it so diem tren duoi giua").split())
CAT_GRAMS = {k: grams(v["en"] + " " + v["vi"]) for k, v in IDX["cats"].items()}


def cat_scores(q):
    qg = {g for g in grams(q) if g not in STOP and len(g) > 1}
    sc = {}
    for k, cg in CAT_GRAMS.items():
        hit = qg & cg
        if hit:
            bi = {g for g in hit if " " in g}
            covered = {w for g in bi for w in g.split()}  # a matched phrase is not counted again word by word
            uni = {g for g in hit if " " not in g and g not in covered}
            sc[k] = 2 * len(bi) + len(uni) + (2 if norm(k.replace("_", " ")) in norm(q) else 0)
    return sc, qg


def search(q, top=10, cat=None, allow_sensitive=False, name=None):
    memes = [m for m in IDX["memes"] if allow_sensitive or not m["sensitive"]]
    n = len(IDX["memes"])
    if name:
        nn = norm(name)
        return [(1.0, m) for m in memes if nn in norm(m["name"])][:top]
    if cat:
        return [(1.0, m) for m in sorted(memes, key=lambda m: (not m["curated"], m["rank"])) if cat in m["cats"]][:top]
    cs, qg = cat_scores(q)
    res = []
    for m in memes:
        s = sum(cs.get(c, 0) * (3 if m["curated"] else 2) for c in m["cats"])
        text = grams(m["name"] + " " + m["meaning"] + " " + m["nba_use"])
        s += 1.5 * len({g for g in qg & text if len(g) > 2})
        if s <= 0:
            continue
        s += (3.0 if m["curated"] else 0) + 2 * (1 - m["rank"] / n)
        res.append((round(s, 2), m))
    res.sort(key=lambda t: -t[0])
    return res[:top]


def sheet(results, out, cell=300):
    cols = min(4, max(1, len(results)))
    rows = (len(results) + cols - 1) // cols
    S = Image.new("RGB", (cols * cell, rows * (cell + 54)), (24, 24, 28))
    d = ImageDraw.Draw(S)
    try:
        f = ImageFont.truetype("arialbd.ttf", 15)
    except OSError:
        f = ImageFont.load_default()
    for i, (_, m) in enumerate(results):
        x, y = (i % cols) * cell, (i // cols) * (cell + 54)
        p = os.path.join(HERE, m["file"])
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((cell - 10, cell - 10))
            S.paste(im, (x + (cell - im.width) // 2, y + 5 + (cell - 10 - im.height) // 2))
        except Exception:
            d.text((x + 10, y + cell // 2), "(no image)", font=f, fill=(200, 80, 80))
        d.text((x + 6, y + cell + 2), f"#{m['id']} {m['name'][:34]}", font=f, fill=(255, 210, 60))
        d.text((x + 6, y + cell + 22), " ".join(m["cats"])[:40], font=f, fill=(190, 190, 200))
    S.save(out, quality=88)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--cat")
    ap.add_argument("--name")
    ap.add_argument("--sheet")
    ap.add_argument("--allow-sensitive", action="store_true")
    ap.add_argument("--list-cats", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.list_cats:
        from collections import Counter
        cnt = Counter(c for m in IDX["memes"] for c in m["cats"])
        for k, v in IDX["cats"].items():
            print(f"{k:20s} {cnt[k]:4d}  {v['vi'][:70]}")
        raise SystemExit
    if a.query:
        cs, _ = cat_scores(a.query)
        print("groups:", ", ".join(f"{k}:{v}" for k, v in sorted(cs.items(), key=lambda t: -t[1])) or "-")
    res = search(a.query, a.top, a.cat, a.allow_sensitive, a.name)
    if a.json:
        print(json.dumps([dict(m, score=s, path=os.path.join(HERE, m["file"])) for s, m in res], ensure_ascii=False, indent=1))
    else:
        for s, m in res:
            print(f"{s:5.1f}  #{m['id']:<5} {m['name']}  [{' '.join(m['cats'])}]  {m['w']}x{m['h']}")
            if m["meaning"]:
                print(f"        meaning: {m['meaning']}\n        NBA: {m['nba_use']}")
            print(f"        {os.path.join(HERE, m['file'])}")
    if a.sheet and res:
        print("sheet:", sheet(res, a.sheet))
