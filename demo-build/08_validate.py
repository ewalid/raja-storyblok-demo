"""Editor-side check: every block in the brand folders matches its schema
(component exists, fields declared, max_length, required, bloks whitelists)."""
import os
from sb_mapi import SB
sb = SB(295704400531259, env_path=os.path.expanduser("~/dev/darwin/storyblok.env"))
comps = {c["name"]: c for c in sb._req("/components?per_page=200")["components"]}
groups = {}
for c in comps.values():
    groups.setdefault(c.get("component_group_uuid"), set()).add(c["name"])
problems = []
def check(b, path):
    c = comps.get(b.get("component"))
    if not c:
        problems.append(f"{path}: unknown component {b.get('component')}"); return
    s = c["schema"]
    for k, v in b.items():
        if k in ("_uid", "component", "_editable"):
            continue
        if "__i18n__" in k:
            base = k.split("__i18n__")[0]
            if base not in s or not s[base].get("translatable"):
                problems.append(f"{path}.{k}: translation of a non-translatable/undeclared field")
            continue
        if k not in s:
            problems.append(f"{path}.{k}: field not declared on {c['name']}")
            continue
        d = s[k]
        if d.get("max_length") and isinstance(v, str) and len(v) > int(d["max_length"]):
            problems.append(f"{path}.{k}: {len(v)} > max {d['max_length']}")
        if d.get("type") == "bloks" and isinstance(v, list):
            if d.get("maximum") and len(v) > int(d["maximum"]):
                problems.append(f"{path}.{k}: {len(v)} > maximum {d['maximum']}")
            if d.get("minimum") and len(v) < int(d["minimum"]):
                problems.append(f"{path}.{k}: {len(v)} < minimum {d['minimum']}")
            for i, child in enumerate(v):
                cn = child.get("component")
                if d.get("restrict_components"):
                    allowed = set(d.get("component_whitelist") or [])
                    for g in d.get("component_group_whitelist") or []:
                        allowed |= groups.get(g, set())
                    if cn not in allowed:
                        problems.append(f"{path}.{k}[{i}]: {cn} not allowed")
                if cn and not comps.get(cn, {}).get("is_nestable", True) and cn != "default-page":
                    problems.append(f"{path}.{k}[{i}]: {cn} is not nestable")
                check(child, f"{path}.{k}[{i}]")
    for k, d in s.items():
        if d.get("required") and not b.get(k):
            problems.append(f"{path}.{k}: required but empty")
n = 0
home = sb._req(f"/stories/{sb.find_story('fr/home')['id']}")["story"]
check(home["content"], "home"); n += 1
for root in ["fr/landing-pages"]:
    fid = sb.find_story(root)["id"]
    stack = [fid]
    while stack:
        pid = stack.pop()
        for s in sb._req(f"/stories?with_parent={pid}&per_page=100")["stories"]:
            if s["is_folder"]:
                stack.append(s["id"]); continue
            full = sb._req(f"/stories/{s['id']}")["story"]
            n += 1
            if not full["published"] or full.get("unpublished_changes"):
                problems.append(f"{full['full_slug']}: not published / unpublished changes")
            check(full["content"], full["full_slug"])
print(n, "stories checked")
print("\n".join(problems) or "no problems")
