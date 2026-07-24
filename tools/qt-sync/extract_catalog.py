"""Extract the canonical product catalog from the built quality-tooling site.

Parses all HTML pages + assets/search-index.js and emits catalog.json:
every listing id with its curated display title, price, and every placement
(catalog-page card, category feature card, search-index entry), including the
section each catalog card sits in.

catalog.json is the committed source of truth the Etsy sync diffs against.

Usage: python extract_catalog.py            (from tools/qt-sync/)
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'sites' / 'quality-tooling'

# ---------------------------------------------------------------- helpers
def unescape(s):
    return (s.replace('&#8243;', '″').replace('&amp;', '&')
             .replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
             .replace('&#39;', "'"))

# Type A: full-card link on catalog pages
PCARD = re.compile(
    r'<a class="card pcard reveal" href="https://www\.etsy\.com/listing/(?P<id>\d+)"[^>]*>'
    r'<div class="ph"><img src="(?P<img>[^"]*)" alt="(?P<alt>.*?)" loading="lazy"[^>]*></div>\s*'
    r'<div class="info"><h3>(?P<title>.*?)</h3><span class="price">\$(?P<price>[\d,.]+)</span>',
    re.S)

# Type B: feature card with local image + "Order on Etsy" link
FCARD = re.compile(
    r'<div class="card reveal"><div class="ph(?: tall)?"><img src="(?P<img>assets/[^"]*)" alt="(?P<alt>.*?)" loading="lazy"[^>]*></div>\s*'
    r'<div class="info"><h3>(?P<title>.*?)</h3><span class="price">\$(?P<price>[\d,.]+)</span>'
    r'(?:<p>(?P<blurb>.*?)</p>)?'
    r'<a class="order" href="https://www\.etsy\.com/listing/(?P<id>\d+)"',
    re.S)

# Section heading on catalog pages: <h2 class="sec" ...>Name <span ...>(N)</span></h2>
SECTION = re.compile(r'<h2 class="sec"[^>]*>(?P<name>[^<]+?)\s*<span[^>]*>\((?P<count>\d+)\)</span></h2>')

def section_at(sections, pos):
    cur = None
    for s_pos, name in sections:
        if s_pos < pos:
            cur = name
        else:
            break
    return cur

# ---------------------------------------------------------------- extract
products = {}   # id -> {title, price, placements: [...]}
def add(pid, title, price, placement):
    p = products.setdefault(pid, {'title': title, 'price': price, 'placements': []})
    p['placements'].append(placement)

pages = sorted(SITE.glob('*.html'))
for page in pages:
    html = page.read_text(encoding='utf-8')
    fname = page.name
    sections = [(m.start(), unescape(m.group('name').strip())) for m in SECTION.finditer(html)]
    for m in PCARD.finditer(html):
        add(m['id'], unescape(m['title']), m['price'], {
            'file': fname, 'kind': 'pcard',
            'section': section_at(sections, m.start()),
            'img': m['img'], 'alt': m['alt']})
    for m in FCARD.finditer(html):
        add(m['id'], unescape(m['title']), m['price'], {
            'file': fname, 'kind': 'feature',
            'img': m['img'], 'title': unescape(m['title'])})

# search index
idx_path = SITE / 'assets' / 'search-index.js'
idx_src = idx_path.read_text(encoding='utf-8')
idx_json = re.search(r'window\.QT_INDEX=(\[.*\]);', idx_src, re.S).group(1)
index = json.loads(idx_json)
page_entries = []
for e in index:
    m = re.match(r'https://www\.etsy\.com/listing/(\d+)$', e['u'])
    if m:
        pid = m.group(1)
        price = e['p'].lstrip('$')
        p = products.setdefault(pid, {'title': e['t'], 'price': price, 'placements': []})
        p['placements'].append({'file': 'assets/search-index.js', 'kind': 'search', 'title': e['t'], 'price': price})
    else:
        page_entries.append(e)

# section inventory per catalog page (for insertion targeting + count maintenance)
section_inventory = {}
for page in ['catalog.html', 'catalog-2.html', 'catalog-3.html']:
    html = (SITE / page).read_text(encoding='utf-8')
    section_inventory[page] = [
        {'name': unescape(m.group('name').strip()), 'count': int(m.group('count'))}
        for m in SECTION.finditer(html)]

# ---------------------------------------------------------------- report + write
out = {
    'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'site': 'sites/quality-tooling',
    'section_inventory': section_inventory,
    'search_page_entries': page_entries,
    'products': dict(sorted(products.items(), key=lambda kv: kv[1]['title'].lower())),
}
Path(__file__).with_name('catalog.json').write_text(
    json.dumps(out, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')

n_pcard = sum(1 for p in products.values() for pl in p['placements'] if pl['kind'] == 'pcard')
n_feat  = sum(1 for p in products.values() for pl in p['placements'] if pl['kind'] == 'feature')
n_search = sum(1 for p in products.values() for pl in p['placements'] if pl['kind'] == 'search')
print(f'products: {len(products)}  pcards: {n_pcard}  feature-cards: {n_feat}  search-entries: {n_search}')

# consistency: price agreement across placements of the same id
for pid, p in products.items():
    prices = {pl.get('price') for pl in p['placements'] if pl.get('price')} | {p['price']}
    seen = set()
    for pl in p['placements']:
        pass
    card_prices = set()
    for pl in p['placements']:
        if 'price' in pl and pl['price']:
            card_prices.add(pl['price'])
    if len(card_prices | {p['price']}) > 1:
        print(f'  NOTE {pid} {p["title"]!r}: differing prices across placements: {card_prices | {p["price"]}}')
