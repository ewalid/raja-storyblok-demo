"""Rich-text helpers shared by the content scripts (description fields are rich text)."""

FIELDS = {"rj-hero": ["subline"], "rj-feature-grid": ["intro"], "rj-feature": ["text"],
          "rj-split": ["text"], "rj-cta-band": ["text"], "rj-faq-item": ["answer"]}

def para(t):
    return {"type": "paragraph", "content": [{"type": "text", "text": t}]}
def doc(nodes):
    return {"type": "doc", "content": nodes}

def convert(b):
    changed = False
    for k in FIELDS.get(b.get("component"), []):
        v = b.get(k)
        if isinstance(v, str):
            b[k] = doc([para(v)] if v.strip() else [])
            changed = True
    if b.get("component") == "rj-split" and "bullets" in b:
        lines = [x.strip() for x in (b.pop("bullets") or "").split("\n") if x.strip()]
        if lines:
            d = b.get("text") if isinstance(b.get("text"), dict) else doc([])
            d["content"].append({"type": "bullet_list", "content": [{"type": "list_item", "content": [para(x)]} for x in lines]})
            b["text"] = d
        changed = True
    for v in list(b.values()):
        if isinstance(v, list):
            for child in v:
                if isinstance(child, dict) and child.get("component"):
                    changed = convert(child) or changed
    return changed
