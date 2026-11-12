#!/usr/bin/env python3
"""
Tìm ảnh trên Wikimedia Commons, in kèm LICENSE và tác giả để chọn được ngay.

    commons_search.py "Jimmy Butler basketball" "Devin Booker"
    commons_search.py --by-only "Stephen Curry"      # chỉ CC BY / PD, bỏ ShareAlike
    commons_search.py --limit 15 "Nikola Jokic"

Chỉ dùng thư viện chuẩn, không cần cài gì.

Tải file gốc sau khi chọn:
    https://commons.wikimedia.org/wiki/Special:FilePath/<TÊN FILE>?width=2400

Vì sao cần --by-only: CC BY chỉ đòi ghi credit; CC BY-SA đòi thêm ShareAlike, kéo theo
nghĩa vụ cho cả video. Xem references/sources.md.
"""
import argparse, html, json, re, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA  = "nba-story-edit/1.0 (skill asset lookup; contact via channel owner)"
SHAREALIKE = re.compile(r"\bSA\b|ShareAlike", re.I)
FREEST     = re.compile(r"^(CC0|Public domain|CC BY [0-9.]+)$", re.I)


def api(params):
    """Gọi API, lịch sự với rate limit. 429 thì lùi dần rồi thử lại."""
    q = urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.load(r)
            time.sleep(2.5)            # tránh HTTP 429
            return data
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(8 * (attempt + 1))
    raise RuntimeError("unreachable")


def clean(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s or "")).strip()


def search(query, limit):
    d = api({"action": "query", "generator": "search",
             "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6,
             "gsrlimit": limit, "prop": "imageinfo",
             "iiprop": "url|size|extmetadata|mime"})
    rows = []
    for p in d.get("query", {}).get("pages", []):
        ii = (p.get("imageinfo") or [{}])[0]
        if not ii or ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        m = ii.get("extmetadata", {})
        g = lambda k: clean(m.get(k, {}).get("value", ""))
        rows.append({
            "title":  p["title"].replace("File:", ""),
            "lic":    g("LicenseShortName") or "?",
            "author": g("Artist") or "?",
            "date":   (g("DateTimeOriginal") or "")[:10],
            "w": ii.get("width", 0), "h": ii.get("height", 0),
            "page": ii.get("descriptionurl", ""),
        })
    rows.sort(key=lambda r: -(r["w"] * r["h"]))
    return rows


def filepath(name, width=2400):
    return ("https://commons.wikimedia.org/wiki/Special:FilePath/"
            + urllib.parse.quote(name) + f"?width={width}")


def main():
    ap = argparse.ArgumentParser(description="Tìm ảnh Wikimedia Commons kèm license")
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--limit", type=int, default=25, help="số kết quả mỗi từ khoá")
    ap.add_argument("--show", type=int, default=8, help="số dòng in ra mỗi từ khoá")
    ap.add_argument("--by-only", action="store_true",
                    help="chỉ giữ CC BY / CC0 / public domain, bỏ ShareAlike")
    ap.add_argument("--json", metavar="FILE", help="ghi toàn bộ kết quả ra JSON")
    a = ap.parse_args()

    out = {}
    for q in a.queries:
        rows = search(q, a.limit)
        if a.by_only:
            rows = [r for r in rows if FREEST.match(r["lic"])]
        out[q] = rows
        print(f"\n{'='*96}\n>>> {q}" + ("   [chỉ CC BY / PD]" if a.by_only else ""))
        if not rows:
            print("  (không có kết quả)")
            continue
        for r in rows[:a.show]:
            warn = "  ⚠ SA" if SHAREALIKE.search(r["lic"]) else ""
            print(f"  {r['w']}x{r['h']:<6}{r['lic']:<17}{r['date']:<11}{r['title'][:50]}{warn}")
            print(f"      {r['author'][:66]}")
            print(f"      {filepath(r['title'])}")
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1, ensure_ascii=False)
        print(f"\n→ {a.json}")
    print("\nNhớ: mọi ảnh Commons đều PHẢI ghi credit. Khối credit mẫu ở references/sources.md.")


if __name__ == "__main__":
    main()
