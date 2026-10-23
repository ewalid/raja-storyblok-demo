"""rj-category-grid + rj-category: the 16-tile category grid (cut-outs on RAJA, photos on Mondoffice)."""
from .common import *

comp("rj-category", "Catégorie", schema({
    "label": text("Libellé", required=True, max_length=40, description="Nom de la catégorie, 2 lignes max."),
    "image": image("Visuel", description="Style « Détouré » : PNG transparent carré (112 px affichés). Style « Photo » : photo carrée ou 4:3."),
    "link": link("Lien", description="Page de la catégorie (story) ou URL du site."),
}, style=False, mobile=False), GROUP_ITEM, icon="block-tag", color="#276ef1", preview="label",
    description="Une tuile de la grille de catégories.")

comp("rj-category-grid", "Grille de catégories", schema({
    "title": text("Titre", max_length=60, description="Optionnel : la grille de la page d'accueil n'a pas de titre."),
    "source": opt("Source des catégories", [("manual", "Manuel : les catégories saisies ci-dessous"),
                                            ("intershop", "Catalogue Intershop : catégories du site affiché (automatique)")], "manual",
                  description="Intershop = toujours à jour avec le catalogue du site (RAJA FR ou Mondoffice IT). Manuel = sélection éditoriale."),
    "columns": opt("Colonnes (ordinateur)", [("8", "8 (comme le site : 2 lignes de 8)"), ("6", "6"), ("4", "4")], "8",
                   description="Sur mobile, les catégories défilent horizontalement."),
    "image_style": opt("Style des visuels", [("cutout", "Détouré 112 px, sans carte (RAJA)"), ("photo", "Photo en carte avec libellé (Mondoffice)")], "cutout",
                       description="Détouré = PNG transparents. Photo = photos d'ambiance."),
    "limit": num("Nombre max (source Intershop)", default_value="16", description="Utilisé seulement avec la source Intershop."),
    "items": bloks("Catégories", ["rj-category"], maximum=24, description="Utilisées seulement avec la source « Manuel ». 16 = 2 lignes de 8."),
}), GROUP_SECT, icon="block-table-2", color="#276ef1", preview="title",
    description="Grille de catégories avec visuels : manuelle ou alimentée par le catalogue Intershop.")

CATS = [("Caisses carton, boîtes", "caisses-carton"), ("Adhésifs, cerclage, collage", "adhesifs"),
        ("Enveloppes, pochettes", "enveloppes"), ("Sacherie, conditionnement", "sacherie"),
        ("Calage, protection", "calage"), ("Etiquetage, signalisation", "etiquetage"),
        ("Film, palettisation", "film"), ("Machines d'emballage", "machines"),
        ("Stockage", "stockage"), ("Manutention", "manutention"),
        ("Équipements et sécurité", "securite"), ("Fournitures et mobilier de bureau", "bureau"),
        ("Entretien, hygiène", "hygiene"), ("Protection individuelle", "epi"),
        ("Emballages alimentaires", "alimentaire"), ("Emballages boutiques", "boutiques")]
def cat(label, key):
    return b("rj-category", label=label, image=img(f"raja-cat-{key}"), link=url("https://www.raja.fr"))
preset("rj-category", cat(*CATS[0]))
preset("rj-category-grid", b("rj-category-grid", source="manual", columns="8", image_style="cutout", limit="16",
       items=[cat(*c) for c in CATS]))
