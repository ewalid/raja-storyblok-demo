"""rj-showcase-band + rj-showcase-item: Mondoffice « Scopri le nostre Vetrine » brand band."""
from .common import *

comp("rj-showcase-item", "Vitrine", schema({
    "image": media("Photo", description="Photo sans texte incrusté, format paysage 16:9."),
    "label": text("Libellé", required=True, max_length=36, description="Affiché en capitales sous la photo, ex. « Tout pour l'expédition »."),
    "link": link("Lien", description="Toute la vitrine est cliquable. Vide = non cliquable."),
}, style=False, mobile=False, sites=False), GROUP_ITEM, icon="block-image", color="#ed1c24", preview="label",
    description="Une vitrine : photo, libellé, lien.")

comp("rj-showcase-band", "Bandeau vitrines", schema({
    "title": text("Titre", max_length=60, description="Ex. « Découvrez nos vitrines ». Vide = pas de titre."),
    "items": bloks("Vitrines", ["rj-showcase-item"], minimum=2, maximum=6, description="2 à 6 vitrines, réparties sur une ligne (2 par ligne sur mobile). 4 = comme Mondoffice."),
}), GROUP_SECT, icon="block-shop", color="#ed1c24", preview="title",
    description="Bandeau couleur marque avec 2 à 6 liens illustrés vers des sélections thématiques.")

def _sc(label, key):
    return b("rj-showcase-item", label=label, image=img(key), link=url("https://www.raja.fr"))

preset("rj-showcase-item", _sc("Tout pour l'expédition", "mo-vetrina-packaging"))
preset("rj-showcase-band", b("rj-showcase-band", title="Découvrez nos vitrines", theme="brand", items=[
    _sc("Tout pour l'expédition", "mo-vetrina-packaging"),
    _sc("Sécurité 360°", "mo-vetrina-dpi"),
    _sc("La technologie utile", "mo-vetrina-tech"),
    _sc("Sélection mobilier de bureau", "mo-vetrina-marreda"),
]))
