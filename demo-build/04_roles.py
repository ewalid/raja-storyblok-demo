"""Space roles per branch (idempotent by role name). The MCP has no space-role operation, so MAPI.
- Atlas · Central groupe: everything (masters, both sites).
- Marketing RAJA FR: raja-fr/ only.
- Marketing Mondoffice IT: mondoffice-it/ + group/ (to translate group masters into Italian)."""
import os
from sb_mapi import SB
sb = SB(296080873997343, env_path=os.path.expanduser("~/dev/darwin/storyblok.env"))
folder = lambda slug: sb.find_story(slug)["id"]
ROLES = [
    ("Atlas · Central groupe", "Équipe centrale : campagnes maîtres et blocs partagés, tous les sites", [], []),
    ("Marketing RAJA FR", "Édite et publie uniquement raja.fr (dossier raja-fr)", [folder("raja-fr")], []),
    ("Marketing Mondoffice IT", "Modifica e pubblica solo mondoffice.it; traduce i contenuti del gruppo in italiano",
     [folder("mondoffice-it"), folder("group")], []),
]
have = {r["role"]: r["id"] for r in sb._req("/space_roles")["space_roles"]}
for name, sub, paths, langs in ROLES:
    body = {"space_role": {"role": name, "subtitle": sub, "allowed_paths": paths, "allowed_languages": langs,
                           "permissions": [], "resolved_allowed_paths": []}}
    if name in have:
        sb._req(f"/space_roles/{have[name]}", "PUT", body); print("updated", name, have[name])
    else:
        r = sb._req("/space_roles", "POST", body)["space_role"]; print("created", name, r["id"])
