# -*- coding: utf-8 -*-
"""
Rebuilds site/assets/ from the originals in site/website/.
Run:  python build_assets.py
Safe to re-run; it overwrites.

Grouping follows the three reference decks:
  Director Work.pdf · Producing Work.pdf · Photography.pdf
"""
import os, json, sys
from PIL import Image, ImageOps

SRC   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "website")
ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
FULL, THUMB = (os.path.join(ASSET, d) for d in ("full", "thumb"))
for d in (FULL, THUMB): os.makedirs(d, exist_ok=True)

FULL_EDGE, THUMB_EDGE, HERO_EDGE = 1800, 760, 2600

srcfiles = sorted(f for f in os.listdir(SRC) if f.lower().endswith((".jpg", ".jpeg", ".png")))
srcfiles = [f for f in srcfiles if not f.startswith("Creative Greyscale")]
deck     = sorted((f for f in os.listdir(SRC) if f.startswith("Creative Greyscale")),
                  key=lambda f: int(f.rsplit("-", 1)[1].split(".")[0]))

# Indices left out on purpose:
#   7, 27, 79 .......... 3-up arrangements of frames already shown in Cities
#   38-42, 46 .......... 2-up / 4-up arrangements of the Do You Feel It prints
#   50 ................. second pass of the elderly-hands frame kept at 43
#   57 ................. frame-for-frame repeat of the event photograph at 56
#   66 ................. cut from Boylston at the artist's request
#   82 ................. repeat of the Cities frame at 4
#   70 ................. same frame as 24, at a lower resolution
#   52 ................. already printed inside the Portraits plate
GROUPS = {
    # ---- Director -------------------------------------------------
    "levi":      ([8, 18, 23, 24, 83, 69],              "Levi By The Sea"),
    "circle":    ([84, 87, 85],                         "How Can I Become A Circle"),
    "unsolved":  ([71, 72, 73, 74],                     "Unsolved Problem"),
    # ---- Producer -------------------------------------------------
    "poem":      ([81, 9, 31, 25],                      "The Poem of Future"),
    "kmoryu":    ([5, 12, 75, 10],                      "К МОРЮ"),
    "boylston":  ([86, 95, 28, 67],                     "Boylston Film Festival"),
    # ---- Installation ---------------------------------------------
    "vivid":     ([89, 90, 88, 91, 92, 93, 94],         "Vivid Dream"),
    "feel":      ([43, 32, 33, 34, 35, 36, 37],         "Do You Feel It"),
    "installwide": ([45],                               "Do You Feel It, installation view"),
    # ---- Photography, by series -----------------------------------
    "bostonl":   ([48, 49, 51, 1, 2, 0],                "Boston"),
    "la":        ([3, 13, 15, 17, 21, 26, 29, 77],      "Los Angeles"),
    "cities":    ([4, 6, 11, 14, 16, 22, 30, 80],       "Cities"),
    "chinatown": ([19, 20, 68, 76, 78],                 "Chinatown"),
    "event":     ([53, 54, 55, 56, 58, 59, 60, 61, 62, 63, 64], "Event photography"),
}
# masthead hero — the puddle-reflection photograph
HERO = 47

# "Do You Feel It, installation view" — full-resolution gallery photos,
# sourced straight from the exhibition folder rather than the deck plates.
EXTERNAL = {
    "install": [
        r"C:\照片\Gallery\Do You Feel It\_DWK0986-HDR.jpg",
        r"C:\照片\Gallery\Do You Feel It\_DWK0991-HDR.jpg",
    ],
}

def emit(path, dst_base, edge, quality):
    im = ImageOps.exif_transpose(Image.open(path))
    if im.mode not in ("RGB", "L"): im = im.convert("RGB")
    im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(dst_base + ".jpg", "JPEG", quality=quality, optimize=True, progressive=True)
    return im.width, im.height

manifest = {}
for group, (idxs, label) in GROUPS.items():
    items = []
    for n, i in enumerate(idxs, 1):
        src  = os.path.join(SRC, srcfiles[i])
        slug = f"{group}-{n:02d}"
        w, h = emit(src, os.path.join(FULL,  slug), FULL_EDGE, 82)
        emit(src, os.path.join(THUMB, slug), THUMB_EDGE, 76)
        items.append({"src": slug, "w": w, "h": h, "alt": f"{label} — {n}"})
    manifest[group] = items
    print(f"{group:10s} {len(items):2d} frames")

for group, paths in EXTERNAL.items():
    items = []
    for n, path in enumerate(paths, 1):
        slug = f"{group}-{n:02d}"
        w, h = emit(path, os.path.join(FULL,  slug), FULL_EDGE, 82)
        emit(path, os.path.join(THUMB, slug), THUMB_EDGE, 76)
        items.append({"src": slug, "w": w, "h": h, "alt": f"Do You Feel It, installation view — {n}"})
    manifest[group] = items
    print(f"{group:10s} {len(items):2d} frames (external)")

hw, hh = emit(os.path.join(SRC, srcfiles[HERO]), os.path.join(FULL, "hero"), HERO_EDGE, 84)
emit(os.path.join(SRC, srcfiles[HERO]), os.path.join(THUMB, "hero"), THUMB_EDGE, 76)
manifest["hero"] = [{"src": "hero", "w": hw, "h": hh, "alt": "Seascape at dusk"}]
print(f"{'hero':10s}  1 frame  {hw}x{hh}")

# Deck slides. 4-7 are the gaffer / crew titles; 9-14 are photography series
# that exist only as the artist's own composed plates.
deckmap = {4: "come-on-in", 5: "whispering-room", 6: "ann-arbor",
           7: "ruthless-rose", 9: "rainy-new-york", 10: "manchester",
           11: "portraits", 12: "dream-sequence", 13: "boston-fuji",
           14: "behind-the-scene"}
slides = {}
for f in deck:
    n = int(f.rsplit("-", 1)[1].split(".")[0])
    if n not in deckmap: continue          # 8 is the section title card
    slug = "slide-" + deckmap[n]
    w, h = emit(os.path.join(SRC, f), os.path.join(FULL, slug), FULL_EDGE, 84)
    emit(os.path.join(SRC, f), os.path.join(THUMB, slug), THUMB_EDGE, 78)
    slides[deckmap[n]] = {"src": slug, "w": w, "h": h}
manifest["deck"] = slides
print(f"{'deck':10s} {len(slides):2d} plates")

with open(os.path.join(ASSET, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=1, ensure_ascii=False)

tot = sum(os.path.getsize(os.path.join(r, f))
          for r, _, fs in os.walk(ASSET) for f in fs)
print(f"\nassets/ total {tot/1e6:.1f} MB")
