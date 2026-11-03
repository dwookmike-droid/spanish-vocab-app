"""Contact sheets for picking word photos: one PNG per 5 words, each row = one word's Commons candidates.

Usage: python3 claude_design/tools/cand_sheets.py claude_design/chNN
Writes claude_design/chNN/cand/sheet_K.png (K = 0, 1, ...). Row label: word key + Spanish word; cell label: index.
"""
import json
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

CELL, LABEL_W, PAD = 200, 190, 6


def main(d):
    d = Path(d)
    nn = d.name[2:]
    root = d.parents[1]
    words = yaml.safe_load((root / f"es/ch{nn}/text/ch{nn}_text.yaml").read_text(encoding="utf-8"))["words"]
    meta = json.loads((d / "cand/meta.json").read_text(encoding="utf-8"))
    try:
        font = ImageFont.truetype(str(root / "claude_design/fonts/Pretendard-Bold.ttf"), 18)
        small = ImageFont.truetype(str(root / "claude_design/fonts/Pretendard-Bold.ttf"), 15)
    except OSError:
        font = small = ImageFont.load_default()
    cols = max((len(v) for v in meta.values()), default=1) or 1
    for s in range(0, len(words), 5):
        chunk = words[s:s + 5]
        sheet = Image.new("RGB", (LABEL_W + cols * (CELL + PAD), len(chunk) * (CELL + PAD)), "white")
        dr = ImageDraw.Draw(sheet)
        for r, w in enumerate(chunk):
            y = r * (CELL + PAD)
            dr.text((8, y + 70), w["key"], fill="black", font=font)
            dr.text((8, y + 98), f"{w['es']}", fill="#a4533a", font=small)
            dr.text((8, y + 120), f"{w['en']}", fill="#555", font=small)
            for c, cand in enumerate(meta.get(w["key"], [])):
                try:
                    im = Image.open(cand["file"] if Path(cand["file"]).exists() else d / "cand" / Path(cand["file"]).name).convert("RGB")
                except OSError:
                    continue
                im.thumbnail((CELL, CELL))
                x = LABEL_W + c * (CELL + PAD)
                sheet.paste(im, (x + (CELL - im.width) // 2, y + (CELL - im.height) // 2))
                dr.rectangle([x, y, x + 26, y + 24], fill="black")
                dr.text((x + 7, y + 2), str(c), fill="white", font=font)
        out = d / f"cand/sheet_{s // 5}.png"
        sheet.save(out)
        print(out)


if __name__ == "__main__":
    main(sys.argv[1])
