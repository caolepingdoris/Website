# Doris Cao — portfolio site

Static site. `index.html` is the deliverable; open it directly, or drop the whole
folder on Netlify / Vercel / GitHub Pages. No build step needed to *serve* it.

## Layout

| # | Section | Contents |
|---|---|---|
| 01 | About | artist statement |
| 02 | Director | Levi By The Sea · Unsolved Problem · How Can I Become A Circle |
| 03 | Producer | The Poem of Future · К МОРЮ · Boylston Film Festival |
| 04 | Gaffer | Ruthless · The Rose Garden (one plate, one card) · Whispering Room · Ann Arbor · Come On In |
| 05 | Installation | Vivid Dream · Do You Feel It · installation views |
| 06 | Photography | eleven series, each with its own camera credit |
| 07 | Credits | filterable crew list |
| 08 | Contact | email only — LinkedIn and Instagram live in the masthead icons |

Grouping follows the three reference decks: `Director Work.pdf`,
`Producing Work.pdf`, `Photography.pdf`.

The cover is a two-frame diptych — `COVER` in `build_assets.py` names the two
source images, currently the pair from Vivid Dream.

## Regenerating

```bash
python build_assets.py    # website/ originals -> assets/full + assets/thumb + manifest.json
python build_page.py      # _head.part + _body.part + manifest -> index.html
```

`build_page.py` refuses to run if `index.html` is newer than the two `.part`
files, so hand edits are not silently thrown away — pass `--force` to override.
Edit `_head.part` (styles) and `_body.part` (markup) rather than `index.html`.

Which source images go where is set by `GROUPS` in `build_assets.py`; the
comment above it lists the frames deliberately left out as repeats.

## Links

All outbound URLs live in one `window.LINKS` object at the top of `_body.part`.
Anything left as `""` hides its own link instead of becoming a dead one — the
per-project **Watch** buttons and the résumé PDF are still empty.
