"""rj-promo-banner: the live sites' "mini-banner" (e.g. « PLUS DE 600 BEST SELLERS AU MEILLEUR PRIX ! »)."""
from .common import *

comp("rj-promo-banner", "Bandeau promo", schema({
    "badge": text("Pastille", max_length=24, description="Petit libellé carré au-dessus du titre, ex. « BEST PRICE », « -30 % ». Vide = pas de pastille."),
    "title": text("Titre", required=True, max_length=70, description="Court et percutant : il s'affiche en capitales."),
    "text": rich("Texte", description="Une phrase. Le gras prend la couleur d'accent."),
    "image": media("Visuel (détourage ou photo)", description="Idéal : un produit détouré (PNG transparent). Une vidéo courte fonctionne aussi."),
    "promo_code": text("Code promo", translatable=False, max_length=20, description="Affiché avec un bouton « Copier ». Vide = pas de code."),
    "ends_at": dt("Fin de l'offre (compte à rebours)", description="Affiche « Plus que 2 j 05 h ». Vide = pas de compte à rebours. Pour masquer le bandeau à cette date, utilisez aussi l'onglet Planning."),
    "cta_label": text("Bouton", max_length=24, description=BTN_HELP),
    "cta_link": link("Lien du bouton"),
}), GROUP_SECT, icon="block-sticker", color="#df091d", preview="title",
    description="Bandeau horizontal pour une offre : titre, code promo, compte à rebours, bouton.")

preset("rj-promo-banner", b("rj-promo-banner", badge="BEST PRICE", title="Plus de 600 best-sellers au meilleur prix !",
       text=doc(P("RAJA s'engage pour protéger votre budget.")), image=img("raja-caisse-double-cannelure"),
       cta_label="Je commande !", cta_link=url("https://www.raja.fr"), theme="promo"))
