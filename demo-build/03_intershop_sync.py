"""Sync the (mock) Intershop catalog into Storyblok datasources so editors pick SKUs and
category slugs from a dropdown instead of typing them. Idempotent: creates missing
datasources, upserts entries by value (SKU / slug), deletes entries no longer in the JSON.

Source of truth: server/data/intershop/<site>.json (the Intershop mock). When the real ICM
is connected, swap load_catalog() for a call to /INTERSHOP/rest/WFS/<site>/-/products.

Usage: python3 demo-build/03_intershop_sync.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sb_mapi import SB

SPACE = 296080873997343
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "server", "data", "intershop")

SITES = {
    "raja-fr": "Intershop · RAJA FR (simulé)",
    "mondoffice-it": "Intershop · Mondoffice IT (simulato)",
}
CATEGORY_NAMES = {
    "raja-fr": "Intershop · Catégories RAJA FR (simulé)",
    "mondoffice-it": "Intershop · Categorie Mondoffice IT (simulato)",
}


def load_catalog(site):
    with open(os.path.join(DATA, f"{site}.json")) as f:
        return json.load(f)


def trunc(s, n=70):
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def price(v):
    return f"{v:.2f}".replace(".", ",")


def ensure_datasource(sb, slug, name, existing):
    ds = existing.get(slug)
    if ds:
        if ds["name"] != name:
            sb._req(f"/datasources/{ds['id']}", "PUT", {"datasource": {"name": name, "slug": slug}})
        return ds["id"], False
    ds = sb._req("/datasources", "POST", {"datasource": {"name": name, "slug": slug}})["datasource"]
    return ds["id"], True


def list_entries(sb, ds_id):
    out, page = [], 1
    while True:
        r = sb._req(f"/datasource_entries?datasource_id={ds_id}&per_page=1000&page={page}")
        batch = r.get("datasource_entries", [])
        out += batch
        if len(batch) < 1000:
            return out
        page += 1


def sync_entries(sb, ds_id, wanted):
    """wanted: list of (name, value). Upsert by value, delete stale. Returns counts."""
    current = {e["value"]: e for e in list_entries(sb, ds_id)}
    c = {"created": 0, "updated": 0, "unchanged": 0, "deleted": 0}
    for name, value in wanted:
        e = current.pop(value, None)
        body = {"datasource_entry": {"name": name, "value": value, "datasource_id": ds_id}}
        if e is None:
            sb._req("/datasource_entries", "POST", body)
            c["created"] += 1
        elif e["name"] != name:
            sb._req(f"/datasource_entries/{e['id']}", "PUT", body)
            c["updated"] += 1
        else:
            c["unchanged"] += 1
    for e in current.values():
        sb._req(f"/datasource_entries/{e['id']}", "DELETE")
        c["deleted"] += 1
    return c


def main():
    sb = SB(SPACE, env_path=os.path.expanduser("~/dev/darwin/storyblok.env"))
    existing = {d["slug"]: d for d in sb._req("/datasources?per_page=100").get("datasources", [])}
    for site, ds_name in SITES.items():
        cat = load_catalog(site)
        jobs = [
            (f"intershop-{site}", ds_name,
             [(f"{p['sku']} · {trunc(p['name'])} · {price(p['salePrice']['value'])} €", p["sku"]) for p in cat["products"]]),
            (f"intershop-categories-{site}", CATEGORY_NAMES[site],
             [(c["name"], c["slug"]) for c in cat["categories"]]),
        ]
        for slug, name, wanted in jobs:
            ds_id, created = ensure_datasource(sb, slug, name, existing)
            counts = sync_entries(sb, ds_id, wanted)
            total = len(list_entries(sb, ds_id))
            print(f"{slug:36} id={ds_id} {'(new) ' if created else ''}entries={total} {counts}")


if __name__ == "__main__":
    main()
