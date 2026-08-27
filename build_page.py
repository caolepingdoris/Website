# -*- coding: utf-8 -*-
"""
Assembles index.html from _head.part + _body.part, expanding markers
against assets/manifest.json (written by build_assets.py).

Markers
  <!--GRID:group-->   gallery cells — clickable, feed the lightbox
  <!--STRIP:group-->  plain <img> row for a project strip

Run:  python build_page.py   (--force to overwrite hand edits)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "index.html")

_parts = [os.path.join(ROOT, "_head.part"), os.path.join(ROOT, "_body.part")]
if os.path.exists(OUT) and os.path.getmtime(OUT) > max(os.path.getmtime(p) for p in _parts):
    print("index.html is newer than the source parts — it looks hand-edited.")
    if "--force" not in sys.argv:
        raise SystemExit(1)

man = json.load(open(os.path.join(ROOT, "assets", "manifest.json"), encoding="utf-8"))

# group -> caption stem shown under each frame and in the lightbox
CAPTION = {
    "levi":      "Levi By The Sea",
    "circle":    "How Can I Become A Circle",
    "poem":      "The Poem of Future",
    "kmoryu":    "К МОРЮ",
    "boylston":  "Boylston Film Festival",
    "unsolved":  "Unsolved Problem",
    "vivid":     "Vivid Dream",
    "feel":      "Do You Feel It",
    "install":     "Do You Feel It — installation view",
    "installwide": "Do You Feel It — installation view",
    "bostonl":   "Boston",
    "la":        "Los Angeles",
    "cities":    "Cities",
    "chinatown": "Chinatown",
    "event":     "Event photography",
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def cells(group, indent="    "):
    cap, out = esc(CAPTION[group]), []
    for n, it in enumerate(man[group], 1):
        label = f"{cap} — {n:02d}"
        out.append(
            f'{indent}<button class="cell" data-cap="{label}" type="button">\n'
            f'{indent}  <img loading="lazy" decoding="async" width="{it["w"]}" height="{it["h"]}"\n'
            f'{indent}       src="assets/thumb/{it["src"]}.jpg" alt="{label}">\n'
            f'{indent}  <figcaption>{n:02d}</figcaption>\n'
            f'{indent}</button>')
    return "\n".join(out)

def strip(group, indent="        "):
    cap, out = esc(CAPTION[group]), []
    for n, it in enumerate(man[group], 1):
        out.append(
            f'{indent}<img loading="lazy" decoding="async" src="assets/thumb/{it["src"]}.jpg"\n'
            f'{indent}     width="{it["w"]}" height="{it["h"]}" alt="{cap} — {n:02d}">')
    return "\n".join(out)

body = open(os.path.join(ROOT, "_body.part"), encoding="utf-8").read()
body = re.sub(r"[ \t]*<!--GRID:([a-z]+)-->",  lambda m: cells(m.group(1)),  body)
body = re.sub(r"[ \t]*<!--STRIP:([a-z]+)-->", lambda m: strip(m.group(1)),  body)
assert "<!--GRID:" not in body and "<!--STRIP:" not in body, "unexpanded marker left in the page"

head = open(os.path.join(ROOT, "_head.part"), encoding="utf-8").read()
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        + head.rstrip() + "\n</head>\n<body>\n\n" + body.strip() + "\n\n</body>\n</html>\n")

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(page)
n_cells = page.count('class="cell"')
print(f"index.html written — {len(page)/1024:.0f} KB, {n_cells} gallery frames")
