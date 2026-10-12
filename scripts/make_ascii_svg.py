
from pathlib import Path
from PIL import Image
import html

INPUT = Path("source-prepped.png")
OUTPUT = Path("daya-ascii.svg")
RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 92, 52
CELL_W, CELL_H = 8, 12

def main():
    if not INPUT.exists():
        raise SystemExit("Missing source-prepped.png")

    image = Image.open(INPUT).convert("L")
    image = image.resize((COLS, ROWS))
    pixels = list(image.getdata())

    lines = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            brightness = pixels[y * COLS + x]
            index = round((255 - brightness) / 255 * (len(RAMP) - 1))
            chars.append(RAMP[index])
        lines.append("".join(chars))

    width = COLS * CELL_W
    height = ROWS * CELL_H
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
        '<g font-family="monospace" font-size="10" xml:space="preserve" fill="#c9d1d9">'
    ]

    for y, line in enumerate(lines):
        parts.append(
            f'<text x="0" y="{(y + 1) * CELL_H - 2}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{y * 0.045:.3f}s" dur="0.12s" fill="freeze"/>'
            f'{html.escape(line)}</text>'
        )

    parts.extend(["</g>", "</svg>"])
    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print("Created daya-ascii.svg successfully")

if __name__ == "__main__":
    main()
