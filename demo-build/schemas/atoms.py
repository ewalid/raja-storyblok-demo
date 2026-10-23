"""Atoms (RAJA · Atomes): the building blocks of rj-free-section. No Style tab: the design is fixed."""
from .common import *

ALIGN3 = [("left", "Gauche"), ("center", "Centré"), ("right", "Droite")]

def atom(fields):
    return schema(fields, style=False, mobile=False, sites=False)

comp("rj-atom-heading", "Titre", atom({
    "text": text("Texte", required=True, max_length=90, description="Le titre, court."),
    "level": opt("Niveau (référencement)", [("h2", "H2 : titre de section"), ("h3", "H3 : sous-titre"), ("h4", "H4 : petit intertitre")], default="h2",
                 description="Pour Google et l'accessibilité. La taille visuelle se règle à part."),
    "size": opt("Taille", [("sm", "S"), ("md", "M"), ("lg", "L"), ("xl", "XL")], default="md", description="Taille d'affichage, dans l'échelle de la charte."),
    "align": opt("Alignement", ALIGN3, default="left", description="Gauche par défaut."),
    "accent": boolean("Couleur de la marque", description="Affiche le titre en bleu RAJA / rouge Mondoffice (en blanc sur un fond coloré)."),
}), GROUP_ATOM, icon="block-text-l", color="#5f6b7a", preview="text", description="Un titre de la charte (Raleway).")

comp("rj-atom-text", "Texte", atom({
    "text": rich("Texte", required=True, description="Paragraphes, listes, liens. Le gras prend la couleur de la marque."),
    "size": opt("Taille", [("normal", "Normale (14 px)"), ("lead", "Chapeau (16 px)")], default="normal", description="« Chapeau » pour une phrase d'introduction."),
    "align": opt("Alignement", ALIGN3, default="left", description="Gauche par défaut."),
}), GROUP_ATOM, icon="block-text-c", color="#5f6b7a", preview="text", description="Un paragraphe de texte riche.")

comp("rj-atom-image", "Image", atom({
    "image": media("Image ou vidéo", required=True, description="Photo sans texte incrusté, ou vidéo courte (en boucle, sans son). Réglez le point focal dans le gestionnaire de médias."),
    "ratio": opt("Format", [("original", "Format d'origine"), ("landscape", "Paysage 16:9"), ("classic", "Paysage 4:3"), ("square", "Carré"), ("portrait", "Portrait 4:5")], default="original",
                 description="L'image est recadrée autour du point focal. « Format d'origine » = pas de recadrage."),
    "rounded": boolean("Coins arrondis", default_value=True, description="Arrondi léger de la charte (4 px)."),
    "caption": text("Légende", max_length=120, description="Optionnelle, en petit sous l'image."),
    "link": link("Lien", description="Optionnel : l'image devient cliquable."),
}), GROUP_ATOM, icon="block-image", color="#5f6b7a", preview="caption", description="Une image ou une vidéo, avec légende et lien optionnels.")

comp("rj-atom-button", "Bouton", atom({
    "label": text("Libellé", required=True, max_length=32, description=BTN_HELP),
    "link": link("Lien", required=True),
    "variant": opt("Style", [("primary", "Principal (pilule couleur marque)"), ("ghost", "Contour"), ("square", "Carré (style formulaire)"), ("link", "Lien texte avec flèche")], default="primary",
                   description="Un seul bouton principal par section : les autres en contour ou lien texte."),
    "align": opt("Alignement", ALIGN3, default="left", description="Gauche par défaut."),
}), GROUP_ATOM, icon="block-arrow-pointer", color="#5f6b7a", preview="label", description="Un bouton de la charte.")

preset("rj-atom-heading", b("rj-atom-heading", text="Emballez et gardez au chaud", level="h2", size="md", align="left", accent=False))
preset("rj-atom-text", b("rj-atom-text", size="normal", align="left", text=doc(Pb("Boîtes isothermes, sacs kraft et contenants pour la vente à emporter, ", ("b", "livrés en 24h"), "."))))
preset("rj-atom-image", b("rj-atom-image", image=img("raja-cat-emballages-alimentaires"), ratio="classic", rounded=True, caption="", link=url("")))
preset("rj-atom-button", b("rj-atom-button", label="Je découvre", link=url("https://www.raja.fr"), variant="primary", align="left"))
