"""rj-text: simple rich-text section."""
from .common import *

comp("rj-text", "Texte", schema({
    "title": text("Titre", max_length=100, description="Optionnel."),
    "body": rich("Texte", toolbar=["bold", "italic", "link", "list", "olist", "h2", "h3"],
                 description="Le contenu. Intertitres H2/H3, listes et liens possibles. Le gras prend la couleur de la marque."),
    "max_width": opt("Largeur du texte", [("narrow", "Étroite (lecture confortable)"), ("normal", "Normale"), ("wide", "Toute la largeur")], default="normal",
                     description="Une largeur étroite se lit mieux pour un texte long."),
    "columns": opt("Colonnes", [("1", "1 colonne"), ("2", "2 colonnes (ordinateur)")], default="1",
                   description="2 colonnes : le texte se répartit en deux sur ordinateur, une seule colonne sur mobile. Pour un texte de référencement par exemple."),
}), GROUP_SECT, icon="block-text-l", color="#276ef1", preview="title",
    description="Section de texte riche : intertitres, listes, liens.")

preset("rj-text", b("rj-text", title="Emballages et équipements pour les professionnels", max_width="normal", columns="1",
    body=doc(Pb("RAJA propose ", ("b", "plus de 12 000 produits"), " d'emballages et d'équipements en stock, livrés en 24h : caisses carton, adhésifs, films de palettisation, calage, stockage et manutention."),
             P("Que vous expédiez dix colis par jour ou plusieurs palettes, vous trouvez le format adapté, au prix dégressif selon la quantité."),
             ul("Plus de 1 200 formats de caisses en stock", "Prix affichés HT", "Conseil et devis pour les gros volumes"))))
