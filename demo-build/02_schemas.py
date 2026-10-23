"""Push every RAJA component schema + default preset. Idempotent (create or update by name).
Single source of truth: demo-build/schemas/*.py. Never patch schemas by hand in the UI."""
import importlib, os, pkgutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sb_mapi import SB
import schemas
from schemas.common import COMPONENTS, PRESETS, PATCHES, SPACE, GROUP_SECT

only = set(sys.argv[1:])
for m in pkgutil.iter_modules(schemas.__path__):
    if m.name != "common":
        importlib.import_module(f"schemas.{m.name}")

sb = SB(SPACE, env_path=os.path.expanduser("~/dev/darwin/storyblok.env"))
groups = {g["name"]: g["uuid"] for g in sb._req("/component_groups")["component_groups"]}
def group(name):
    if name not in groups:
        groups[name] = sb._req("/component_groups", "POST", {"component_group": {"name": name}})["component_group"]["uuid"]
    return groups[name]

existing = {c["name"]: c for c in sb.components()}
for spec in COMPONENTS:
    if only and spec["name"] not in only:
        continue
    spec = dict(spec)
    spec["component_group_uuid"] = group(spec.pop("group"))
    # whitelist by group name -> uuid
    for fld in spec["schema"].values():
        if isinstance(fld, dict) and fld.get("component_group_whitelist_names"):
            fld["component_group_whitelist"] = [group(n) for n in fld.pop("component_group_whitelist_names")]
            fld["restrict_type"] = "groups"
    if spec["name"] in existing:
        sb._req(f"/components/{existing[spec['name']]['id']}", "PUT", {"component": spec})
    else:
        existing[spec["name"]] = sb._req("/components", "POST", {"component": spec})["component"]
    print("component", spec["name"])

# patches to existing starter components (e.g. default-page body whitelist)
for name, fields in PATCHES.items():
    if only and name not in only:
        continue
    c = next((x for x in sb.components() if x["name"] == name), None)
    if not c:
        continue
    for fld, changes in fields.items():
        changes = dict(changes)
        if "component_group_whitelist_names" in changes:
            changes["component_group_whitelist"] = [group(n) for n in changes.pop("component_group_whitelist_names")]
        c["schema"][fld].update(changes)
    sb._req(f"/components/{c['id']}", "PUT", {"component": {"name": name, "schema": c["schema"]}})
    print("patched", name)

# default presets: a block added in the editor arrives filled, not empty
presets = {}
for p in sb._req("/presets").get("presets", []):
    presets[(p["component_id"], p["name"])] = p["id"]
existing = {c["name"]: c for c in sb.components()}
NAME = "Par défaut"
for name, content in PRESETS.items():
    if (only and name not in only) or name not in existing:
        continue
    cid = existing[name]["id"]
    body = {"preset": {"name": NAME, "component_id": cid, "preset": content}}
    pid = presets.get((cid, NAME))
    if pid:
        sb._req(f"/presets/{pid}", "PUT", body)
    else:
        pid = sb._req("/presets", "POST", body)["preset"]["id"]
    sb._req(f"/components/{cid}", "PUT", {"component": {"name": name, "preset_id": pid}})
    print("preset", name, pid)
