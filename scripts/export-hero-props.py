#!/usr/bin/env python3
"""Export supplied transparent props for the existing v89 browser stage.

Keep the full camera frame and contact shadows so object-fit matches the scene.
Only split the empty central gutter and downsample; never modify the masters.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('delivery', type=Path, help='V89_PROPS_ONLY_20261028/delivery')
    args = parser.parse_args()
    records = []
    for version, suffix, size in [
        ('props_v55_16x9', '', (1920, 1080)),
        ('props_v54_A3', '-mobile', (1023, 1440)),
    ]:
        source = args.delivery / version / 'layers/17_foreground_props.png'
        original = Image.open(source).convert('RGBA')
        w, h = original.size
        # The native delivery has no foreground pixels in this central gutter.
        assert original.getchannel('A').crop((w // 2 - 1, 0, w // 2 + 1, h)).getbbox() is None
        for prop, box in [('gifts', (0, 0, w // 2, h)), ('snowman', (w // 2, 0, w, h))]:
            # Both viewports use the horizontal snowman; portrait layout is
            # handled by the browser without altering its proportions.
            if suffix and prop == 'snowman':
                continue
            layer = Image.new('RGBA', original.size)
            layer.paste(original.crop(box), box[:2])
            output = ROOT / 'img/motion' / f'marc-{prop}{suffix}.webp'
            layer.resize(size, Image.Resampling.LANCZOS).save(output, quality=90, method=6)
            records.append({
                'path': str(output.relative_to(ROOT)),
                'source': f'{version}/layers/17_foreground_props.png',
                'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'outputSha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                'width': size[0], 'height': size[1], 'bytes': output.stat().st_size,
                'encoding': 'WebP quality 90; full camera frame; original contact shadows',
            })
    (ROOT / 'config/hero-props.json').write_text(json.dumps(records, indent=2) + '\n')
    print(f'Exported {len(records)} layers: {sum(r["bytes"] for r in records):,} bytes total')


if __name__ == '__main__':
    main()
