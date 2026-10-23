"""rj-hero-mosaic + rj-promo-tile: the homepage tile grid of raja.fr and mondoffice.it
(big slider + medium/small tiles, 1280 x 370), with every word editable instead of baked
into the image."""
from .common import *

TILE_BG = [("brand", "Couleur de la marque (dégradé RAJA / rouge Mondoffice)"), ("promo", "Rouge promo"),
           ("orange", "Orange remise"), ("dark", "Anthracite"), ("soft", "Gris clair"), ("cream", "Crème"), ("white", "Blanc (bordure fine)")]

comp("rj-promo-tile", "Tuile promo", schema({
    "title": text("Titre", required=True, max_length=60, description="Court : 2 lignes max sur une petite tuile. Police Raleway extra-grasse."),
    "badge": text("Pastille", max_length=20, description="Petit libellé carré, ex. « BEST PRICE », « -20 % », « NOUVEAU ». Vide = pas de pastille."),
    "badge_color": opt("Couleur de la pastille", [("red", "Rouge (BEST PRICE)"), ("orange", "Orange (remise)"), ("brand", "Couleur de la marque (nouveauté)"), ("dark", "Anthracite")], "red",
                       description="Rouge = meilleur prix, orange = remise en %, couleur marque = nouveauté, anthracite = neutre."),
    "eyebrow": text("Sur-titre", max_length=40, description="Petite ligne au-dessus du titre, ex. « Offre de bienvenue ». Optionnel."),
    "text": rich("Texte", description="Une phrase. Le gras ressort (ex. le code promo). Masqué sur les petites tuiles en mobile."),
    "cta_label": text("Bouton", max_length=24, description="Ex. « JE DÉCOUVRE ». Toute la tuile est cliquable dès qu'un lien est renseigné."),
    "cta_link": link("Lien de la tuile", description="Rend toute la tuile cliquable. Sans lien, la tuile s'affiche mais ne mène nulle part."),
    "image": media("Visuel (image ou vidéo)", description="Produit détouré (PNG transparent) ou photo d'ambiance. Pas de texte incrusté : le texte est saisi ici, donc traduisible."),
    "image_mode": opt("Placement du visuel", [("cutout", "Détouré à droite (produit sur fond de couleur)"), ("photo", "Photo sur la moitié droite"),
                                              ("background", "Photo plein fond (voile sombre pour la lisibilité)")], "cutout",
                      description="Détouré = idéal pour un packshot transparent. Plein fond = le texte passe en blanc sur la photo."),
    "background": opt("Fond", TILE_BG, "brand", description="Couleurs de la charte uniquement. Ignoré en mode « Photo plein fond »."),
}, style=False, mobile=False), GROUP_ITEM, icon="block-image", color="#276ef1", preview="title",
    description="Une diapositive ou une tuile : pastille, titre, texte, bouton, visuel. Peut être programmée (onglet Planning).")

comp("rj-hero-mosaic", "Mosaïque d'accueil", schema({
    "layout": opt("Composition", [("raja", "RAJA : diaporama + 1 tuile moyenne au-dessus de petites tuiles"),
                                  ("mondoffice", "Mondoffice : diaporama + 2 × 2 petites tuiles"),
                                  ("slider", "Diaporama seul, pleine largeur")], "raja",
                  description="La grille de droite s'adapte au nombre de tuiles : jamais de case vide."),
    "slides": bloks("Diapositives", ["rj-promo-tile"], minimum=1, maximum=6,
                    description="1 à 6 diapositives. Chacune peut avoir ses dates (onglet Planning de la diapositive) : idéal pour une promo."),
    "tiles": bloks("Tuiles à droite", ["rj-promo-tile"], maximum=4,
                   description="0 à 4 tuiles. RAJA : 3 (1 moyenne + 2 petites). Mondoffice : 4. Ignorées en mode « Diaporama seul »."),
    "autoplay": num("Défilement automatique (secondes)", default_value="6",
                    description="0 = pas de défilement automatique. S'arrête au survol, dans l'éditeur visuel et si l'utilisateur a réduit les animations."),
}), GROUP_SECT, icon="block-carousel", color="#276ef1", preview="layout",
    description="Première section des pages d'accueil : grand diaporama à gauche, tuiles promo à droite (370 px de haut).")

def tile(**k):
    return b("rj-promo-tile", **k)

SLIDES = [
    tile(badge="BEST PRICE", title="Moins d'effort, plus d'efficacité", text=doc(Pb("Transpalettes et chariots ", ("b", "au meilleur prix"), " toute l'année.")),
         cta_label="JE DÉCOUVRE", cta_link=url("https://www.raja.fr"), image=img("raja-hero-warehouse-scanner"),
         image_mode="cutout", background="brand"),
    tile(badge="-20 %", badge_color="orange", eyebrow="Offre de bienvenue", title="-20 % sur votre 1ère commande",
         text=doc(Pb("Avec le code ", ("b", "WBIENVENUE"), ", sans minimum d'achat.")), cta_label="J'EN PROFITE",
         cta_link=url("https://www.raja.fr"), image=img("raja-hero-packaging"), image_mode="cutout", background="dark"),
    tile(title="Bientôt les fêtes de fin d'année, anticipez votre pic d'activité !", text=doc(P("Emballages, calage et étiquetage livrés en 24h.")),
         cta_label="JE DÉCOUVRE", cta_link=url("https://www.raja.fr"), image=img("raja-hero-boutique"), image_mode="background"),
]
TILES = [
    tile(badge="CADEAU", badge_color="orange", title="Halloween approche…", text=doc(Pb("Un seau de bonbons offert dès ", ("b", "250 € HT"), " d'achat*.")),
         cta_label="J'EN PROFITE", cta_link=url("https://www.raja.fr"), image=img("raja-boutique-shopping-bag"), image_mode="cutout", background="promo"),
    tile(title="La marque engagée pour vous simplifier la vie", cta_label="NOS ENGAGEMENTS", cta_link=url("https://www.raja.fr"),
         image=img("raja-hero-eco-globe"), image_mode="cutout", background="soft"),
    tile(title="Emballez et gardez au chaud", cta_label="JE DÉCOUVRE", cta_link=url("https://www.raja.fr"),
         image=img("raja-cat-emballages-alimentaires"), image_mode="cutout", background="cream"),
]
preset("rj-promo-tile", SLIDES[0])
preset("rj-hero-mosaic", b("rj-hero-mosaic", layout="raja", slides=SLIDES, tiles=TILES, autoplay="6"))
