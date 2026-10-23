"""rj-faq + rj-faq-item: accessible accordion (details/summary)."""
from .common import *

comp("rj-faq-item", "Question", schema({
    "question": text("Question", required=True, max_length=120, description="Formulée comme le client la poserait, ex. « Quels sont les délais de livraison ? »."),
    "answer": rich("Réponse", required=True, description="2 à 4 phrases. Liens et listes possibles."),
}, style=False, mobile=False, sites=False), GROUP_ITEM, icon="block-comment", color="#276ef1", preview="question",
    description="Une question et sa réponse.")

comp("rj-faq", "FAQ", schema({
    "title": text("Titre", max_length=70, default_value="Questions fréquentes", description="Ex. « Questions fréquentes »."),
    "intro": rich("Introduction", description="Optionnelle, une phrase sous le titre."),
    "items": bloks("Questions", ["rj-faq-item"], minimum=1, maximum=15, description="1 à 15 questions. Les plus fréquentes en premier."),
    "open_first": boolean("Première question ouverte", default_value=True, description="La première réponse est dépliée à l'arrivée sur la page."),
    "single_open": boolean("Une seule réponse ouverte à la fois", default_value=True, description="Ouvrir une question referme les autres. Décochez pour pouvoir en ouvrir plusieurs."),
}), GROUP_SECT, icon="block-comment", color="#276ef1", preview="title",
    description="Questions/réponses en accordéon, accessible au clavier.")

def _q(q, *a):
    return b("rj-faq-item", question=q, answer=doc(*a))

preset("rj-faq-item", _q("Quels sont les délais de livraison ?", P("Les produits en stock sont livrés en 24h. Le délai exact s'affiche sur chaque fiche produit et dans votre panier.")))
preset("rj-faq", b("rj-faq", title="Questions fréquentes", open_first=True, single_open=True, items=[
    _q("Quels sont les délais de livraison ?", P("Les produits en stock sont livrés en 24h. Le délai exact s'affiche sur chaque fiche produit et dans votre panier.")),
    _q("Comment trouver le bon format de carton ?", P("Utilisez l'outil « Je trouve mes formats » : saisissez les dimensions intérieures de votre produit (longueur x largeur x hauteur, en cm) parmi plus de 1 200 formats en stock.")),
    _q("Les prix sont-ils affichés hors taxes ?", P("Oui. Les prix sont indiqués HT, avec un prix dégressif selon la quantité commandée.")),
    _q("Comment utiliser un code promo ?", Pb("Saisissez le code dans votre panier avant de valider la commande. Exemple : ", ("b", "WBIENVENUE"), " pour -20 % sur votre première commande.")),
]))
