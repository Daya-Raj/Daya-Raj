
from pathlib import Path
from datetime import date
import json
import re
import requests
from bs4 import BeautifulSoup

USERNAME = "Daya-Raj"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT = Path("data/contributions.json")

def main():
    response = requests.get(
        URL,
        timeout=30,
        headers={"User-Agent": "Daya-Raj-profile"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    days = []

    for cell in soup.select("td[data-date]"):
        day = cell.get("data-date")
        level = cell.get("data-level", "0")

        if not day:
            continue

        label = cell.get("aria-label", "")
        match = re.search(r"([\d,]+)\s+contributions?", label)
        count = int(match.group(1).replace(",", "")) if match else 0

        days.append({
            "date": day,
            "level": int(level),
            "count": count
        })

    if not days:
        raise SystemExit(
            "No contribution cells found. GitHub's page structure may have changed."
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps({
            "username": USERNAME,
            "fetched_on": date.today().isoformat(),
            "days": days
        }, indent=2),
        encoding="utf-8"
    )

    print(f"Saved {len(days)} contribution days to {OUTPUT}")

if __name__ == "__main__":
    main()
