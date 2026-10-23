"""rj-promo-duo: two half-width promo banners side by side (Mondoffice 632 x 233 pair)."""
from .common import *

comp("rj-promo-duo", "Duo de bannières", schema({
    "items": bloks("Bannières", ["rj-promo-tile"], minimum=2, maximum=3,
                   description="2 bannières côte à côte (3 possibles). Empilées sur mobile. Chacune peut être programmée (onglet Planning)."),
}), GROUP_SECT, icon="block-columns", color="#df091d",
    description="Deux bannières promo demi-largeur, 233 px de haut.")

preset("rj-promo-duo", b("rj-promo-duo", items=[
    b("rj-promo-tile", badge="VENTE FLASH", title="Film bulles 50 % recyclé", text=doc(Pb("Jusqu'à ", ("b", "-40 %"), " cette semaine seulement.")),
      cta_label="J'EN PROFITE", cta_link=url("https://www.raja.fr"), image=img("raja-duo-vente-flash"), image_mode="cutout", background="promo"),
    b("rj-promo-tile", title="Équipez votre entrepôt", text=doc(P("Rayonnages, établis et chariots livrés et montés.")),
      cta_label="JE DÉCOUVRE", cta_link=url("https://www.raja.fr"), image=img("raja-duo-entrepot"), image_mode="photo", background="soft"),
]))
