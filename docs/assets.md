# Asset register

| Asset group | Purpose / origin | Current use |
| --- | --- | --- |
| `img/motion/marc-scene*.jpg` | Prepared MARC scene renders; user identifies v89 as latest master | Optimized derivatives in hero; desktop/mobile source selection |
| `img/design/snow-christmas-logo.png` | Supplied event logo export | Lossless WebP derivative; no shape/color changes |
| `img/logo/meguro-marc-wordmark-white.svg` | Supplied Illustrator outline; details in `img/logo/README.md` | Hero venue wordmark |
| `img/motion/foreground-branches.webp` | Snowy branch artwork | Reused for forest opening and margins |
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
