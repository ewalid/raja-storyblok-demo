"""rj-reviews + rj-review: raja.fr reviews strip (note globale, Avis Vérifiés, cartes d'avis)."""
from .common import *

comp("rj-review", "Avis client", schema({
    "quote": area("Avis", required=True, max_length=200, description="Le texte de l'avis, tel que déposé (3 lignes maximum à l'affichage). Pas de guillemets : ils sont ajoutés automatiquement."),
    "author": text("Auteur", max_length=40, description="Ex. « Sandrine M. » ou « Anonyme »."),
    "date": text("Date", translatable=False, max_length=20, description="Telle qu'affichée, ex. « 22/10/2026 ». Le site ajoute « le » devant."),
    "stars": opt("Note", [("5", "5 étoiles"), ("4", "4 étoiles"), ("3", "3 étoiles"), ("2", "2 étoiles"), ("1", "1 étoile")], default="5", description="Nombre d'étoiles pleines."),
}, style=False, mobile=False, sites=False), GROUP_ITEM, icon="block-comment", color="#276ef1", preview="quote",
    description="Un avis client : texte, auteur, date, note.")

comp("rj-reviews", "Avis clients", schema({
    "title": text("Titre", max_length=70, description="Optionnel, ex. « Ils nous font confiance »."),
    "rating": text("Note globale", translatable=False, max_length=10, default_value="4,6/5", description="Au format « 4,6/5 » : les étoiles se remplissent automatiquement d'après cette note."),
    "count": text("Nombre d'avis", max_length=40, default_value="619 avis", description="Ex. « 619 avis ». Reprenez le chiffre réel de la plateforme d'avis."),
    "source_logo": image("Logo de la plateforme d'avis", description="Ex. le logo Avis Vérifiés ou Trustpilot (PNG transparent)."),
    "source_label": text("Nom de la plateforme", max_length=40, description="Texte à côté du logo, ex. « Avis certifiés par Avis Vérifiés »."),
    "reviews": bloks("Avis", ["rj-review"], minimum=1, maximum=12, description="1 à 12 avis, 3 visibles sur ordinateur, le reste défile."),
    "cta_label": text("Lien « tous les avis »", max_length=32, description=BTN_HELP),
    "cta_link": link("Lien vers tous les avis", description="Page de la plateforme d'avis ou page avis du site."),
}), GROUP_SECT, icon="block-comment", color="#276ef1", preview="rating",
    description="Note globale, logo de la plateforme d'avis et cartes d'avis clients qui défilent.")

def _rv(q, a, d, s="5"):
    return b("rj-review", quote=q, author=a, date=d, stars=s)

preset("rj-review", _rv("Commande rapide, livraison rapide. Toujours très professionnel.", "Anonyme", "22/10/2026"))
preset("rj-reviews", b("rj-reviews", title="Ce que nos clients en disent", rating="4,6/5", count="619 avis",
    source_logo=img("raja-avis-verifies"), source_label="Avis certifiés par Avis Vérifiés",
    cta_label="Voir tous les avis", cta_link=url("https://www.raja.fr"), reviews=[
        _rv("RAS, tout est OK.", "Anonyme", "22/10/2026"),
        _rv("Commande rapide, livraison rapide. Toujours très professionnel.", "Anonyme", "22/10/2026"),
    ]))
