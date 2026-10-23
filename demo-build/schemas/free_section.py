"""rj-free-section: a section composed by marketers from atoms (RAJA · Atomes group), 1 to 3 columns."""
from .common import *

def _col(n, help_):
    d = bloks(n, [], maximum=8, description=help_)
    d["component_group_whitelist_names"] = [GROUP_ATOM]
    d["restrict_components"] = True
    return d

comp("rj-free-section", "Section libre (atomes)", schema({
    "title": text("Titre de section", max_length=90, description="Optionnel. Pour un titre dans une colonne, ajoutez plutôt un atome « Titre »."),
    "columns": opt("Nombre de colonnes", [("1", "1 colonne"), ("2", "2 colonnes"), ("3", "3 colonnes")], default="2",
                   description="Sur mobile, les colonnes s'empilent dans l'ordre 1, 2, 3. Le contenu d'une colonne non affichée est conservé."),
    "body": _col("Colonne 1", "Composez avec les atomes : titre, texte, image, bouton. Jusqu'à 8 atomes."),
    "body_2": _col("Colonne 2", "Affichée si « Nombre de colonnes » vaut 2 ou 3."),
    "body_3": _col("Colonne 3", "Affichée si « Nombre de colonnes » vaut 3."),
    "valign": opt("Alignement vertical des colonnes", [("top", "En haut"), ("center", "Centré"), ("bottom", "En bas")], default="center",
                  description="Utile quand une colonne contient une image et l'autre du texte : « Centré » aligne le texte au milieu de l'image."),
    "gap": opt("Espacement", [("sm", "Serré"), ("md", "Normal"), ("lg", "Aéré")], default="md",
               description="Espace entre les atomes et entre les colonnes."),
}), GROUP_SECT, icon="block-block", color="#276ef1", preview="title",
    description="Section à composer soi-même avec des atomes (titre, texte, image, bouton) sur 1 à 3 colonnes, sans développeur et sans sortir de la charte.")

preset("rj-free-section", b("rj-free-section", title="", columns="2", valign="center", gap="md",
    body=[b("rj-atom-heading", text="Emballez et gardez au chaud", level="h2", size="lg", align="left", accent=False),
          b("rj-atom-text", size="lead", align="left", text=doc(Pb("Boîtes isothermes, sacs kraft et contenants pour la vente à emporter : ", ("b", "tout pour la restauration"), ", livré en 24h."))),
          b("rj-atom-button", label="Je découvre", link=url("https://www.raja.fr"), variant="primary", align="left")],
    body_2=[b("rj-atom-image", image=img("raja-cat-emballages-alimentaires"), ratio="classic", rounded=True, caption="", link=url(""))],
    body_3=[]))
