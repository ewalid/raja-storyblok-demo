"""Upload local/remote images to the Storyblok asset library (signed S3 flow). Idempotent by filename."""
import json, os, subprocess, time, urllib.request
from sb_mapi import SB

class Assets:
    def __init__(self, sb):
        self.sb = sb
        self._folders = None
        self._existing = None

    def folder(self, name, parent_id=None):
        if self._folders is None:
            self._folders = self.sb._req("/asset_folders")["asset_folders"]
        for f in self._folders:
            if f["name"] == name and (f.get("parent_id") or None) == parent_id:
                return f["id"]
        body = {"asset_folder": {"name": name}}
        if parent_id:
            body["asset_folder"]["parent_id"] = parent_id
        f = self.sb._req("/asset_folders", "POST", body)["asset_folder"]
        self._folders.append(f)
        return f["id"]

    def existing(self):
        if self._existing is None:
            self._existing, page = {}, 1
            while True:
                r = self.sb._req(f"/assets?per_page=100&page={page}")
                for a in r.get("assets", []):
                    self._existing[a["filename"].split("/")[-1]] = a
                if len(r.get("assets", [])) < 100:
                    break
                page += 1
        return self._existing

    def upload(self, path, folder_id=None, alt="", title=""):
        name = os.path.basename(path)
        ex = self.existing().get(name)
        if ex:
            return ex["filename"]
        size = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path], capture_output=True, text=True).stdout
        w = h = None
        for line in size.splitlines():
            if "pixelWidth" in line: w = line.split()[-1]
            if "pixelHeight" in line: h = line.split()[-1]
        body = {"filename": name, "asset_folder_id": folder_id}
        if not (w and h):  # videos: sips can't read them, ffprobe can
            out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                  "-of", "csv=p=0:s=x", path], capture_output=True, text=True).stdout.strip()
            if "x" in out:
                w, h = out.split("x")[:2]
        if w and h and w != "<nil>":
            body["size"] = f"{w}x{h}"
        signed = self.sb._req("/assets", "POST", body)
        args = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", signed["post_url"]]
        for k, v in signed["fields"].items():
            args += ["-F", f"{k}={v}"]
        args += ["-F", f"file=@{path}"]
        code = subprocess.run(args, capture_output=True, text=True).stdout
        if code not in ("200", "201", "204"):
            raise RuntimeError(f"S3 upload failed {code} for {name}")
        a = self.sb._req(f"/assets/{signed['id']}/finish_upload")
        if alt or title:
            self.sb._req(f"/assets/{signed['id']}", "PUT", {"asset": {"alt": alt, "title": title}})
        url = f"https://a.storyblok.com/{signed['fields']['key']}"
        self.existing()[name] = {"filename": url, "id": signed["id"]}
        return url

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest
