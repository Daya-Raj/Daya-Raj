
from pathlib import Path
import sys
import cv2
import numpy as np
from PIL import Image

def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/prep_photo.py image.jpeg")

    source = Path(sys.argv[1])

    if not source.exists():
        raise SystemExit(f"Image not found: {source.resolve()}")

    image = Image.open(source).convert("RGB")
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    gray = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    ).apply(gray)

    Image.fromarray(gray).save("source-prepped.png")
    print("Created source-prepped.png successfully")

if __name__ == "__main__":
    main()
