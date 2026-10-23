"""Reusable Storyblok Management API helper for demo prep.

Throttled (respects the 6 req/s limit), idempotent where it matters. Reads tokens
from a project .env (STORYBLOK_MANAGEMENT_TOKEN + optional STORYBLOK_TOKEN).

Usage:
    from sb_mapi import SB
    sb = SB(space_id=293608500818806, env_path="/path/to/theme/.env")
    sb.upsert_story("careers/home", name="Accueil", content={...}, parent_slug="careers")
    sb.publish_story("careers/config")
    sb.create_or_update_component({"name": "hero", "is_nestable": True, "schema": {...}})
    sb.push_experiment_results(EXP_ID, charts=[...])   # experiment must be running

Nothing here is Storyblok-official; it's just thin wrappers over the documented MAPI.
"""
import json, time, urllib.request, urllib.error


class SB:
    def __init__(self, space_id, env_path=".env", region="eu"):
        self.space = str(space_id)
        host = {"eu": "mapi.storyblok.com", "us": "api-us.storyblok.com",
                "ap": "api-ap.storyblok.com", "ca": "api-ca.storyblok.com",
                "cn": "app.storyblokchina.cn"}[region]
        self.base = f"https://{host}/v1/spaces/{self.space}"
        env = {}
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k] = v.strip().strip('"').strip("'")
        self.h = {"Authorization": env["STORYBLOK_MANAGEMENT_TOKEN"],
                  "Content-Type": "application/json"}

    def _req(self, path, method="GET", body=None):
        data = json.dumps(body).encode() if body is not None else None
        for _ in range(8):
            req = urllib.request.Request(self.base + path, data=data, method=method, headers=self.h)
            try:
                r = urllib.request.urlopen(req)
                time.sleep(0.25)  # stay under 6 req/s
                raw = r.read()
                return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(1.6)
                    continue
                raise RuntimeError(f"HTTP {e.code} {method} {path}: {e.read().decode()[:400]}")
        raise RuntimeError(f"rate limited repeatedly: {path}")

    # ---- stories ----
    def find_story(self, slug):
        r = self._req(f"/stories?with_slug={slug}")
        s = r.get("stories", [])
        return s[0] if s else None

    def folder_id(self, slug, name=None):
        f = self.find_story(slug)
        if f:
            return f["id"]
        return self._req("/stories", "POST",
                         {"story": {"name": name or slug.title(), "slug": slug, "is_folder": True}})["story"]["id"]

    def upsert_story(self, slug, name, content, parent_slug=None, publish=False, path=None):
        story = {"content": content}
        if path is not None:
            story["path"] = path
        ex = self.find_story(slug)
        q = "?publish=1" if publish else ""
        if ex:
            return self._req(f"/stories/{ex['id']}{q}", "PUT", {"story": story})
        leaf = slug.split("/")[-1]
        story.update({"name": name, "slug": leaf})
        if parent_slug:
            story["parent_id"] = self.folder_id(parent_slug)
        return self._req(f"/stories{q}", "POST", {"story": story})

    def publish_story(self, slug):
        ex = self.find_story(slug)
        if not ex:
            raise RuntimeError(f"no story {slug}")
        st = self._req(f"/stories/{ex['id']}")["story"]
        return self._req(f"/stories/{ex['id']}?publish=1", "PUT", {"story": {"content": st["content"]}})

    def set_real_path(self, slug, path):
        ex = self.find_story(slug)
        return self._req(f"/stories/{ex['id']}", "PUT", {"story": {"path": path}})

    # ---- components + presets ----
    def components(self):
        return self._req("/components", ).get("components", [])

    def create_or_update_component(self, spec):
        """spec = {name, is_root, is_nestable, schema, ...}. Idempotent by name."""
        existing = {c["name"]: c["id"] for c in self.components()}
        if spec["name"] in existing:
            return self._req(f"/components/{existing[spec['name']]}", "PUT", {"component": spec})
        return self._req("/components", "POST", {"component": spec})

    def create_default_preset(self, component_name, preset_content, preset_name="Default"):
        cid = {c["name"]: c["id"] for c in self.components()}[component_name]
        p = self._req("/presets", "POST",
                      {"preset": {"name": preset_name, "component_id": cid, "preset": preset_content, "image": ""}})["preset"]
        self._req(f"/components/{cid}", "PUT", {"component": {"name": component_name, "preset_id": p["id"]}})
        return p["id"]

    @staticmethod
    def color(hex_value):
        return {"plugin": "native-color-picker", "color": hex_value}

    # ---- experiments (A/B) ----
    def experiments(self):
        return self._req("/experiments").get("experiments", [])

    def activate_experiment(self, experiment_id, end_date=None):
        q = f"?end_date={end_date}" if end_date else ""
        return self._req(f"/experiments/{experiment_id}/activate{q}", "PUT", {})

    def push_experiment_results(self, experiment_id, charts):
        """charts = list of {kind: bar|line|text, title, xLabel, yLabel, labels, series|body}.
        Experiment must be running or completed first (activate it, and publish the involved stories)."""
        return self._req(f"/experiments/{experiment_id}/results", "POST", {"charts": charts})

    def select_winner(self, experiment_id, variant_id):
        return self._req(f"/experiments/{experiment_id}/select_winner?variant_id={variant_id}", "PATCH", {})
