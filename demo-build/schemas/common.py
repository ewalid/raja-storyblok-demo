"""Shared schema kit for the RAJA Group demo (single source of truth: never patch schemas by hand).

Every block module in this folder calls `comp(...)` and `preset(...)`; 02_schemas.py imports
them all, pushes the components, then the default presets. Editor labels are French
(central team + RAJA FR); help text on every option.
"""
import json, os, uuid

SPACE = 296080873997343
HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "..", "assets", "manifest.json")

# ---------- field helpers ----------
def f(type_, name, **kw):
    d = {"type": type_, "display_name": name}
    d.update(kw)
    return d
text = lambda n, **k: f("text", n, **{"translatable": True, **k})
area = lambda n, **k: f("textarea", n, **{"translatable": True, **k})
# Body copy: rich text with a trimmed toolbar, so editors format text without breaking the design.
rich = lambda n, **k: f("richtext", n, **{"translatable": True, "customize_toolbar": True,
                                          "toolbar": ["bold", "italic", "link", "list", "olist"], **k})
boolean = lambda n, **k: f("boolean", n, **k)
num = lambda n, **k: f("number", n, **k)
media = lambda n, **k: f("asset", n, filetypes=["images", "videos"], **k)   # image OR video
image = lambda n, **k: f("asset", n, filetypes=["images"], **k)
multiasset = lambda n, **k: f("multiasset", n, filetypes=["images"], **k)
link = lambda n, **k: f("multilink", n, allow_target_blank=True, email_link_type=True, show_anchor=True, **k)
dt = lambda n, **k: f("datetime", n, **k)

def opt(n, choices, default=None, **k):
    d = f("option", n, options=[{"name": lbl, "value": val} for val, lbl in choices], **k)
    if default is not None:
        d["default_value"] = default
    return d

def opts(n, choices, **k):
    return f("options", n, options=[{"name": lbl, "value": val} for val, lbl in choices], **k)

def ds_opts(n, datasource, **k):
    """Multi-select fed by a datasource (e.g. the Intershop SKU snapshot)."""
    return f("options", n, source="internal", datasource_slug=datasource, **k)

def ds_opt(n, datasource, **k):
    return f("option", n, source="internal", datasource_slug=datasource, **k)

def bloks(n, whitelist, minimum=None, maximum=None, **k):
    d = f("bloks", n, restrict_components=True, restrict_type="", component_whitelist=whitelist, **k)
    if minimum:
        d["minimum"] = minimum
    if maximum:
        d["maximum"] = maximum
    return d

BTN_HELP = "Le bouton n'apparaît sur le site que si un libellé ET un lien sont renseignés."

# ---------- shared tabs (rendered by RjShell + useRjBlock.js) ----------
THEMES = [("white", "Blanc"), ("soft", "Gris clair (selon la marque)"), ("cream", "Crème (surlignage prix)"),
          ("brand", "Couleur de la marque (dégradé RAJA / rouge Mondoffice)"), ("band", "Bandeau marque clair"),
          ("dark", "Anthracite"), ("promo", "Rouge promo"), ("orange", "Orange remise")]
SPACING = [("none", "Aucun"), ("xs", "XS"), ("sm", "S"), ("md", "M"), ("lg", "L"), ("xl", "XL")]
ALIGN = [("left", "Gauche"), ("center", "Centré")]
TITLE = [("sm", "S"), ("md", "M"), ("lg", "L"), ("xl", "XL")]
SITES = [("raja-fr", "RAJA France"), ("mondoffice-it", "Mondoffice Italia")]

STYLE = {
    "theme": opt("Fond (charte groupe)", THEMES, description="Couleurs de la charte uniquement. Les couleurs « marque » s'adaptent seules au site (bleu RAJA, rouge Mondoffice). Vide = réglage par défaut du bloc."),
    "spacing": opt("Espacement intérieur (haut/bas)", SPACING, description="Vide = réglage par défaut du bloc."),
    "outer_spacing": opt("Marge extérieure", SPACING, description="Espace avant/après le bloc. Vide = aucun."),
    "align": opt("Alignement du texte", ALIGN, description="Vide = réglage par défaut du bloc."),
    "width": opt("Largeur", [("contained", "Contenue (1280 px)"), ("wide", "Large"), ("full", "Pleine largeur")], description="Vide = Contenue."),
    "shape": opt("Forme", [("square", "Droite (pleine largeur)"), ("rounded", "Carte arrondie")], description="Carte arrondie = le fond du bloc devient une carte."),
    "title_size": opt("Taille du titre", TITLE, description="Vide = réglage par défaut du bloc."),
}
MOBILE = {
    "mobile_hidden": boolean("Masquer sur mobile", description="Le bloc reste visible sur ordinateur."),
    "desktop_hidden": boolean("Masquer sur ordinateur", description="Pour un contenu prévu uniquement pour mobile."),
    "mobile_spacing": opt("Espacement mobile", SPACING, description="Mobile uniquement. Vide = comme sur ordinateur."),
    "mobile_align": opt("Alignement mobile", ALIGN, description="Mobile uniquement."),
    "mobile_title_size": opt("Taille du titre mobile", TITLE, description="Mobile uniquement."),
}
PLANNING = {
    "visible_from": dt("Visible à partir du", description="Vide = immédiatement. Le bloc apparaît seul à cette date (heure de Paris affichée dans l'éditeur)."),
    "visible_until": dt("Visible jusqu'au", description="Vide = sans fin. Le bloc disparaît automatiquement : idéal pour une promo."),
}
SITES_TAB = {
    "sites": opts("Visible sur les sites", SITES, description="Utile pour un bloc du groupe partagé entre sites. Vide = tous les sites."),
}

def schema(general, style=True, mobile=True, planning=True, sites=True, extra_tabs=None):
    s, pos, tabs = {}, 0, []
    def add(fields):
        nonlocal pos
        for k, v in fields.items():
            v = dict(v); v["pos"] = pos; pos += 1
            s[k] = v
        return list(fields.keys())
    add(general)
    tab_list = (extra_tabs or []) + [("Style", STYLE, style), ("Mobile", MOBILE, mobile), ("Planning", PLANNING, planning),
                                     ("Sites", SITES_TAB, sites)]
    for title, fields, on in tab_list:
        if on:
            tabs.append((title, add(fields)))
    for title, keys in tabs:
        s[f"tab-{uuid.uuid5(uuid.NAMESPACE_DNS, 'rj-' + title)}"] = {"type": "tab", "display_name": title, "keys": keys, "pos": pos}
        pos += 1
    return s

# ---------- registries ----------
COMPONENTS = []   # component specs
PRESETS = {}      # component name -> preset content (blok dict)
GROUP_SECT, GROUP_ITEM, GROUP_ATOM, GROUP_PAGE = "RAJA · Sections", "RAJA · Éléments", "RAJA · Atomes", "RAJA · Pages"

def comp(name, display, sch, group, nestable=True, root=False, icon=None, color=None, preview=None, description=""):
    COMPONENTS.append({"name": name, "display_name": display, "schema": sch, "is_nestable": nestable, "is_root": root,
                       "group": group, "icon": icon, "color": color, "preview_field": preview, "description": description})

def preset(name, content):
    PRESETS[name] = content

# ---------- content helpers for presets ----------
def _manifest():
    try:
        return json.load(open(MANIFEST))
    except FileNotFoundError:
        return {}
A = _manifest()

def img(key):
    a = A.get(key)
    if not a:
        return {"fieldtype": "asset", "filename": "", "id": None, "alt": ""}
    return {"fieldtype": "asset", "filename": a["filename"], "id": a.get("id"), "alt": a.get("alt", ""), "focus": "", "name": "", "title": ""}

def url(u):
    return {"linktype": "url", "url": u, "cached_url": u, "fieldtype": "multilink"}

P = lambda t: {"type": "paragraph", "content": [{"type": "text", "text": t}]}
def Pb(*parts):
    """Paragraph from parts; a part wrapped as ('b', text) is bold (shown in brand colour where supported)."""
    out = []
    for p in parts:
        if isinstance(p, tuple):
            out.append({"type": "text", "text": p[1], "marks": [{"type": "bold"}]})
        else:
            out.append({"type": "text", "text": p})
    return {"type": "paragraph", "content": out}
doc = lambda *n: {"type": "doc", "content": list(n)}
ul = lambda *items: {"type": "bullet_list", "content": [{"type": "list_item", "content": [P(i)]} for i in items]}

def b(component, **fields):
    return {"_uid": str(uuid.uuid4()), "component": component, **fields}

# Patches to existing (starter) components: {name: {field: {changes}}}, applied by 02_schemas.py.
PATCHES = {}
def patch(name, field, **changes):
    PATCHES.setdefault(name, {})[field] = changes
