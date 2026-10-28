#!/usr/bin/env python3
"""Encode referenced raster images without overwriting originals. Requires Pillow.
PNG -> lossless WebP; JPEG -> WebP quality 88. Keep original if savings < 15%.
Only rewrites local source references with --write; review output visually.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write', action='store_true')
args = parser.parse_args()
files = list((ROOT/'templates').rglob('*.html')) + list((ROOT/'partials').glob('*.html')) + list(ROOT.glob('*.css'))
manifest_path = ROOT/'config/assets.json'
previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
content = '\n'.join(p.read_text() for p in files)
paths = set(re.findall(r'img/(?!optimized/)[\w/.-]+\.(?:png|jpg|jpeg)', content))
paths.update(previous)
manifest = {}
for name in sorted(paths):
    original = ROOT/name
    if not original.is_file():
        continue
    digest = hashlib.sha256(original.read_bytes()).hexdigest()[:12]
    target = Path('img/optimized') / Path(name).relative_to('img').with_suffix(f'.{digest}.webp')
    destination = ROOT/target
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(original) as source:
        image = source.convert('RGBA' if 'A' in source.getbands() else 'RGB')
        image.save(destination, 'WEBP', lossless=original.suffix.lower()=='.png', quality=88, method=6)
    if destination.stat().st_size >= original.stat().st_size * .85:
        destination.unlink()
        continue
    manifest[name] = {'path':str(target),'sourceBytes':original.stat().st_size,'outputBytes':destination.stat().st_size,
                      'width':image.width,'height':image.height,'mode':'lossless' if original.suffix.lower()=='.png' else 'quality-88'}
if args.write:
    for p in files:
        text = p.read_text()
        for source, item in manifest.items():
            old = previous.get(source, {}).get('path',source)
            text = text.replace(old, item['path']).replace(source,item['path'])
        p.write_text(text)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'images':len(manifest),'originalBytes':sum(x['sourceBytes'] for x in manifest.values()),
                  'optimizedBytes':sum(x['outputBytes'] for x in manifest.values())},indent=2))
