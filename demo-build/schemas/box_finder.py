"""rj-box-finder: raja.fr "Je trouve mes formats" (dimensions -> matching boxes from Intershop)."""
from .common import *

comp("rj-box-finder", "Recherche de cartons", schema({
    "title": rich("Titre", customize_toolbar=True, toolbar=["bold"], description="Les mots en gras prennent la couleur de la marque, ex. « Je trouve **mes formats** »."),
    "subtitle": text("Sous-titre", max_length=60, description="Ex. « Plus de 1200 formats en stock ! »."),
    "helper": text("Aide", max_length=120, description="Consigne au-dessus des champs, ex. « Entrer les dimensions intérieures en cm »."),
    "cta_label": text("Bouton", max_length=28, description="Lance la recherche dans le catalogue Intershop. Vide = « Trouver mon carton »."),
    "image": image("Visuel (carton détouré)", description="PNG transparent. Masqué sur mobile."),
    "empty_text": text("Message si aucun résultat", max_length=140, description="Optionnel. Vide = message par défaut proposant des dimensions proches."),
}), GROUP_SECT, icon="block-search", color="#276ef1", preview="subtitle",
    description="Bandeau de recherche par dimensions (L × l × H) : affiche les cartons correspondants du catalogue.")

preset("rj-box-finder", b("rj-box-finder", title=doc(Pb("Je trouve ", ("b", "mes formats"))), subtitle="Plus de 1200 formats en stock !",
       helper="Entrer les dimensions intérieures en cm (Longueur x largeur x Hauteur) :", cta_label="Trouver mon carton",
       image=img("raja-box-finder-carton"), theme="soft"))
