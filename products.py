"""Product catalog for Luxury Tree Nuts and Dry Fruits.

Prices are in whole Indian Rupees (INR), matching the printed rate list
dated 17 August 2026. Update this list whenever the rate list changes.

`image` points to a file in static/images/ (illustrated product artwork).
`badge` is an optional short label shown on the product card.
"""

PRODUCTS_LIST = [
    # Almonds (Badam Giri)
    {"id": "badam-giri-regular", "name": "Badam Giri Regular", "quantity_label": "500g", "price": 759, "category": "Almonds (Badam Giri)", "image": "almond.svg"},
    {"id": "badam-giri-viraat", "name": "Badam Giri Viraat", "quantity_label": "500g", "price": 966, "category": "Almonds (Badam Giri)", "image": "almond.svg", "badge": "JUMBO"},
    {"id": "badam-giri-roasted", "name": "Badam Giri Roasted", "quantity_label": "500g", "price": 883, "category": "Almonds (Badam Giri)", "image": "almond-roasted.svg"},
    {"id": "badam-giri-roasted-viraat", "name": "Badam Giri Roasted Viraat", "quantity_label": "500g", "price": 1035, "category": "Almonds (Badam Giri)", "image": "almond-roasted.svg", "badge": "JUMBO"},
    {"id": "badam-giri-mamra", "name": "Badam Giri Mamra", "quantity_label": "500g", "price": 2898, "category": "Almonds (Badam Giri)", "image": "almond-mamra.svg", "badge": "PREMIUM"},
    {"id": "badam-giri-mamra-viraat", "name": "Badam Giri Mamra Viraat", "quantity_label": "500g", "price": 3432, "category": "Almonds (Badam Giri)", "image": "almond-mamra.svg", "badge": "PREMIUM JUMBO"},
    {"id": "badam-giri-sonora-viraat", "name": "Badam Giri Sonora Viraat", "quantity_label": "500g", "price": 977, "category": "Almonds (Badam Giri)", "image": "almond.svg", "badge": "JUMBO"},
    # Cashews (Kaju)
    {"id": "kaju", "name": "Kaju", "quantity_label": "500g", "price": 860, "category": "Cashews (Kaju)", "image": "cashew.svg"},
    {"id": "kaju-viraat-jumbo", "name": "Kaju Viraat (Jumbo)", "quantity_label": "500g", "price": 1182, "category": "Cashews (Kaju)", "image": "cashew.svg", "badge": "JUMBO"},
    {"id": "kaju-roasted", "name": "Kaju Roasted", "quantity_label": "500g", "price": 906, "category": "Cashews (Kaju)", "image": "cashew-roasted.svg"},
    {"id": "kaju-roasted-viraat", "name": "Kaju Roasted Viraat", "quantity_label": "500g", "price": 1256, "category": "Cashews (Kaju)", "image": "cashew-roasted.svg", "badge": "JUMBO"},
    # Pistachios
    {"id": "pistachio", "name": "Pistachio", "quantity_label": "500g", "price": 1196, "category": "Pistachios", "image": "pistachio.svg"},
    {"id": "pistachio-viraat-jumbo", "name": "Pistachio Viraat (Jumbo)", "quantity_label": "500g", "price": 1288, "category": "Pistachios", "image": "pistachio.svg", "badge": "JUMBO"},
    # Walnuts
    {"id": "walnut-inshell", "name": "Walnut Inshell", "quantity_label": "500g", "price": 676, "category": "Walnuts", "image": "walnut-inshell.svg"},
    {"id": "walnut-kernels", "name": "Walnut Kernels", "quantity_label": "500g", "price": 1196, "category": "Walnuts", "image": "walnut-kernel.svg"},
    # Mixes
    {"id": "breakfast-mix", "name": "Breakfast Mix", "quantity_label": "500g", "price": 635, "category": "Mixes", "image": "breakfast-mix.svg"},
    {"id": "mix-nuts-box-of-10", "name": "Mix Nuts Box of 10", "quantity_label": "500g", "price": 1040, "category": "Mixes", "image": "mix-nuts-box.svg"},
    {"id": "mix-nut-medium-jar", "name": "Mix Nut Medium Jar", "quantity_label": "250g", "price": 598, "category": "Mixes", "image": "mix-nut-jar.svg"},
    {"id": "mix-nut-big-jar", "name": "Mix Nut Big Jar", "quantity_label": "500g", "price": 1196, "category": "Mixes", "image": "mix-nut-jar.svg"},
    # Dried Berries & Figs
    {"id": "seedless-black-raisin", "name": "Seedless Black Raisin", "quantity_label": "250g", "price": 267, "category": "Dried Berries & Figs", "image": "raisin.svg"},
    {"id": "blueberry", "name": "Blueberry", "quantity_label": "1Kg", "price": 1632, "category": "Dried Berries & Figs", "image": "blueberry.svg"},
    {"id": "cranberry-whole", "name": "Cranberry Whole", "quantity_label": "1Kg", "price": 708, "category": "Dried Berries & Figs", "image": "cranberry.svg"},
    {"id": "figs", "name": "Figs", "quantity_label": "250g", "price": 900, "category": "Dried Berries & Figs", "image": "figs.svg"},
]

WEB_IMAGE_URLS = {
    "almond.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Almond_Nuts.jpg?width=900",
    "almond-roasted.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Ger%C3%B6stete_Mandeln.jpg?width=900",
    "almond-mamra.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/KASHMIRI_MAMRA_ALMONDS.jpg?width=900",
    "cashew.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Raw_cashew_(1).jpg?width=900",
    "cashew-roasted.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Vengurla_cashews_laid_out_in_the_sun_for_drying.jpg?width=900",
    "pistachio.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Pistachio.jpg?width=900",
    "walnut-inshell.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/3_walnuts.jpg?width=900",
    "walnut-kernel.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Black_walnut_cracked_open_to_expose_meat.jpg?width=900",
    "breakfast-mix.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Studentenfutter_01.JPG?width=900",
    "mix-nuts-box.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Nut_and-fruit_mixes_DEN_LILLE_NOTTEFABRIKKEN_Norway_Naturblanding_rosiner_torket_frukt_naturlige_notterr_(paranotter_mandler_valnotter)_og_torrostede_cashewnotter_2017.jpg?width=900",
    "mix-nut-jar.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/MixedNuts.JPG?width=900",
    "raisin.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/BLACK_RAISINS.jpg?width=900",
    "blueberry.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Fresh_blueberries_(49901958521).jpg?width=900",
    "cranberry.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Cranberries_in_bowl.jpg?width=900",
    "figs.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Fig_cut_open.jpg?width=900",
}

for product in PRODUCTS_LIST:
    product["web_image"] = WEB_IMAGE_URLS[product["image"]]

PRODUCTS = {p["id"]: p for p in PRODUCTS_LIST}

CATEGORIES = list(dict.fromkeys(p["category"] for p in PRODUCTS_LIST))
