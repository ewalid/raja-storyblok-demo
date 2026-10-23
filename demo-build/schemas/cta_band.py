"""rj-cta-band: closing call-to-action band."""
from .common import *

comp("rj-cta-band", "Bandeau d'appel à l'action", schema({
    "title": text("Titre", required=True, max_length=80, description="Une question ou une invitation, ex. « Besoin d'un devis pour un gros volume ? »."),
    "text": rich("Texte", description="Une phrase. Le gras est mis en valeur."),
    "primary_label": text("Bouton principal", max_length=32, description=BTN_HELP),
    "primary_link": link("Lien du bouton principal"),
    "secondary_label": text("Bouton secondaire", max_length=32, description="Bouton contour, optionnel. " + BTN_HELP),
    "secondary_link": link("Lien du bouton secondaire"),
}), GROUP_SECT, icon="block-arrow-pointer", color="#276ef1", preview="title",
    description="Bandeau de fin de page : titre, phrase, un ou deux boutons. Aligné à gauche = boutons à droite ; centré = boutons dessous.")

preset("rj-cta-band", b("rj-cta-band", title="Besoin d'un devis pour un gros volume ?",
    text=doc(Pb("Nos conseillers vous répondent ", ("b", "de 8h à 18h30"), " et vous proposent un prix adapté à vos quantités.")),
    primary_label="Demander un devis", primary_link=url("https://www.raja.fr"),
    secondary_label="Nous contacter", secondary_link=url("https://www.raja.fr"), theme="brand"))
