
from pathlib import Path
import os
import html

OUTPUT = Path("info-card.svg")
STATIC = os.getenv("STATIC") == "1"

ROWS = [
    ("NAME", "Daya Raj"),
    ("ROLE", "Developer / AI-ML Explorer"),
    ("LANG", "Java / Python / JavaScript"),
    ("WEB", "HTML / CSS / React"),
    ("BACKEND", "Spring Boot / MySQL"),
    ("FOCUS", "DSA / AI-ML / Full-stack"),
    ("BUILD", "Projects with real-world use"),
]

def main():
    width, height = 490, 330

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect x="1" y="1" width="488" height="328" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<path d="M1 42 H489" stroke="#30363d"/>',
        '<circle cx="20" cy="21" r="5" fill="#ff7b72"/>',
        '<circle cx="38" cy="21" r="5" fill="#d29922"/>',
        '<circle cx="56" cy="21" r="5" fill="#3fb950"/>',
        '<text x="78" y="26" fill="#8b949e" font-family="monospace" font-size="12">daya@github — neofetch</text>',
        '<text x="22" y="68" fill="#58a6ff" font-family="monospace" font-size="15">DAYA RAJ</text>',
        '<text x="22" y="88" fill="#8b949e" font-family="monospace" font-size="11">-----------------------------------------</text>'
    ]

    for i, (key, value) in enumerate(ROWS):
        y = 120 + i * 28
        delay = i * 0.16
        opacity = "1" if STATIC else "0"
        animation = "" if STATIC else (
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
        )

        parts.append(
            f'<g opacity="{opacity}">'
            f'<text x="22" y="{y}" fill="#79c0ff" font-family="monospace" font-size="12">{html.escape(key)}</text>'
            f'<text x="112" y="{y}" fill="#c9d1d9" font-family="monospace" font-size="12">{html.escape(value)}</text>'
            f'{animation}</g>'
        )

    parts.append("</svg>")
    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print("Created info-card.svg successfully")

if __name__ == "__main__":
    main()
