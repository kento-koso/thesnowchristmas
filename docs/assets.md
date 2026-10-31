# Asset register

| Asset group | Purpose / origin | Current use |
| --- | --- | --- |
| `img/motion/marc-scene*.jpg` | v89 camera/compositor with supplied 2026-11-01 native TREE_GARDEN plates removing both market snowmen | Optimized derivatives in hero; desktop/mobile source selection |
| `img/design/snow-christmas-logo.png` | Supplied event logo export | Lossless WebP derivative; no shape/color changes |
| `img/logo/meguro-marc-wordmark-white.svg` | Supplied Illustrator outline; details in `img/logo/README.md` | Hero venue wordmark |
| `img/motion/foreground-branches.webp` | Snowy branch artwork | Reused for forest opening and margins |
| `img/motion/marc-gifts*.webp`, `marc-snowman*.webp` | Supplied foreground renders: v55 corrected-contact 16:9 snowman on all screens; v55 desktop / v54 A3 mobile gifts; original v89 camera | Hero 2.5D layers with ground-pivot rocking; not a live mesh |
| `img/m/`, `img/talk/` | Photography and event material; credits retained in page text | Optimized where beneficial, lazy loaded below hero |
| `img/winter/*.svg` | Code-native winter decoration | Borders, snow banks and crystals |
| `img/models/*.bin`, `snow-decor.js` | Blender-derived experimental decorations; export notes retained | Not loaded by current pages |
| `img/design/snow-village*`, old KV/fir assets | Earlier prepared artwork | Retained; not automatically deleted |

`config/assets.json` records each optimized file, original path, dimensions, encoding and byte sizes. Original sources are never overwritten. The logo uses lossless encoding; JPEG photographs use WebP quality 88 at original dimensions. Only conversions saving at least 15% are selected. Source checksums in derivative names invalidate image caches.

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/optimize-images.py --write
npm run format
npm run build
npm run check
```

Visually inspect photographic derivatives after export. The normal build/check process does not need Pillow. The script also updates references in templates, partials and CSS. Old derivatives may remain on disk after a source replacement; remove only after checking references.

A filename alone is not evidence of Blender master version or licensing. The relationship between prepared renders and the supplied v89 master should be retained with future export records. Existing attribution is preserved; this refactor does not assert a new rights clearance.

Foreground exports are recorded in `config/hero-props.json` with source/output SHA-256 hashes and dimensions. Run `python3 scripts/export-hero-props.py /path/to/V89_PROPS_ONLY_20261028/delivery` to reproduce them. The export splits the transparent central gutter, retains the full camera frame and local contact shadows, and downsamples to WebP. Three files total about 79 KB; each viewport loads two files. The mobile snowman reuses the 16:9 export, fitted around its portrait foot position. A CSS-only 1.15 vertical scale corrects its squat appearance on the site, anchored at the native foot point; the source image is unchanged. Native masters stay in the art delivery folder. Motion shares the existing animation loop, pause/reduced-motion state, and offscreen/hidden-page suspension.

Background exports are recorded in `config/hero-backgrounds.json`. They use the supplied `market_snowmen_removal_v74_20261101/patched_plates` replacement for `TREE_GARDEN` in the v89 `FINAL_*_COMPOSITE` scenes. Export at the existing web dimensions, with falling-snow, volume and crystal layers disabled so the site continues to animate these independently. Foreground gift/snowman layers and their animation are unchanged. The scene JPEGs are replaceable web exports; original Blender masters and native plates remain outside this repository.
