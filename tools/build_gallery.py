#!/usr/bin/env python3
"""
Generuje data/gallery.json na podstawie katalogów:
images/portfolio/<nazwa-produktu>/

Obsługiwane obrazy:
.jpg, .jpeg, .png, .webp, .avif

Opcjonalny plik product.json w katalogu produktu:
{
  "title": "Nazwa produktu",
  "category": "Kategoria",
  "description": "Opis",
  "featured": true,
  "order": 1,
  "status": "published"
}

Produkty bez zdjęć lub ze statusem innym niż "published" są pomijane.
"""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "images" / "portfolio"
OUTPUT = ROOT / "data" / "gallery.json"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

def humanize(slug: str) -> str:
    text = re.sub(r"[-_]+", " ", slug).strip()
    return text[:1].upper() + text[1:]

def load_metadata(folder: Path) -> dict:
    metadata_file = folder / "product.json"
    if not metadata_file.exists():
        return {}
    try:
        return json.loads(metadata_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Błędny JSON w {metadata_file}: {exc}") from exc

def relative_url(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def build_gallery() -> list[dict]:
    if not PORTFOLIO.exists():
        raise RuntimeError(f"Nie istnieje katalog: {PORTFOLIO}")

    products = []

    for folder in sorted(path for path in PORTFOLIO.iterdir() if path.is_dir()):
        metadata = load_metadata(folder)

        if metadata.get("status", "published") != "published":
            continue

        images = sorted(
            path for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        )

        if not images:
            print(f"Pominięto {folder.name}: brak zdjęć.")
            continue

        product = {
            "slug": folder.name,
            "title": metadata.get("title", humanize(folder.name)),
            "category": metadata.get("category", "Realizacje"),
            "description": metadata.get("description", ""),
            "featured": bool(metadata.get("featured", False)),
            "order": int(metadata.get("order", 9999)),
            "cover": relative_url(images[0]),
            "images": [relative_url(image) for image in images],
        }
        products.append(product)

    products.sort(key=lambda item: (item["order"], item["title"].lower()))
    return products

def main() -> int:
    try:
        gallery = build_gallery()
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(
            json.dumps(gallery, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"Gotowe: {OUTPUT}")
        print(f"Liczba opublikowanych produktów: {len(gallery)}")
        return 0
    except Exception as exc:
        print(f"Błąd: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
