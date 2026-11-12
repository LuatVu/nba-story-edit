#!/usr/bin/env python3
"""
Sinh biểu đồ theo style SOFA Zone (nền đen, chữ trắng, accent cam).

    make_chart.py --mode dumbbell --csv salaries.csv --title "..." --tall
    make_chart.py --mode bars     --csv cap.csv      --title "..." --video
    make_chart.py --mode line     --csv payroll.csv  --title "..."

CSV:
  dumbbell : label,<tênA>,<tênB>      -> hai chấm nối nhau, so sánh 2 kỳ
  bars     : label,value
  line     : x,<series1>[,<series2>...]

Cần: pip install matplotlib        (video cần thêm ffmpeg trong PATH)
"""
import argparse, csv, os, sys

BG      = "#000000"
FG      = "#FFFFFF"
MUTED   = "#9A9A9A"
GRID    = "#2A2A2A"
ACCENT  = "#E8912A"

TITLE_FONTS = ["Archivo", "Inter", "Helvetica Neue", "DejaVu Sans"]
BODY_FONTS  = ["Inter", "Helvetica Neue", "DejaVu Sans"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        sys.exit("CSV rỗng")
    return rows[0], rows[1:]


def num(s):
    s = str(s).strip().replace(",", "").replace("$", "").replace("%", "")
    if s.endswith(("M", "m")):
        return float(s[:-1]) * 1e6
    if s.endswith(("K", "k")):
        return float(s[:-1]) * 1e3
    return float(s)


def fmt(v):
    a = abs(v)
    if a >= 1e9:  return f"{v/1e9:.2f}B"
    if a >= 1e6:  return (f"{v/1e6:.0f}M" if a >= 1e8 else f"{v/1e6:.1f}M")
    if a >= 1e3:  return f"{v/1e3:.0f}K"
    if a == int(a): return f"{int(v)}"
    return f"{v:.1f}"


def center_rows(ax, n, span_min=9):
    """Giữ độ dày dòng ổn định dù chỉ có vài dòng: canh giữa trong khung span_min dòng."""
    span = max(n, span_min)
    pad = (span - n) / 2.0
    ax.set_ylim(-0.6 - pad, n - 0.4 + pad)


def whiten_yticks(ax):
    for t in ax.get_yticklabels():
        t.set_color(FG)


def style_axes(ax, xgrid=True, ygrid=False):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=15, length=0)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=1)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, lw=1)
    ax.set_axisbelow(True)


def header(fig, title, subtitle, legend_pairs, source):
    fig.text(0.055, 0.966, title, color=FG, fontsize=34, fontweight="600",
             va="top", ha="left", family=TITLE_FONTS)
    y = 0.966 - (68 / fig.get_size_inches()[1] / 100)
    if subtitle:
        fig.text(0.055, y, subtitle, color=MUTED, fontsize=19,
                 va="top", ha="left", family=BODY_FONTS)
        y -= 46 / fig.get_size_inches()[1] / 100
    if legend_pairs:
        x = 0.055
        for name, color in legend_pairs:
            fig.text(x, y, "●", color=color, fontsize=17, va="top", ha="left")
            fig.text(x + 0.018, y, name, color=FG, fontsize=17, va="top",
                     ha="left", family=BODY_FONTS)
            x += 0.018 + 0.011 * len(name) + 0.028
    if source:
        fig.text(0.962, 0.022, source, color=MUTED, fontsize=14,
                 va="bottom", ha="right", family=BODY_FONTS)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", required=True, choices=["dumbbell", "bars", "line"])
    p.add_argument("--csv", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--source", default="", help='vd "Spotrac · 09.11.2026"')
    p.add_argument("--out", default="chart.png")
    p.add_argument("--accent", default=ACCENT)
    p.add_argument("--tall", action="store_true",
                   help="PNG cao để scroll dọc trong Premiere")
    p.add_argument("--video", action="store_true", help="xuất MP4 có animation")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--duration", type=float, default=4.0)
    p.add_argument("--slice", default="", help="vd 0:12 -> chỉ lấy 12 dòng đầu")
    a = p.parse_args()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        sys.exit("Thiếu matplotlib.  Chạy:  pip install matplotlib")

    head, rows = load(a.csv)
    if a.slice:
        i, j = (int(x) if x else None for x in a.slice.split(":"))
        rows = rows[i:j]
    if not rows:
        sys.exit("Không còn dòng nào sau --slice")

    accent = a.accent
    plt.rcParams["savefig.facecolor"] = BG
    plt.rcParams["figure.facecolor"] = BG

    W_IN = 19.2

    # ---------------- dumbbell ----------------
    if a.mode == "dumbbell":
        if len(head) < 3:
            sys.exit("dumbbell cần 3 cột: label,A,B")
        labels = [r[0] for r in rows]
        A = [num(r[1]) for r in rows]
        B = [num(r[2]) for r in rows]
        n = len(rows)
        h_in = (0.52 * n + 3.2) if a.tall else 10.8
        fig, ax = plt.subplots(figsize=(W_IN, h_in))
        y = list(range(n))[::-1]
        for yi, av, bv in zip(y, A, B):
            ax.plot([av, bv], [yi, yi], color=accent, lw=3, zorder=1,
                    solid_capstyle="round")
        ax.scatter(A, y, s=190, color=FG, zorder=3, edgecolors=BG, linewidths=2)
        ax.scatter(B, y, s=190, color=accent, zorder=3, edgecolors=BG, linewidths=2)
        ax.set_yticks(y); ax.set_yticklabels(labels, color=FG, fontsize=17,
                                             fontfamily=BODY_FONTS)
        ax.set_xticklabels([fmt(t) for t in ax.get_xticks()])
        style_axes(ax, xgrid=True)
        whiten_yticks(ax)
        center_rows(ax, n, span_min=9 if not a.tall else n)
        fig.subplots_adjust(left=0.20, right=0.965,
                            top=1 - (1.15 / h_in), bottom=0.9 / h_in)
        header(fig, a.title, a.subtitle,
               [(head[1], FG), (head[2], accent)], a.source)

    # ---------------- bars ----------------
    elif a.mode == "bars":
        labels = [r[0] for r in rows]
        vals = [num(r[1]) for r in rows]
        n = len(rows)
        h_in = (0.52 * n + 3.2) if a.tall else 10.8
        fig, ax = plt.subplots(figsize=(W_IN, h_in))
        y = list(range(n))[::-1]
        bars = ax.barh(y, vals, height=0.56, color=accent)
        texts = [ax.text(v + max(vals) * 0.018, yi, fmt(v), color=FG, fontsize=16,
                         va="center", fontfamily=BODY_FONTS)
                 for v, yi in zip(vals, y)]
        ax.set_yticks(y); ax.set_yticklabels(labels, color=FG, fontsize=17,
                                             fontfamily=BODY_FONTS)
        ax.set_xticks([])
        style_axes(ax, xgrid=False)
        whiten_yticks(ax)
        ax.set_xlim(0, max(vals) * 1.17)
        center_rows(ax, n, span_min=9 if not a.tall else n)
        fig.subplots_adjust(left=0.20, right=0.965,
                            top=1 - (1.15 / h_in), bottom=0.9 / h_in)
        header(fig, a.title, a.subtitle, [], a.source)

        if a.video:
            from matplotlib.animation import FuncAnimation, FFMpegWriter
            frames = int(a.fps * a.duration)

            def upd(k):
                t = min(1.0, (k + 1) / frames)
                e = 1 - (1 - t) ** 3           # ease-out cubic
                for b, v, tx in zip(bars, vals, texts):
                    b.set_width(v * e)
                    tx.set_x(v * e + max(vals) * 0.018)
                    tx.set_text(fmt(v * e))
                return list(bars) + texts

            out = a.out if a.out.endswith(".mp4") else os.path.splitext(a.out)[0] + ".mp4"
            FuncAnimation(fig, upd, frames=frames, blit=False).save(
                out, writer=FFMpegWriter(fps=a.fps, bitrate=16000,
                                         extra_args=["-pix_fmt", "yuv420p"]))
            print(out); return

    # ---------------- line ----------------
    else:
        xs = [r[0] for r in rows]
        series = []
        for ci in range(1, len(head)):
            series.append((head[ci], [num(r[ci]) for r in rows]))
        fig, ax = plt.subplots(figsize=(W_IN, 10.8))
        colors = [accent, FG, MUTED]
        for i, (name, vals) in enumerate(series):
            ax.plot(range(len(xs)), vals, lw=3.5,
                    color=colors[i % len(colors)], solid_capstyle="round")
        ax.set_xticks(range(len(xs)))
        ax.set_xticklabels(xs, color=MUTED, fontsize=15, fontfamily=BODY_FONTS)
        ax.set_yticklabels([fmt(t) for t in ax.get_yticks()])
        style_axes(ax, xgrid=False, ygrid=True)
        fig.subplots_adjust(left=0.085, right=0.965, top=0.845, bottom=0.085)
        header(fig, a.title, a.subtitle,
               [(nm, colors[i % len(colors)]) for i, (nm, _) in enumerate(series)],
               a.source)

    out = a.out if a.out.endswith(".png") else a.out + ".png"
    fig.savefig(out, dpi=100, facecolor=BG)
    print(out)


if __name__ == "__main__":
    main()
