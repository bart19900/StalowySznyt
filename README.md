# Stalowy Sznyt — galeria automatyczna

## Najważniejsze

Po dodaniu zdjęć do odpowiedniego folderu i wysłaniu zmian na GitHub, workflow sam uruchamia:

```bash
python tools/build_gallery.py
```

Skrypt przegląda foldery w:

```text
images/portfolio/
```

i generuje:

```text
data/gallery.json
```

Nie trzeba ręcznie dopisywać zdjęć do HTML.

## Dodawanie nowego produktu

1. Utwórz katalog, np.:

```text
images/portfolio/lampa-stojaca-01/
```

2. Włóż do niego zdjęcia:

```text
01.webp
02.webp
03.webp
```

Pierwsze zdjęcie alfabetycznie zostanie okładką.

3. Dodaj opcjonalny plik `product.json`:

```json
{
  "title": "Lampa stojąca L-01",
  "category": "Lampy",
  "description": "Czarna stal i naturalne drewno.",
  "featured": true,
  "order": 5,
  "status": "published"
}
```

4. Wykonaj commit i push do gałęzi `main`.

GitHub Actions przebuduje galerię i opublikuje stronę.

## Publikowanie projektu Inventora jako zdjęć

Do katalogu produktu możesz dodać:
- render z Inventora,
- eksport PNG/JPG,
- zrzut ekranu,
- później również plik GLB w katalogu `models/`.

Dla projektów w przygotowaniu ustaw:

```json
"status": "draft"
```

Po dodaniu zdjęć zmień status na:

```json
"status": "published"
```

## Lokalna aktualizacja galerii w Windows

Uruchom dwuklikiem:

```text
build-gallery.bat
```

Do działania wymagany jest Python 3.

## Ważne

W `Settings → Pages` źródło publikacji powinno być ustawione na:

```text
GitHub Actions
```
