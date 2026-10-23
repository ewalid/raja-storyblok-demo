"""rj-card-slider + rj-card: Mondoffice sector cards slider and blog row, one block with two looks."""
from .common import *

comp("rj-card", "Carte", schema({
    "image": media("Photo", description="Photo sans texte incrusté. Format paysage conseillé ; réglez le point focal dans le gestionnaire de médias."),
    "title": text("Titre", required=True, max_length=60, description="Court : 2 à 5 mots, ex. « Commerces alimentaires »."),
    "text": rich("Texte", description="Une ou deux phrases (3 lignes maximum à l'affichage). Non affiché en présentation « Vignettes »."),
    "link": link("Lien", description="Toute la carte devient cliquable. Vide = carte non cliquable."),
    "link_label": text("Libellé du lien", max_length=28, description="Remplace le libellé commun du carrousel pour cette carte uniquement. Vide = libellé commun."),
}, style=False, mobile=False, sites=False), GROUP_ITEM, icon="block-image", color="#ed1c24", preview="title",
    description="Une carte de carrousel : photo, titre, texte, lien.")

comp("rj-card-slider", "Carrousel de cartes", schema({
    "title": text("Titre", max_length=80, description="Ex. « Des solutions pour chaque secteur ». Vide = pas de titre."),
    "intro": rich("Introduction", description="Optionnelle, une phrase sous le titre."),
    "variant": opt("Présentation", [("cards", "Cartes blanches (photo, titre, texte, lien)"), ("tiles", "Vignettes photo avec bandeau titre (blog, guides)")], default="cards",
                   description="Cartes : comme « Soluzioni per ogni settore » de Mondoffice. Vignettes : comme la rangée blog « Mondoffice informa »."),
    "per_view": opt("Cartes visibles sur ordinateur", [("3", "3"), ("4", "4"), ("5", "5")], default="4",
                    description="Nombre de cartes visibles sans défiler sur grand écran. Sur mobile, une carte et demie ; les flèches apparaissent quand il y a plus de cartes."),
    "link_label": text("Libellé du lien des cartes", max_length=28, default_value="Découvrir", description="Affiché en bas de chaque carte, ex. « Découvrir », « Scopri di più ». Chaque carte peut le remplacer."),
    "cards": bloks("Cartes", ["rj-card"], minimum=2, maximum=10, description="2 à 10 cartes. L'ordre ici est l'ordre d'affichage."),
}), GROUP_SECT, icon="block-1-2block", color="#ed1c24", preview="title",
    description="Carrousel horizontal de cartes (secteurs, guides, articles) ; défilement tactile et flèches.")

def _card(title, text, key):
    return b("rj-card", title=title, text=doc(P(text)), image=img(key), link=url("https://www.raja.fr"), link_label="")

preset("rj-card", _card("E-commerce", "Cartons, pochettes et calage pour expédier vos commandes en toute sécurité.", "raja-corner-ecommerce"))
preset("rj-card-slider", b("rj-card-slider", title="Des solutions pour chaque secteur", variant="cards", per_view="4", link_label="Découvrir", cards=[
    _card("Toutes les activités", "Des produits professionnels et des solutions pensées pour les besoins de chaque secteur.", "group-warehouse-managers"),
    _card("Nettoyage et entretien", "Détergents, EPI et consommables pour l'entretien des bureaux, hôtels et locaux professionnels.", "group-hygiene-cleaning"),
    _card("E-commerce", "Emballages d'expédition, calage, étiquetage et équipement d'entrepôt pour préparer vos commandes.", "raja-corner-ecommerce"),
    _card("Bureaux et professions libérales", "Mobilier, fournitures, impression et archivage pour équiper tout le cabinet.", "group-office-open-space"),
    _card("Commerces de détail", "Sacs, emballages boutique et présentoirs pour valoriser vos produits en magasin.", "raja-corner-pack-protect-ship"),
]))
