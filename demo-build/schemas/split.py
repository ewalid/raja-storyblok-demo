"""rj-split: text + photo/video side by side."""
from .common import *

comp("rj-split", "Texte + image", schema({
    "eyebrow": text("Surtitre", max_length=40, description="Petit libellé en capitales au-dessus du titre. À utiliser avec parcimonie : vide dans la plupart des cas."),
    "title": text("Titre", required=True, max_length=80, description="Une phrase courte."),
    "text": rich("Texte", description="2 à 4 phrases, ou une courte liste. Le gras prend la couleur de la marque."),
    "cta_label": text("Bouton", max_length=32, description=BTN_HELP),
    "cta_link": link("Lien du bouton"),
    "image": media("Image ou vidéo", description="Photo sans texte incrusté, ou vidéo courte (lue en boucle, sans son). Réglez le point focal dans le gestionnaire de médias."),
    "image_side": opt("Position de l'image", [("right", "À droite"), ("left", "À gauche")], default="right",
                      description="Sur mobile, l'image passe toujours au-dessus du texte. Alternez la position d'un bloc à l'autre."),
    "media_ratio": opt("Format de l'image", [("landscape", "Paysage 16:10"), ("square", "Carré"), ("portrait", "Portrait 4:5"), ("original", "Format d'origine")], default="landscape",
                       description="L'image est recadrée autour du point focal. « Format d'origine » = pas de recadrage."),
}), GROUP_SECT, icon="block-text-img-l", color="#276ef1", preview="title",
    description="Texte et image côte à côte, avec bouton.")

preset("rj-split", b("rj-split", eyebrow="", title="Je trouve mes formats",
    text=doc(Pb(("b", "Plus de 1 200 formats"), " de caisses en stock ! Entrez les dimensions intérieures de votre produit (longueur x largeur x hauteur, en cm) et trouvez le carton qu'il vous faut."),
             ul("Cartons simple et double cannelure", "Boîtes postales et caisses américaines", "Livrés en 24h")),
    cta_label="Trouver mon carton", cta_link=url("https://www.raja.fr/caisses-cartons-boites_C11.html"),
    image=img("raja-box-finder"), image_side="right", media_ratio="landscape", theme="soft"))
