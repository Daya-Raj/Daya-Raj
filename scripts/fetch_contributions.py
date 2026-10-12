
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
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tooltip_counts = {}

    for tooltip in soup.find_all("tool-tip"):
        target = tooltip.get("for")
        text = tooltip.get_text(" ", strip=True)

        if not target:
            continue

        match = re.search(
            r"([\d,]+)\s+contributions?",
            text,
            re.IGNORECASE
        )

        if match:
            tooltip_counts[target] = int(
                match.group(1).replace(",", "")
            )

    days = []

    for cell in soup.select(
        "td.ContributionCalendar-day[data-date][data-level]"
    ):
        day = cell.get("data-date")
        cell_id = cell.get("id")

        if not day:
            continue

        try:
            date.fromisoformat(day)
            level = max(
                0,
                min(4, int(cell.get("data-level", "0")))
            )
        except (ValueError, TypeError):
            continue

        count = tooltip_counts.get(cell_id)

        if count is None and level == 0:
            count = 0

        days.append({
            "date": day,
            "level": level,
            "count": count
        })

    if not days:
        raise SystemExit("No contribution days found.")

    days.sort(key=lambda item: item["date"])

    exact_counts = sum(
        item["count"] is not None for item in days
    )

    total = (
        sum(item["count"] for item in days)
        if exact_counts == len(days)
        else None
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps({
            "username": USERNAME,
            "fetched_on": date.today().isoformat(),
            "days": days,
            "totalContributions": total
        }, indent=2),
        encoding="utf-8"
    )

    print(f"Found {len(days)} days.")
    print(f"Exact counts available: {exact_counts}")
    print(f"Total contributions: {total}")
    print(f"Saved data to {OUTPUT}")


if __name__ == "__main__":
    main()
