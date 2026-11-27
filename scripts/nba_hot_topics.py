"""Daily NBA hot-topic radar for Turn On Hoops meme posts (ESPN public JSON, no key).

    python scripts/nba_hot_topics.py                 # yesterday's results (US date) + latest news
    python scripts/nba_hot_topics.py --date 20261126 --news 25
    python scripts/nba_hot_topics.py --json > hot.json

Scores each game/news item by what drives engagement on a US NBA meme page:
big-market / big-fanbase teams, star names, extreme stat lines, blowouts, upsets, OT,
injuries, trades/rumors, drama words. The list is a starting point: always confirm the
story (and that it is still fresh) with a web search before writing the post.
"""
import sys as _sys
_sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import argparse, datetime as dt, json, re, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
# Fanbase / social reach weight (rough, US + global). Tune as the season goes.
TEAM_W = {"LAL": 3.0, "GS": 2.8, "BOS": 2.5, "NY": 2.5, "CHI": 2.0, "MIA": 2.0, "DAL": 2.0,
          "PHI": 1.8, "CLE": 1.6, "OKC": 1.8, "DEN": 1.7, "MIL": 1.5, "PHX": 1.5, "SA": 1.8,
          "HOU": 1.5, "MIN": 1.4, "BKN": 1.3, "LAC": 1.3, "TOR": 1.2, "ORL": 1.2, "IND": 1.2,
          "SAC": 1.0, "ATL": 1.1, "MEM": 1.1, "NO": 1.0, "DET": 1.2, "POR": 1.0, "UTAH": 0.9,
          "CHA": 0.9, "WSH": 0.9}
HOT_WORDS = {
    r"\btrade|traded|deal|acquire|rumor|request": 3, r"injur|out for|surgery|torn|sprain|questionable": 2,
    r"fine|suspend|ejected|technical|fight|altercation|scuffle": 3, r"record|career-high|history|first time|triple-double|50|60": 2,
    r"benched|demoted|feud|criticize|blast|rips|calls out|slams|beef|drama": 3, r"mvp|goat|all-star|contract|max|extension": 2,
    r"fired|hire|coach": 2, r"buzzer|game-winner|overtime|comeback": 2, r"lebron|curry|luka|wembanyama|giannis|jokic|durant|shai|tatum|edwards|morant|embiid|bronny": 2,
}


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))


def word_score(text):
    t = text.lower()
    return sum(w for rx, w in HOT_WORDS.items() if re.search(rx, t))


def games(date):
    d = get(f"{BASE}/scoreboard?dates={date}")
    out = []
    for e in d.get("events", []):
        c = e["competitions"][0]
        if e["status"]["type"]["state"] != "post":
            continue
        tm = {x["homeAway"]: x for x in c["competitors"]}
        h, a = tm["home"], tm["away"]
        hs, as_ = int(h["score"]), int(a["score"])
        win, lose = (h, a) if hs > as_ else (a, h)
        margin = abs(hs - as_)
        abbr = [h["team"]["abbreviation"], a["team"]["abbreviation"]]
        score = sum(TEAM_W.get(x, 1) for x in abbr)
        notes = []
        if margin >= 25: score += 2; notes.append(f"blowout +{margin}")
        if margin <= 3: score += 1.5; notes.append("close game")
        if "OT" in e["status"]["type"]["shortDetail"]: score += 1.5; notes.append("overtime")
        try:
            if float(win["records"][0]["summary"].split("-")[0]) < float(lose["records"][0]["summary"].split("-")[0]) - 4:
                score += 2; notes.append("upset")
        except Exception:
            pass
        leaders = []
        for x in c["competitors"]:
            for L in x.get("leaders", []):
                if L["name"] in ("points", "rebounds", "assists") and L.get("leaders"):
                    top = L["leaders"][0]
                    v = float(top["value"])
                    leaders.append(f"{top['athlete']['displayName']} ({x['team']['abbreviation']}) {int(v)} {L['abbreviation']}")
                    if (L["name"] == "points" and v >= 40) or (L["name"] != "points" and v >= 18):
                        score += 2.5; notes.append(f"big line: {top['athlete']['shortName']} {int(v)} {L['abbreviation']}")
                    if word_score(top["athlete"]["displayName"]):
                        score += 1
        out.append({"type": "game", "score": round(score, 1),
                    "title": f"{a['team']['abbreviation']} {as_} @ {h['team']['abbreviation']} {hs} ({e['status']['type']['shortDetail']})",
                    "notes": notes, "leaders": leaders})
    return out


def news(n):
    d = get(f"{BASE}/news?limit={n}")
    out = []
    for a in d.get("articles", []):
        text = a["headline"] + " " + a.get("description", "")
        teams = [c.get("description", "") for c in a.get("categories", []) if c.get("type") == "team"]
        s = word_score(text) + 0.5 * len(teams)
        if re.search(r"visit|host|meet|take on", a["headline"].lower()) and s < 2:
            s -= 2  # generic previews
        out.append({"type": "news", "score": round(s, 1), "title": a["headline"],
                    "notes": [a.get("published", "")[:16], ", ".join(teams)], "link": a.get("links", {}).get("web", {}).get("href", "")})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYYMMDD (US). Default: yesterday in US Eastern time")
    ap.add_argument("--news", type=int, default=20)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    date = a.date or (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=5) - dt.timedelta(days=1)).strftime("%Y%m%d")
    items = sorted(games(date) + news(a.news), key=lambda x: -x["score"])
    if a.json:
        print(json.dumps(items, ensure_ascii=False, indent=1))
    else:
        print(f"== Hot topics (games {date} + latest ESPN news) ==")
        for it in items:
            print(f"{it['score']:5.1f} [{it['type']}] {it['title']}")
            if it.get("notes"): print("        " + " | ".join(x for x in it["notes"] if x))
            if it.get("leaders"): print("        " + "; ".join(it["leaders"]))
