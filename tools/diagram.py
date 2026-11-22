"""The architecture diagram: media/diagram-<en|tr>-<light|dark>.png

    python tools/diagram.py

Few boxes and big labels, so it stays legible when a phone shows it about 330 px wide
(labels land near 16 px). What each box does is written on the page under it, not in
the picture. Drawn at 900 px wide in IBM Plex Sans; the game room carries the accent.
One layout, labelled in English for the page's English part and in Turkish for its Turkish section.
"""
import json
import math
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "media" / "fonts"
ACCENT = json.loads((ROOT / "media" / "headings" / "headings.json").read_text(encoding="utf-8"))["accent"]

THEMES = {
    "light": {"bg": (255, 255, 255, 0), "box": "#f6f8fa", "edge": "#d0d7de", "text": "#1f2328", "line": "#8c959f"},
    "dark": {"bg": (13, 17, 23, 0), "box": "#161b22", "edge": "#30363d", "text": "#e6edf3", "line": "#6e7681"},
}

LABELS = {
    "en": {"projector": "Projector", "phones": "Phones", "panel": "Panel", "worker": "Worker",
           "room": "Game room", "gate": "Gate", "d1": "D1"},
    "tr": {"projector": "Projeksiyon", "phones": "Telefonlar", "panel": "Panel", "worker": "Worker",
           "room": "Oyun odası", "gate": "Kapı", "d1": "D1"},
}

W, H = 900, 760
BH = 120          # box height
R = 18            # corner radius
ROWS = [20, 220, 420, 620]


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def box(d, x0, y0, x1, label, t, font, accent=None):
    fill = t["box"]
    edge = accent or t["edge"]
    d.rounded_rectangle((x0, y0, x1, y0 + BH), R, fill=fill, outline=edge, width=5 if accent else 3)
    d.text(((x0 + x1) / 2, y0 + BH / 2), label, font=font, fill=accent or t["text"], anchor="mm")


def arrow(d, x0, y0, x1, y1, colour):
    d.line((x0, y0, x1, y1), fill=colour, width=5)
    # head pointing at (x1, y1)
    a = math.atan2(y1 - y0, x1 - x0)
    s = 22
    p1 = (x1 - s * math.cos(a - 0.45), y1 - s * math.sin(a - 0.45))
    p2 = (x1 - s * math.cos(a + 0.45), y1 - s * math.sin(a + 0.45))
    d.polygon([(x1, y1), p1, p2], fill=colour)


def main() -> None:
    font = ImageFont.truetype(str(FONTS / "IBMPlexSans-SemiBold.ttf"), 44)
    for (lang, lb), (theme, t) in ((a, b) for a in LABELS.items() for b in THEMES.items()):
        accent = ACCENT[theme]
        im = Image.new("RGBA", (W, H), t["bg"])
        d = ImageDraw.Draw(im)
        line = t["line"]
        # clients
        gap = 30
        cw = (W - 2 * 30 - 2 * gap) / 3
        xs = [(30 + i * (cw + gap), 30 + i * (cw + gap) + cw) for i in range(3)]
        for (x0, x1), label in zip(xs, [lb["projector"], lb["phones"], lb["panel"]]):
            box(d, x0, ROWS[0], x1, label, t, font)
            arrow(d, (x0 + x1) / 2, ROWS[0] + BH + 6, (x0 + x1) / 2 * 0.25 + W / 2 * 0.75, ROWS[1] - 8, line)
        # worker
        box(d, 150, ROWS[1], W - 150, lb["worker"], t, font)
        # durable objects
        left, right = (30, 410), (W - 410, W - 30)
        arrow(d, 330, ROWS[1] + BH + 6, (left[0] + left[1]) / 2, ROWS[2] - 8, line)
        arrow(d, W - 330, ROWS[1] + BH + 6, (right[0] + right[1]) / 2, ROWS[2] - 8, line)
        box(d, left[0], ROWS[2], left[1], lb["room"], t, font, accent=accent)
        box(d, right[0], ROWS[2], right[1], lb["gate"], t, font)
        # D1: results from the game room, quizzes from the worker
        arrow(d, (left[0] + left[1]) / 2, ROWS[2] + BH + 6, (left[0] + left[1]) / 2, ROWS[3] - 8, line)
        arrow(d, W / 2, ROWS[1] + BH + 6, W / 2, ROWS[3] - 8, line)
        box(d, 30, ROWS[3], W - 30, lb["d1"], t, font)
        out = ROOT / "media" / f"diagram-{lang}-{theme}.png"
        im.save(out, optimize=True)
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
