"""rj-product-carousel: products from the (mock) Intershop catalogue, picked by SKU or category per site."""
from .common import *

comp("rj-product-carousel", "Carrousel produits", schema({
    "title": text("Titre", max_length=60, description="Ex. « Ces produits pourraient vous intéresser »."),
    "see_all_label": text("Lien « Voir tout »", max_length=24, description="Ex. « Voir tout ». Affiché à droite du titre si un lien est renseigné."),
    "see_all_link": link("Lien « Voir tout »"),
    "source": opt("Choix des produits", [("skus", "Sélection de produits (SKU)"), ("category", "Une catégorie du catalogue")], "skus",
                  description="Rien de sélectionné = meilleures ventes du site, le bloc n'est jamais vide."),
    "skus_raja": ds_opts("Produits RAJA FR", "intershop-raja-fr",
                         description="Utilisés sur raja.fr. Prix, stock et visuels viennent d'Intershop : rien à ressaisir."),
    "skus_mondoffice": ds_opts("Prodotti Mondoffice IT", "intershop-mondoffice-it",
                               description="Utilisés sur mondoffice.it. Le même bloc affiche la sélection du site consulté."),
    "category_raja": ds_opt("Catégorie RAJA FR", "intershop-categories-raja-fr", description="Avec « Une catégorie du catalogue », sur raja.fr."),
    "category_mondoffice": ds_opt("Categoria Mondoffice IT", "intershop-categories-mondoffice-it", description="Avec « Une catégorie du catalogue », sur mondoffice.it."),
    "limit": num("Nombre max de produits", default_value="12", description="Entre 1 et 24."),
    "card_style": opt("Style des cartes", [("horizontal", "Horizontale, image à gauche (comme le site)"), ("vertical", "Verticale, image au-dessus")], "horizontal",
                      description="Horizontale = carte de 306 px du site actuel. Verticale = pour une page catégorie."),
}), GROUP_SECT, icon="block-carousel", color="#fe9601", preview="title",
    description="Produits Intershop (prix, stock, avis) dans un carrousel : choisissez des SKU ou une catégorie par site.")

preset("rj-product-carousel", b("rj-product-carousel", title="Ces produits pourraient vous intéresser", see_all_label="Voir tout",
       see_all_link=url("https://www.raja.fr/caisses-cartons-boites_C11.html"), source="skus", skus_raja=[], skus_mondoffice=[],
       limit="12", card_style="horizontal"))
