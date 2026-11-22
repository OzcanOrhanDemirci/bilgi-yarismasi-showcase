"""The still screens: media/screens/<name>-<en|tr>.webp, from shots of two local runs of the app.

    python tools/screens.py

The shots sit in yerel/en/shots (English run) and yerel/shots (Turkish run), gitignored;
UPDATING.md says how they were taken. Each set is built for each language:
  lobby    the projector's lobby, 1920x1080 scaled to 1280 wide
  phones   three phone screens side by side
  panel    the staff panel on a phone (editor, results) and the PDF result sheet
Portrait screens get rounded corners and a thin grey edge on a transparent ground,
so one file reads on GitHub's light and dark themes.
"""
import pathlib

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = {"en": ROOT / "yerel" / "en" / "shots", "tr": ROOT / "yerel" / "shots"}
OUT = ROOT / "media" / "screens"
EDGE = (140, 149, 159, 255)

GROUPS = {
    "phones": ["telefon-1-pin.png", "telefon-5-cevap.png", "telefon-7-dogru.png"],
    "panel": ["panel-tel-duzenleyici-2.png", "panel-tel-sonuc.png", "pdf-1.png"],
}
H = 1000      # height of each screen in a group
GAP = 40


def framed(im: Image.Image, h: int) -> Image.Image:
    im = im.convert("RGB")
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    r = round(h * 0.035)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, w - 1, h - 1), r, outline=EDGE, width=3)
    return out


def load(shots, entry):
    name, crop = (entry, None) if isinstance(entry, str) else entry
    im = Image.open(shots / name)
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    return im


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, shots in SHOTS.items():
        build(lang, shots)
    for f in sorted(OUT.iterdir()):
        print(f.relative_to(ROOT), f"{f.stat().st_size // 1024} KB")


def build(lang: str, shots: pathlib.Path) -> None:
    lobby = Image.open(shots / "sunucu-2-lobi.png").convert("RGB").resize((1280, 720), Image.LANCZOS)
    rr = Image.new("L", lobby.size, 0)
    ImageDraw.Draw(rr).rounded_rectangle((0, 0, 1279, 719), 22, fill=255)
    lob = Image.new("RGBA", lobby.size, (0, 0, 0, 0))
    lob.paste(lobby, (0, 0), rr)
    lob.save(OUT / f"lobby-{lang}.webp", quality=88, method=6)
    for name, files in GROUPS.items():
        tiles = [framed(load(shots, f), H) for f in files]
        w = sum(t.width for t in tiles) + GAP * (len(tiles) - 1)
        sheet = Image.new("RGBA", (w, H), (0, 0, 0, 0))
        x = 0
        for t in tiles:
            sheet.alpha_composite(t, (x, 0))
            x += t.width + GAP
        sheet.save(OUT / f"{name}-{lang}.webp", quality=88, method=6)


if __name__ == "__main__":
    main()
