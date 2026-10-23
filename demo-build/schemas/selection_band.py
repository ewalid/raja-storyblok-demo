"""rj-selection-band + rj-link-item: RAJA « Découvrez nos sélections de produits adaptés à votre activité »."""
from .common import *
from .usp_bar import ICONS

comp("rj-link-item", "Lien (liste)", schema({
    "label": text("Libellé", required=True, max_length=40, description="Texte du lien, ex. « E-commerce »."),
    "link": link("Lien", description="Page ou boutique visée. Sans lien, l'élément est masqué sur le site (cadre pointillé dans l'éditeur)."),
    "icon": opt("Pictogramme (optionnel)", ICONS, description="Petit pictogramme devant le libellé. Vide = pas de pictogramme (comme sur raja.fr)."),
}, style=False, mobile=False, sites=False), GROUP_ITEM, icon="block-arrow-pointer", color="#276ef1", preview="label",
    description="Un lien d'une liste, avec pictogramme optionnel.")

comp("rj-selection-band", "Bandeau sélections par activité", schema({
    "title": text("Titre", required=True, max_length=90, description="Une phrase, ex. « Découvrez nos sélections de produits adaptés à votre activité »."),
    "text": rich("Texte", description="Optionnel, une ou deux phrases. Le gras est mis en valeur."),
    "links": bloks("Liens", ["rj-link-item"], minimum=1, maximum=10, description="Les activités ou boutiques, 3 à 8 idéalement. Affichées sur 2 colonnes."),
    "cta_label": text("Bouton", max_length=32, description=BTN_HELP + " Ex. « Voir toutes les boutiques »."),
    "cta_link": link("Lien du bouton"),
    "images": multiasset("Photos (1 à 3)", description="1 à 3 photos sans texte incrusté, assemblées en mosaïque décalée à droite. Au-delà de 3, seules les 3 premières s'affichent. Réglez le point focal dans le gestionnaire de médias."),
}), GROUP_SECT, icon="block-image", color="#276ef1", preview="title",
    description="Bandeau couleur marque : titre, liste de liens par activité, bouton, mosaïque de photos.")

def _lk(label, u="https://www.raja.fr"):
    return b("rj-link-item", label=label, link=url(u), icon="")

preset("rj-link-item", _lk("E-commerce"))
preset("rj-selection-band", b("rj-selection-band",
    title="Découvrez nos sélections de produits adaptés à votre activité",
    text=doc(Pb("Emballages, équipements et fournitures choisis pour ", ("b", "votre métier"), ".")),
    links=[_lk("E-commerce"), _lk("Logistique"), _lk("Commerces de détail"), _lk("Commerces alimentaires"), _lk("Nettoyage et entretien")],
    cta_label="Voir toutes les boutiques", cta_link=url("https://www.raja.fr"),
    images=[a for a in (img("raja-sector-warehouse"), img("raja-sector-ecommerce"), img("raja-sector-boutique")) if a["filename"]],
    theme="band"))
