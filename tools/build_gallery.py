#!/usr/bin/env python3

from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

PORTFOLIO = ROOT / "images" / "portfolio"
MODELS = ROOT / "models"
OUTPUT = ROOT / "data" / "gallery.json"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".avif"
}

MODEL_EXTENSIONS = {
    ".glb"
}


# =========================================================
# NAZWY I KATEGORIE OBECNYCH PRODUKTÓW
# =========================================================

PRODUCT_DEFAULTS = {

    "krzeslo-barowe": {
        "title": "Krzesło barowe",
        "category": "Meble",
        "description":
            "Krzesło barowe w loftowym stylu.",
        "order": 10
    },

    "kwietnik-narozny": {
        "title": "Kwietnik narożny",
        "category": "Kwietniki",
        "description":
            "Narożny kwietnik wykonany z czarnej stali.",
        "order": 20
    },

    "kwietnik-pionowy-4-pietrowy": {
        "title": "Kwietnik pionowy 4-piętrowy",
        "category": "Kwietniki",
        "description":
            "Pionowy kwietnik o czterech poziomach.",
        "order": 30
    },

    "kwietnik": {
        "title": "Kwietnik",
        "category": "Kwietniki",
        "description":
            "Minimalistyczny kwietnik w stylu loftowym.",
        "order": 40
    },

    "lampa-kwietnik": {
        "title": "Lampa–kwietnik",
        "category": "Lampy i kwietniki",
        "description":
            "Połączenie oświetlenia i stalowej konstrukcji na rośliny.",
        "order": 50
    },

    "stolik-kanapowy": {
        "title": "Stolik kanapowy",
        "category": "Meble",
        "description":
            "Stolik pomocniczy z czarnej stali do strefy wypoczynkowej.",
        "order": 60
    },

    "stolik-kawowy": {
        "title": "Stolik kawowy",
        "category": "Meble",
        "description":
            "Loftowy stolik kawowy z czarnej stali i drewna.",
        "order": 70
    },

    "suszarka": {
        "title": "Suszarka",
        "category": "Wyposażenie",
        "description":
            "Stalowy element wyposażenia wykonany według indywidualnego projektu.",
        "order": 80
    },

    "wc-wieszak": {
        "title": "Wieszak WC",
        "category": "Wyposażenie",
        "description":
            "Minimalistyczny stalowy wieszak do łazienki.",
        "order": 90
    }
}


# =========================================================
# FUNKCJE POMOCNICZE
# =========================================================

def humanize(slug):

    text = re.sub(
        r"[-_]+",
        " ",
        slug
    ).strip()

    return text[:1].upper() + text[1:]


def read_json(path):

    if not path.is_file():
        return {}

    try:

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            f"Błędny JSON w {path}: {exc}"
        )


def relative_url(path):

    return path.relative_to(
        ROOT
    ).as_posix()


def normalize_path(value):

    return Path(
        str(value)
        .strip()
        .replace("\\", "/")
    ).as_posix()


# =========================================================
# ZDJĘCIA
# =========================================================

def find_images(folder):

    if not folder.is_dir():
        return []

    return sorted(

        path

        for path in folder.iterdir()

        if path.is_file()

        and path.suffix.lower()
        in IMAGE_EXTENSIONS
    )


# =========================================================
# AUTOMATYCZNE WYSZUKIWANIE MODELU
# =========================================================

def find_model(slug):

    folder = MODELS / slug

    if not folder.is_dir():
        return None


    # Najpierw szukamy idealnego układu:
    #
    # models/stolik-kawowy/stolik-kawowy.glb

    preferred = (
        folder /
        f"{slug}.glb"
    )


    if preferred.is_file():

        return preferred


    # Jeżeli nazwa pliku jest inna,
    # bierzemy pierwszy znaleziony GLB.

    models = sorted(

        path

        for path in folder.iterdir()

        if path.is_file()

        and path.suffix.lower()
        in MODEL_EXTENSIONS
    )


    if models:

        return models[0]


    return None


# =========================================================
# MODEL WPISANY RĘCZNIE W product.json
# =========================================================

def resolve_explicit_model(model_value):

    if not model_value:

        return None


    model_path = (
        ROOT /
        normalize_path(model_value)
    )


    if model_path.is_file():

        return model_path


    print(
        "OSTRZEŻENIE:"
        f" nie znaleziono modelu "
        f"{model_value}"
    )


    return None


# =========================================================
# METADANE PRODUKTU
# =========================================================

def load_metadata(slug):

    metadata = dict(
        PRODUCT_DEFAULTS.get(
            slug,
            {}
        )
    )


    # Można opcjonalnie umieścić:
    #
    # models/stolik-kawowy/product.json

    model_metadata = read_json(

        MODELS /
        slug /
        "product.json"
    )


    metadata.update(
        model_metadata
    )


    # Jeżeli istnieje folder portfolio,
    # jego product.json ma najwyższy priorytet.

    portfolio_metadata = read_json(

        PORTFOLIO /
        slug /
        "product.json"
    )


    metadata.update(
        portfolio_metadata
    )


    return metadata


# =========================================================
# MODELE JUŻ PRZYPISANE DO INNEGO PRODUKTU
# =========================================================

def collect_claimed_models():

    claimed = set()


    if not PORTFOLIO.is_dir():

        return claimed


    for folder in PORTFOLIO.iterdir():

        if not folder.is_dir():

            continue


        metadata = read_json(

            folder /
            "product.json"
        )


        model = metadata.get(
            "model"
        )


        if model:

            claimed.add(
                normalize_path(model)
            )


    return claimed


# =========================================================
# GENEROWANIE GALERII
# =========================================================

def build_gallery():

    PORTFOLIO.mkdir(
        parents=True,
        exist_ok=True
    )


    MODELS.mkdir(
        parents=True,
        exist_ok=True
    )


    # Produkty posiadające zdjęcia

    portfolio_slugs = {

        folder.name

        for folder
        in PORTFOLIO.iterdir()

        if folder.is_dir()
    }


    # Produkty posiadające modele

    model_slugs = {

        folder.name

        for folder
        in MODELS.iterdir()

        if folder.is_dir()
    }


    # Łączymy obie listy.

    all_slugs = (
        portfolio_slugs |
        model_slugs
    )


    claimed_models = (
        collect_claimed_models()
    )


    products = []


    for slug in sorted(
        all_slugs
    ):


        metadata = (
            load_metadata(slug)
        )


        # -----------------------------------------
        # STATUS
        # -----------------------------------------

        if (
            metadata.get(
                "status",
                "published"
            )
            != "published"
        ):

            print(
                f"Pominięto {slug}: "
                "status != published"
            )

            continue


        # -----------------------------------------
        # ZDJĘCIA
        # -----------------------------------------

        portfolio_folder = (
            PORTFOLIO /
            slug
        )


        images = find_images(
            portfolio_folder
        )


        # -----------------------------------------
        # MODEL 3D
        # -----------------------------------------

        explicit_model = (
            resolve_explicit_model(

                metadata.get(
                    "model",
                    ""
                )
            )
        )


        model_file = (

            explicit_model

            or

            find_model(slug)
        )


        # -----------------------------------------
        # ZABEZPIECZENIE PRZED DUPLIKATAMI
        # -----------------------------------------

        if (

            slug
            not in portfolio_slugs

            and

            model_file is not None

            and

            relative_url(model_file)
            in claimed_models
        ):

            print(
                f"Pominięto {slug}: "
                "model jest już używany "
                "przez inny produkt."
            )

            continue


        # -----------------------------------------
        # BRAK ZDJĘĆ I MODELU
        # -----------------------------------------

        if (
            not images
            and
            model_file is None
        ):

            print(
                f"Pominięto {slug}: "
                "brak zdjęć i GLB."
            )

            continue


        # -----------------------------------------
        # DANE PRODUKTU
        # -----------------------------------------

        title = metadata.get(

            "title",

            humanize(slug)
        )


        category = metadata.get(

            "category",

            "Modele 3D"
        )


        description = metadata.get(

            "description",

            "Interaktywny model 3D "
            "produktu Stalowy Sznyt."
        )


        product = {

            "slug":
                slug,

            "title":
                title,

            "category":
                category,

            "description":
                description,

            "featured":
                bool(
                    metadata.get(
                        "featured",
                        False
                    )
                ),

            "order":
                int(
                    metadata.get(
                        "order",
                        9999
                    )
                ),

            "cover":
                relative_url(
                    images[0]
                )
                if images
                else "",

            "images": [

                relative_url(image)

                for image
                in images
            ],

            "model":
                relative_url(
                    model_file
                )
                if model_file
                else ""
        }


        products.append(
            product
        )


    # -----------------------------------------
    # SORTOWANIE
    # -----------------------------------------

    products.sort(

        key=lambda product: (

            product["order"],

            product["title"].lower()
        )
    )


    return products


# =========================================================
# START
# =========================================================

def main():

    try:

        gallery = (
            build_gallery()
        )


        OUTPUT.parent.mkdir(

            parents=True,

            exist_ok=True
        )


        OUTPUT.write_text(

            json.dumps(

                gallery,

                ensure_ascii=False,

                indent=2
            ),

            encoding="utf-8"
        )


        print()

        print(
            f"Gotowe: {OUTPUT}"
        )


        print(
            "Liczba produktów "
            f"na stronie: {len(gallery)}"
        )


        print()


        for product in gallery:


            if product["images"]:

                image_status = (
                    str(
                        len(
                            product[
                                "images"
                            ]
                        )
                    )
                    +
                    " zdj."
                )

            else:

                image_status = "-"


            if product["model"]:

                model_status = "3D"

            else:

                model_status = "-"


            print(

                " • "
                +
                product["title"]
                +
                ": "
                +
                image_status
                +
                ", "
                +
                model_status
            )


        return 0


    except Exception as exc:


        print(

            f"BŁĄD: {exc}",

            file=sys.stderr
        )


        return 1


if __name__ == "__main__":

    raise SystemExit(
        main()
    )
