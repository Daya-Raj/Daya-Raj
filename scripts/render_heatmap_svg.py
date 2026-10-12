
from pathlib import Path
from datetime import date
import json
import html

DATA = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL = 11
GAP = 3
LEFT = 28
TOP = 30

def main():
    if not DATA.exists():
        raise SystemExit("Missing data/contributions.json")

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = payload.get("days", [])

    if not days:
        raise SystemExit("No contribution data available")

    days = days[-371:]
    first_day = date.fromisoformat(days[0]["date"])
    padding = (first_day.weekday() + 1) % 7
    days = [{"date": "", "level": 0, "count": 0}] * padding + days

    width = LEFT * 2 + 53 * (CELL + GAP)
    height = TOP + 7 * (CELL + GAP) + 28

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" rx="10" fill="#0d1117"/>',
        '<g font-family="monospace" font-size="10" fill="#8b949e">',
        '<text x="28" y="18">Less</text>'
    ]

    for i, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{width - 128 + i * 19}" y="8" '
            f'width="12" height="12" rx="2" fill="{color}"/>'
        )

    for i, day in enumerate(days):
        col, row = divmod(i, 7)
        x = LEFT + col * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        level = max(0, min(4, int(day.get("level", 0))))
        contribution_date = html.escape(day.get("date", ""))
        count = int(day.get("count", 0))

        parts.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="2" fill="{PALETTE[level]}" opacity="0">'
            f'<title>{count} contributions on {contribution_date}</title>'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{col * 0.018 + row * 0.012:.3f}s" '
            f'dur="0.18s" fill="freeze"/>'
            f'</rect>'
        )

    total = sum(int(day.get("count", 0)) for day in payload["days"])
    username = html.escape(payload.get("username", "Daya-Raj"))

    parts.append(
        f'<text x="{LEFT}" y="{height - 8}">'
        f'{total:,} contributions in fetched calendar · @{username}</text>'
    )
    parts.append("</g></svg>")

    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print("Created contrib-heatmap.svg successfully")

if __name__ == "__main__":
    main()
