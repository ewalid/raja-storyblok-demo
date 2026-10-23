"""rj-usp-bar + rj-usp-item: reassurance bar (Mondoffice in-page USP bar: grey, 46px, radius 4px, brand icons)."""
from .common import *

# RjIcon names with editor labels (shared with rj-link-item and atoms).
ICONS = [("truck", "Camion (livraison)"), ("box", "Colis"), ("gift", "Cadeau"), ("mail", "Enveloppe"),
         ("phone", "Téléphone"), ("star", "Étoile (avis)"), ("search", "Loupe"), ("cart", "Panier"),
         ("user", "Compte client"), ("bolt", "Éclair (rapidité)"), ("shield", "Bouclier (sécurité, garantie)"),
         ("return", "Retour (satisfait ou remboursé)"), ("euro", "Euro (prix)"), ("leaf", "Feuille (éco-responsable)"),
         ("clock", "Horloge (délai)"), ("check", "Coche (validé)"), ("tag", "Étiquette (promo)"),
         ("headset", "Casque (service client)"), ("factory", "Usine (fabrication)"), ("arrow", "Flèche")]

comp("rj-usp-item", "Argument de réassurance", schema({
    "icon": opt("Pictogramme", ICONS, default="truck", description="Pictogramme de la charte, affiché dans la couleur de la marque (bleu RAJA, rouge Mondoffice)."),
    "text": text("Texte en gras", required=True, max_length=48, description="L'argument, court : « Livrés en 24h », « 4,6/5 Avis Vérifiés »."),
    "subtext": text("Précision (petit texte)", max_length=60, description="Optionnel : la condition ou le détail, ex. « Sur les produits en stock »."),
    "link": link("Lien (optionnel)", description="Vide = l'argument n'est pas cliquable."),
}, style=False, mobile=False, sites=False), GROUP_ITEM, icon="block-shield", color="#276ef1", preview="text",
    description="Un argument : pictogramme, texte en gras, précision.")

comp("rj-usp-bar", "Barre de réassurance", schema({
    "style": opt("Présentation", [("bar", "Barre grise compacte (comme Mondoffice)"), ("cards", "Pictogramme au-dessus du texte")], default="bar",
                 description="Barre : une ligne grise arrondie de 46 px, idéale sous un bandeau. Pictogrammes au-dessus : plus aéré, pour une page de contenu."),
    "items": bloks("Arguments", ["rj-usp-item"], minimum=2, maximum=5, description="2 à 5 arguments. Ils se répartissent sur la largeur ; sur mobile ils s'empilent."),
}), GROUP_SECT, icon="block-shield", color="#276ef1", preview="style",
    description="Bandeau d'arguments de réassurance : livraison, avis clients, satisfait ou remboursé.")

def _usp(icon, t, s):
    return b("rj-usp-item", icon=icon, text=t, subtext=s, link=url(""))

preset("rj-usp-item", _usp("truck", "Livrés en 24h", "Sur les produits en stock"))
preset("rj-usp-bar", b("rj-usp-bar", style="bar", theme="white", spacing="xs", items=[
    _usp("truck", "Livrés en 24h", "Sur les produits en stock"),
    _usp("box", "+ de 12 000 produits", "Emballages et équipements en stock"),
    _usp("star", "4,6/5 Avis Vérifiés", "619 avis clients"),
    _usp("headset", "01 49 90 49 90", "Nos conseillers de 8h à 18h30"),
]))
