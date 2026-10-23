"""A/B/C test on the RAJA FR home's "Mosaïque d'accueil" + illustrative results.

The Storyblok MCP has no experiment operations, so this script does only the experiment
part via the Management API: `setup` creates the experiment + variant stories,
`launch` publishes, activates and pushes the sample results. The variant stories'
content is edited through the MCP between the two steps.
Usage: python3 05_mosaic_experiment.py setup | launch
"""
import json, math, os, sys
from sb_mapi import SB

sb = SB(296080873997343, env_path=os.path.expanduser("~/dev/darwin/storyblok.env"))
NAME = "mosaique_accueil"


def experiment():
    found = [e for e in sb.experiments() if e["name"] == NAME]
    return sb._req(f"/experiments/{found[0]['id']}")["experiment"] if found else None


def setup():
    home = sb.find_story("raja-fr/home")
    exp = experiment() or sb._req("/experiments", "POST", {"experiment": {
        "name": NAME,
        "display_name": "RAJA FR · Mosaïque d'accueil",
        "description": "Quelle première diapositive et quelles tuiles font cliquer : best price entrepôt (contrôle), "
                       "offres d'abord, ou produits détourés.",
        "story_ids": [home["id"]],
        "experiment_variants_attributes": [
            {"name": "controle", "display_name": "Contrôle", "is_control": True, "weight": 34},
            {"name": "promo_dabord", "display_name": "Promo d'abord", "is_control": False, "weight": 33},
            {"name": "produits_detoures", "display_name": "Produits détourés", "is_control": False, "weight": 33},
        ],
    }})["experiment"]
    for v in exp["experiment_variants"]:
        if not v["is_control"] and not v.get("story_mappings"):
            sb._req(f"/experiments/{exp['id']}/variants/{v['id']}/story_mappings", "POST",
                    {"story_mapping": {"original_story_id": home["id"]}})
    exp = sb._req(f"/experiments/{exp['id']}")["experiment"]
    print(json.dumps({"id": exp["id"], "status": exp["status"], "variants": [
        {"name": v["name"], "id": v["id"], "stories": [m["variant_story_id"] for m in v.get("story_mappings") or []]}
        for v in exp["experiment_variants"]]}, indent=1))


def fr(v, d=2):
    """French decimal comma for chart text."""
    return f"{v:.{d}f}".replace(".", ",")


def charts(exp_id):
    L = ["Contrôle", "Promo d'abord", "Produits détourés"]
    DAYS = [f"J{d}" for d in range(1, 15)]
    V = [[1840, 1795, 1902, 1760, 1988, 1120, 980, 1875, 1820, 1930, 1790, 2010, 1150, 1010],
         [1830, 1810, 1890, 1775, 1975, 1105, 995, 1860, 1835, 1915, 1805, 1990, 1140, 1000],
         [1835, 1800, 1895, 1770, 1980, 1110, 990, 1870, 1825, 1925, 1795, 2000, 1145, 1005]]
    C = [[92, 88, 97, 85, 101, 55, 47, 93, 90, 98, 87, 103, 57, 49],
         [121, 118, 126, 113, 132, 70, 62, 124, 120, 128, 116, 135, 73, 64],
         [104, 99, 108, 97, 113, 62, 54, 106, 102, 110, 98, 115, 64, 56]]
    cum = lambda xs: [sum(xs[:i + 1]) for i in range(len(xs))]
    rate = lambda c, v: [round(a / b * 100, 2) for a, b in zip(c, v)]
    n = [sum(v) for v in V]
    x = [sum(c) for c in C]
    r = [round(a / b * 100, 2) for a, b in zip(x, n)]
    p1, p2 = x[0] / n[0], x[1] / n[1]
    p = (x[0] + x[1]) / (n[0] + n[1])
    z = (p2 - p1) / math.sqrt(p * (1 - p) * (1 / n[0] + 1 / n[1]))
    conf = round((1 - math.erfc(abs(z) / math.sqrt(2))) * 100, 1)
    up = [round((ri / r[0] - 1) * 100, 1) for ri in r]
    sessions = f"{sum(n):,}".replace(",", "\u202f")
    conf_txt = "> 99,9 %" if conf >= 99.95 else f"≈ {fr(conf, 1)} %"
    atc = [3.1, 3.9, 4.4]          # add-to-cart from the mosaic (% of sessions)
    rpv = [4.82, 5.37, 5.91]       # revenue per visitor (€ HT)
    return [
        {"kind": "text", "title": "Synthèse : Mosaïque d'accueil RAJA FR",
         "body": f"**Promo d'abord** gagne sur l'indicateur principal (clics sur la mosaïque) : **{fr(r[1])} %** contre "
                 f"**{fr(r[0])} %** pour le contrôle (+{fr(up[1], 1)} %, confiance {conf_txt}). **Produits détourés** clique moins "
                 f"({fr(r[2])} %) mais convertit mieux : ajout au panier {fr(atc[2], 1)} % et **{fr(rpv[2])} € HT** de CA par visiteur.\n\n"
                 f"{sessions} sessions sur 14 jours, répartition 34/33/33.\n\n"
                 "DONNÉES D'EXEMPLE : l'expérience et sa répartition sont réelles, les chiffres sont illustratifs."},
        {"kind": "bar", "title": "Taux de clic sur la mosaïque (indicateur principal)", "xLabel": "Variante",
         "yLabel": "CTR (%)", "labels": L, "series": [{"label": "CTR mosaïque (%)", "data": r}]},
        {"kind": "bar", "title": "Ajout au panier depuis la mosaïque", "xLabel": "Variante", "yLabel": "% des sessions",
         "labels": L, "series": [{"label": "Ajout au panier (%)", "data": atc}]},
        {"kind": "bar", "title": "Chiffre d'affaires par visiteur", "xLabel": "Variante", "yLabel": "€ HT",
         "labels": L, "series": [{"label": "CA / visiteur (€ HT)", "data": rpv}]},
        {"kind": "bar", "title": "Entonnoir : visite → clic mosaïque → fiche produit → panier", "xLabel": "Étape",
         "yLabel": "% des visiteurs", "labels": ["Visite", "Clic mosaïque", "Fiche produit", "Panier"],
         "series": [{"label": L[0], "data": [100, r[0], 3.6, atc[0]]},
                    {"label": L[1], "data": [100, r[1], 4.5, atc[1]]},
                    {"label": L[2], "data": [100, r[2], 5.2, atc[2]]}]},
        {"kind": "bar", "title": "Clics par emplacement de la mosaïque", "xLabel": "Emplacement", "yLabel": "Part des clics (%)",
         "labels": ["Diapositive 1", "Diapositives 2-3", "Tuile moyenne", "Petites tuiles"],
         "series": [{"label": L[0], "data": [41, 14, 27, 18]},
                    {"label": L[1], "data": [52, 11, 23, 14]},
                    {"label": L[2], "data": [38, 12, 24, 26]}]},
        {"kind": "bar", "title": "CTR mosaïque par appareil", "xLabel": "Appareil", "yLabel": "CTR (%)",
         "labels": ["Ordinateur", "Tablette", "Mobile"],
         "series": [{"label": L[0], "data": [5.6, 5.0, 4.1]},
                    {"label": L[1], "data": [7.2, 6.6, 5.8]},
                    {"label": L[2], "data": [6.3, 5.7, 4.6]}]},
        {"kind": "bar", "title": "Nouveaux clients vs clients existants (CTR)", "xLabel": "Profil", "yLabel": "CTR (%)",
         "labels": ["Nouveaux", "Existants"],
         "series": [{"label": L[0], "data": [4.4, 5.6]},
                    {"label": L[1], "data": [7.1, 5.9]},
                    {"label": L[2], "data": [5.0, 6.6]}]},
        {"kind": "bar", "title": "Contrôle de la répartition (sessions)", "xLabel": "Variante", "yLabel": "Sessions",
         "labels": L, "series": [{"label": "Sessions", "data": n}]},
        {"kind": "line", "title": "CTR cumulé par jour", "xLabel": "Jour du test", "yLabel": "CTR cumulé (%)",
         "labels": DAYS, "series": [{"label": L[i], "data": rate(cum(C[i]), cum(V[i]))} for i in range(3)]},
        {"kind": "line", "title": "CTR quotidien (creux du week-end visible en J6-J7 et J13-J14)", "xLabel": "Jour du test",
         "yLabel": "CTR (%)", "labels": DAYS, "series": [{"label": L[i], "data": rate(C[i], V[i])} for i in range(3)]},
        {"kind": "line", "title": "Sessions par jour", "xLabel": "Jour du test", "yLabel": "Sessions",
         "labels": DAYS, "series": [{"label": L[i], "data": V[i]} for i in range(3)]},
        {"kind": "text", "title": "Lecture et prochaine étape",
         "body": "Promo d'abord attire surtout les **nouveaux visiteurs** ; Produits détourés convertit mieux les **clients "
                 "existants**. Piste : garder Promo d'abord par défaut et servir Produits détourés aux clients connectés "
                 "(règle de personnalisation), plutôt que de choisir un seul gagnant."},
        {"kind": "text", "title": "Avertissement",
         "body": f"DONNÉES D'EXEMPLE, 14 jours simulés. Expérience {exp_id}, répartition 34/33/33. Ne pas choisir de "
                 "gagnant à partir de ces chiffres dans un vrai programme."},
    ]


def launch():
    exp = experiment()
    # the home and both variant stories are published via the MCP before launch
    if exp["status"] != "running":
        exp = sb._req(f"/experiments/{exp['id']}/activate", "PUT", {})["experiment"]
    ch = charts(exp["id"])
    # Storyblok accepts only bar, line and text (a pie chart is refused with 422, checked 2026-10-23)
    sb._req(f"/experiments/{exp['id']}/results", "POST", {"charts": ch})
    print("pushed", len(ch), "charts")
    print("status", exp["status"], exp["id"])


{"setup": setup, "launch": launch}[sys.argv[1]]()
