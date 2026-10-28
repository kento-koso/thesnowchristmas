#!/usr/bin/env python3
"""Offline release checks. No external requests, form submissions or payments."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from build import ROOT, PAGES, build

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.images=[]; self.lang=None
        self.body=False; self.skip=0; self.text=[]
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='body':self.body=True
        if tag in ('style','script'):self.skip+=1
        if 'id' in a:self.ids.append(a['id'])
        if tag=='img':self.images.append(a)
        for name in ('src','href'):
            if name in a:self.links.append((tag,name,a[name]))
        if 'srcset' in a:
            self.links.extend((tag,'src',x.strip().split()[0]) for x in a['srcset'].split(',') if x.strip())
    def handle_endtag(self, tag):
        if tag=='body':self.body=False
        if tag in ('style','script'):self.skip-=1
    def handle_data(self, data):
        if self.body and not self.skip:self.text.append(data)
    def copy(self):
        return re.sub(r'\s+','',''.join(self.text))

def errors_for_pages(root=ROOT):
    errors=[]
    pages={name:Page((root/name).read_text()) for name in PAGES}
    for name,page in pages.items():
        if page.lang!='ja':errors.append(f'{name}: missing Japanese language')
        duplicates=[id for id,count in Counter(page.ids).items() if count>1]
        if duplicates:errors.append(f'{name}: duplicate IDs {duplicates}')
        if '{{' in (root/name).read_text():errors.append(f'{name}: unresolved template token')
        for image in page.images:
            if not image.get("width") or not image.get("height"):
                errors.append(f'{name}: image missing reserved dimensions: {image.get("src")}')
            if 'alt' not in image:errors.append(f'{name}: image missing alt: {image.get("src")}')
        for tag,attr,url in page.links:
            parsed=urlsplit(url)
            if parsed.scheme or parsed.netloc:continue
            path=unquote(parsed.path)
            target=(root/name).parent/path if path else root/name
            if target.is_dir():target=target/'index.html'
            if not target.is_file():
                errors.append(f'{name}: missing {url}');continue
            if tag=='a' and parsed.fragment and target.suffix=='.html':
                ids=Page(target.read_text()).ids
                if unquote(parsed.fragment) not in ids:errors.append(f'{name}: missing anchor {url}')
    for css in root.glob('*.css'):
        for match in re.finditer(r"url\((?:\"([^\"]*)\"|'([^']*)'|([^)]*))\)",css.read_text()):
            url=next(group for group in match.groups() if group is not None).strip()
            parsed=urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            if not (css.parent/unquote(parsed.path)).is_file():errors.append(f'{css.name}: missing {url}')
    return errors

def check():
    build(check=True)
    errors=errors_for_pages()
    fixture=json.loads((ROOT/'tests/content-baseline.json').read_text())
    for name,text in fixture.items():
        if Page((ROOT/name).read_text()).copy()!=text:
            errors.append(f'{name}: approved copy changed; review before updating baseline')
    budgets=json.loads((ROOT/'config/budgets.json').read_text())
    assets=json.loads((ROOT/'config/assets.json').read_text())
    total=sum((ROOT/item['path']).stat().st_size for item in assets.values())
    if total>budgets['optimizedImagesBytes']:errors.append('Optimized image budget exceeded')
    for name,limit in budgets['files'].items():
        if (ROOT/name).stat().st_size>limit:errors.append(f'{name}: size budget exceeded')
    for js in list(ROOT.glob('*.js'))+[ROOT/'config/event.js']:
        result=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
        if result.returncode:errors.append(result.stderr)
    result=subprocess.run(['node',str(ROOT/'scripts/check-css.mjs')],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:errors.append(result.stderr)
    if errors:raise ValueError('\n'.join(errors))
    print(f'PASS: {len(PAGES)} pages, local links/anchors, copy baseline, CSS/JS syntax, asset budgets, generated files')

if __name__=='__main__':
    try:check()
    except (ValueError,OSError) as e:sys.exit(str(e))
