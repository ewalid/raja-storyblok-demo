"""rj-hero: campaign hero, one component with five layouts (the agency's "one component, several styles")."""
from .common import *

comp("rj-hero", "Hero de campagne", schema({
    "layout": opt("Mise en page", [("split", "Texte | visuel"), ("split-reverse", "Visuel | texte"), ("media-wide", "Texte | grand visuel"),
                                   ("stacked", "Texte centré, visuel dessous"), ("full-bg", "Visuel plein fond, texte sur carte blanche")], "split",
                  description="Même contenu, 5 styles : changez la mise en page sans ressaisir le texte."),
    "eyebrow": text("Sur-titre", max_length=40, description="Petite ligne au-dessus du titre, ex. « Black Friday ». Optionnel."),
    "headline": text("Titre", required=True, max_length=70, description="Le message principal, 2 lignes max."),
    "headline_accent": text("Fin du titre en couleur", max_length=40, description="Suite du titre affichée dans la couleur de la marque. Optionnel."),
    "subline": rich("Sous-titre", description="Une ou deux phrases (20 mots max conseillés). Le gras prend la couleur de la marque."),
    "primary_label": text("Bouton principal", max_length=24, description=BTN_HELP),
    "primary_link": link("Lien du bouton principal"),
    "secondary_label": text("Bouton secondaire", max_length=24, description="Bouton contour. " + BTN_HELP),
    "secondary_link": link("Lien du bouton secondaire"),
    "proof": text("Preuve (avis)", max_length=60, description="Petite ligne avec 5 étoiles, ex. « 4,6/5 sur 619 avis vérifiés ». Optionnel."),
    "image": media("Visuel (image ou vidéo)", description="Photo ou vidéo courte (muette, en boucle). Le point focal de l'image est respecté."),
    "video_poster": image("Image d'attente de la vidéo", description="Affichée pendant le chargement si le visuel est une vidéo."),
}), GROUP_SECT, icon="block-image", color="#6121f5", preview="headline",
    description="En-tête de page de campagne : titre, sous-titre, 2 boutons, visuel ; 5 mises en page.")

preset("rj-hero", b("rj-hero", layout="split", eyebrow="Rentrée logistique",
       headline="Préparez votre pic d'activité", headline_accent="dès maintenant",
       subline=doc(Pb("Plus de ", ("b", "1 200 formats de caisses"), " en stock, livrés en 24h partout en France.")),
       primary_label="Je découvre", primary_link=url("https://www.raja.fr/caisses-cartons-boites_C11.html"),
       secondary_label="Nos conseils", secondary_link=url("https://www.raja.fr"),
       proof="4,6/5 sur 619 avis vérifiés", image=img("raja-hero-entrepot"), theme="soft"))
