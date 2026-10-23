"""rj-headline-band: the centred USP headline under the homepage hero."""
from .common import *

comp("rj-headline-band", "Titre d'accroche", schema({
    "text": rich("Titre", required=True, customize_toolbar=True, toolbar=["bold", "italic", "link"],
                 description="Une phrase. Les mots en gras prennent la couleur de la marque (bleu RAJA, rouge Mondoffice)."),
    "level": opt("Niveau de titre (SEO)", [("h1", "H1 : titre principal de la page"), ("h2", "H2 : titre de section")], "h1",
                 description="Un seul H1 par page. Choisissez H2 si la page a déjà un titre principal."),
    "size": opt("Taille", [("sm", "S (20 px)"), ("md", "M (28 px, comme le site)"), ("lg", "L (34 px)")], "md", description="M = taille du site actuel."),
}), GROUP_SECT, icon="block-text-c", color="#222831", preview="text",
    description="Grande phrase centrée, ex. « + de 12 000 produits en stock livrés en 24h ».")

preset("rj-headline-band", b("rj-headline-band", level="h1", size="md",
       text=doc(Pb(("b", "+ de 12 000 produits"), " d'emballages et d'équipements ", ("b", "en stock"), " livrés en ", ("b", "24h")))))
