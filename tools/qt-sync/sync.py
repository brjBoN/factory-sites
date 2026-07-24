"""Etsy -> site catalog sync for sites/quality-tooling (the CLAUDE.md catalog pattern).

Inputs (same directory):
  harvest.json   live Etsy shop state (written by the browser harvest step, see README)
  catalog.json   canonical site catalog (extract_catalog.py seeds it; sync.py maintains it)
  curation.json  human-approved additions {id: {title, section}}

What syncs automatically:
  * price changes         -> every placement (catalog cards, feature cards, search index)
  * primary-image changes -> catalog cards (Etsy CDN hotlinks)
  * re-listed products    -> href swap (old id gone + new id shares the same image uid)
  * delisted products     -> catalog card removed + section count decremented
                             (feature cards are never auto-removed: flagged in report)
  * curated additions     -> new catalog card, alphabetical slot, section count, search index

Everything ambiguous (new physical items without curation, duplicate listings,
raw-title drift, delisted products with feature placements) goes to sync-report.md.

Policy exclusions (never added, never reported as pending): digital files
(PNG/SVG/sublimation), print-on-demand merch, RUSH ORDER / WHOLESALE listings.

Usage:
  python sync.py             dry run: prints plan, writes sync-report.md
  python sync.py --apply     patch site files + catalog.json
  python sync.py --selftest  exercise price/removal/add/relist paths in memory
"""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SITE = ROOT / 'sites' / 'quality-tooling'

DIGITAL = re.compile(r'PNG|SVG|Sublimation|Cricut|JPG', re.I)
MERCH   = re.compile(r'T-shirt|Sweatshirt|pint glass|Garment-Dyed', re.I)
ADMIN   = re.compile(r'^RUSH ORDER$|WHOLESALE', re.I)

SECTION_RE = re.compile(r'<h2 class="sec"[^>]*>(?P<name>[^<]+?)\s*<span[^>]*>\((?P<count>\d+)\)</span></h2>')
PCARD_RE = re.compile(
    r'<a class="card pcard reveal" href="https://www\.etsy\.com/listing/(?P<id>\d+)"[^>]*>'
    r'<div class="ph"><img src="(?P<img>[^"]*)"[^>]*></div>\s*'
    r'<div class="info"><h3>(?P<title>.*?)</h3><span class="price">\$(?P<price>[\d,.]+)</span>', re.S)

ARROW = ('<svg class="arr" width="25" height="12" viewBox="0 0 26 12" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M1 6h22M18.5 1.8 23 6l-4.5 4.2"/></svg>')

def esc_text(s):   # for h3 text nodes
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def esc_attr(s):   # for attribute values
    return esc_text(s).replace('"', '&quot;')
def uid_of(url):
    m = re.search(r'/il/[0-9a-f]+/(\d+)/', url or '')
    return m.group(1) if m else None
def big_img(url):  # upgrade any il_WxH variant to 800x800 for card sharpness
    return re.sub(r'il_\d+x\d+\.', 'il_800x800.', url)

def make_card(pid, title, price, img, eol):
    return (f'<a class="card pcard reveal" href="https://www.etsy.com/listing/{pid}" target="_blank" rel="noopener">'
            f'<div class="ph"><img src="{esc_attr(img)}" alt="{esc_attr(title)}" loading="lazy" referrerpolicy="no-referrer"></div>{eol}'
            f'<div class="info"><h3>{esc_text(title)}</h3><span class="price">${price}</span>'
            f'<span class="order">View on Etsy {ARROW}</span></div></a>')

def card_span(html, m):
    """Full extent of a pcard: match start .. its closing </a>."""
    end = html.index('</a>', m.end()) + 4
    return m.start(), end

def section_cards(html, section):
    """Ordered [(match, start, end)] of pcards belonging to a named section."""
    secs = [(m.start(), m.group('name').strip()) for m in SECTION_RE.finditer(html)]
    out = []
    for m in PCARD_RE.finditer(html):
        cur = None
        for pos, name in secs:
            if pos < m.start():
                cur = name
            else:
                break
        if cur == section:
            out.append((m, *card_span(html, m)))
    return out

def bump_count(html, section, delta):
    def sub(m):
        if m.group('name').strip() == section:
            return m.group(0).replace(f"({m.group('count')})", f"({int(m.group('count')) + delta})")
        return m.group(0)
    return SECTION_RE.sub(sub, html)

def rewrite_price(html, pid, new_price):
    """Update the price inside every card (pcard or feature) tied to pid."""
    n = 0
    # pcards: price sits inside the card span
    for m in list(PCARD_RE.finditer(html)):
        if m.group('id') == pid:
            s, e = card_span(html, m)
            seg = re.sub(r'<span class="price">\$[\d,.]+</span>',
                         f'<span class="price">${new_price}</span>', html[s:e], count=1)
            html = html[:s] + seg + html[e:]
            n += 1
    # feature cards: price precedes the order link that carries the id
    fpat = re.compile(r'(<span class="price">)\$[\d,.]+(</span>(?:<p>.*?</p>)?<a class="order" '
                      r'href="https://www\.etsy\.com/listing/' + pid + r'")', re.S)
    html, k = fpat.subn(lambda m: m.group(1) + '$' + new_price + m.group(2), html)
    return html, n + k

def rewrite_href(html, old_id, new_id):
    return html.replace(f'https://www.etsy.com/listing/{old_id}', f'https://www.etsy.com/listing/{new_id}')

def rewrite_img(html, pid, new_img):
    n = 0
    for m in list(PCARD_RE.finditer(html)):
        if m.group('id') == pid:
            s, e = card_span(html, m)
            seg = re.sub(r'(<div class="ph"><img src=")[^"]*(")', lambda mm: mm.group(1) + esc_attr(new_img) + mm.group(2), html[s:e], count=1)
            html = html[:s] + seg + html[e:]
            n += 1
    return html, n

def remove_card(html, pid, section):
    cards = section_cards(html, section)
    for m, s, e in cards:
        if m.group('id') == pid:
            return bump_count(html[:s] + html[e:], section, -1), True
    return html, False

def insert_card(html, section, card_html, title):
    cards = section_cards(html, section)
    if not cards:
        raise RuntimeError(f'section {section!r} has no cards to anchor on')
    for m, s, e in cards:
        if m.group('title') > title:          # plain codepoint sort, matches site order
            return bump_count(html[:s] + card_html + html[s:], section, +1)
    _, _, last_end = cards[-1]
    return bump_count(html[:last_end] + card_html + html[last_end:], section, +1)

def fix_malformed_alts(html):
    """Repair alt attributes that contain raw double quotes (pre-existing defect)."""
    pat = re.compile(r'alt="(?P<val>[^<>]*?)" loading="lazy"')
    def sub(m):
        v = m.group('val')
        if '"' in v:
            return f'alt="{v.replace(chr(34), "&quot;")}" loading="lazy"'
        return m.group(0)
    return pat.sub(sub, html)

# ------------------------------------------------------------------ validators
def validate_site(files, catalog):
    errs = []
    all_pcards = {}
    for fname, html in files.items():
        # section counts == cards in section, alphabetical order
        secs = [(m.start(), m.group('name').strip(), int(m.group('count'))) for m in SECTION_RE.finditer(html)]
        for pos, name, count in secs:
            cards = section_cards(html, name)
            if len(cards) != count:
                errs.append(f'{fname}: section {name!r} count ({count}) != cards ({len(cards)})')
            titles = [m.group('title') for m, _, _ in cards]
            if titles != sorted(titles):
                errs.append(f'{fname}: section {name!r} not alphabetical: {titles}')
        for m in PCARD_RE.finditer(html):
            all_pcards.setdefault(m.group('id'), []).append(fname)
        # attribute hygiene: no alt with raw quotes
        for m in re.finditer(r'alt="([^"<>]*)"([^>]*)>', html):
            pass
        if re.search(r'alt="[^"<>]*"[A-Za-z]', html):
            errs.append(f'{fname}: malformed alt attribute (raw quote) present')
        if re.search(r'<span class="price">\$(?![\d,]+\.\d\d<)', html):
            errs.append(f'{fname}: malformed price present')
    dupes = {pid: fs for pid, fs in all_pcards.items() if len(fs) > 1}
    if dupes:
        errs.append(f'duplicate pcards: {dupes}')
    return errs

def regen_search_index(catalog):
    entries = []
    for pid, p in sorted(catalog['products'].items(), key=lambda kv: kv[1]['title']):
        entries.append({'t': p['title'], 'u': f'https://www.etsy.com/listing/{pid}', 'p': f"${p['price']}"})
    entries += catalog['search_page_entries']
    return 'window.QT_INDEX=' + json.dumps(entries, ensure_ascii=False) + ';'

# ------------------------------------------------------------------ diff
def compute_diff(catalog, harvest, curation):
    prods = catalog['products']
    hv = {i['id']: i for i in harvest['items']}
    d = {'price': [], 'img': [], 'gone': [], 'relist': [], 'adds': [], 'dups': [],
         'review': [], 'excluded': [], 'title_drift': []}
    active_uids = {}
    for pid, p in prods.items():
        h = hv.get(pid)
        if h:
            active_uids.setdefault(uid_of(h['img']), pid)
    for pid, p in prods.items():
        h = hv.get(pid)
        if not h:
            d['gone'].append(pid); continue
        if h['price'] != p['price']:
            d['price'].append((pid, p['price'], h['price']))
        site_img = next((pl['img'] for pl in p['placements'] if pl['kind'] == 'pcard'), None)
        if site_img and uid_of(site_img) and uid_of(h['img']) and uid_of(site_img) != uid_of(h['img']):
            d['img'].append((pid, big_img(h['img'])))
        if p.get('raw_title') and p['raw_title'] != h['title']:
            d['title_drift'].append((pid, p['raw_title'], h['title']))
    new = {pid: h for pid, h in hv.items() if pid not in prods}
    for pid, h in sorted(new.items(), key=lambda kv: kv[1]['title']):
        if DIGITAL.search(h['title']) or MERCH.search(h['title']) or ADMIN.search(h['title']):
            d['excluded'].append((pid, h['title'])); continue
        # re-list: pairs with a gone product sharing the image uid
        paired = None
        for gpid in d['gone']:
            gp = prods[gpid]
            g_uid = uid_of(next((pl['img'] for pl in gp['placements'] if pl['kind'] == 'pcard'), '') or '')
            if g_uid and g_uid == uid_of(h['img']):
                paired = gpid; break
        if paired:
            d['relist'].append((paired, pid)); d['gone'].remove(paired); continue
        if pid in curation.get('add', {}):
            c = curation['add'][pid]
            d['adds'].append((pid, c['title'], c['section'], h)); continue
        # duplicate listing of a product already on site (same photo, both active)
        twin = active_uids.get(uid_of(h['img']))
        if twin:
            d['dups'].append((pid, h['title'], twin, prods[twin]['title'])); continue
        d['review'].append((pid, h['title'], h['price']))
    return d

# ------------------------------------------------------------------ main
def run(apply=False):
    catalog = json.loads((HERE / 'catalog.json').read_text(encoding='utf-8'))
    harvest = json.loads((HERE / 'harvest.json').read_text(encoding='utf-8'))
    curation = json.loads((HERE / 'curation.json').read_text(encoding='utf-8'))
    hv = {i['id']: i for i in harvest['items']}
    d = compute_diff(catalog, harvest, curation)

    page_of = {}
    for page, secs in catalog['section_inventory'].items():
        for s in secs:
            page_of[s['name']] = page

    fnames = sorted({pl['file'] for p in catalog['products'].values() for pl in p['placements']
                     if pl['file'].endswith('.html')} | set(catalog['section_inventory']))
    files = {f: (SITE / f).read_text(encoding='utf-8') for f in fnames}
    eol = '\r\n' if '\r\n' in files['catalog.html'] else '\n'

    changed = set()
    # 1. malformed-alt repair (idempotent hygiene pass)
    for f in fnames:
        fixed = fix_malformed_alts(files[f])
        if fixed != files[f]:
            files[f] = fixed; changed.add(f)
    # 2. prices
    for pid, old, new in d['price']:
        p = catalog['products'][pid]
        for f in {pl['file'] for pl in p['placements'] if pl['file'].endswith('.html')}:
            files[f], n = rewrite_price(files[f], pid, new)
            if n: changed.add(f)
        p['price'] = new
    # 3. images
    for pid, new_img in d['img']:
        for pl in catalog['products'][pid]['placements']:
            if pl['kind'] == 'pcard':
                files[pl['file']], n = rewrite_img(files[pl['file']], pid, new_img)
                if n: changed.add(pl['file']); pl['img'] = new_img
    # 4. re-lists (href swap everywhere, id key moves)
    for old_id, new_id in d['relist']:
        p = catalog['products'].pop(old_id)
        for f in {pl['file'] for pl in p['placements'] if pl['file'].endswith('.html')}:
            files[f] = rewrite_href(files[f], old_id, new_id); changed.add(f)
        if hv[new_id]['price'] != p['price']:
            for f in {pl['file'] for pl in p['placements'] if pl['file'].endswith('.html')}:
                files[f], _ = rewrite_price(files[f], new_id, hv[new_id]['price'])
            p['price'] = hv[new_id]['price']
        catalog['products'][new_id] = p
    # 5. removals (pcards only; feature placements flagged)
    flagged_features = []
    for pid in d['gone']:
        p = catalog['products'][pid]
        for pl in [x for x in p['placements'] if x['kind'] == 'pcard']:
            files[pl['file']], ok = remove_card(files[pl['file']], pid, pl['section'])
            if ok: changed.add(pl['file'])
        feats = [x for x in p['placements'] if x['kind'] == 'feature']
        if feats:
            flagged_features.append((pid, p['title'], [x['file'] for x in feats]))
        p['placements'] = feats
        p['delisted'] = True
    for pid in d['gone']:
        if not catalog['products'][pid]['placements']:
            del catalog['products'][pid]
    # 6. adds
    for pid, title, section, h in d['adds']:
        page = page_of[section]
        img = big_img(h['img'])
        files[page] = insert_card(files[page], section, make_card(pid, title, h['price'], img, eol), title)
        changed.add(page)
        catalog['products'][pid] = {
            'title': title, 'price': h['price'], 'raw_title': h['title'], 'img_uid': uid_of(h['img']),
            'placements': [
                {'file': page, 'kind': 'pcard', 'section': section, 'img': img, 'alt': esc_attr(title)},
                {'file': 'assets/search-index.js', 'kind': 'search', 'title': title, 'price': h['price']}]}
    # 7. seed/refresh raw titles + uids for active products
    for pid, p in catalog['products'].items():
        if pid in hv:
            p['raw_title'] = hv[pid]['title']
            p['img_uid'] = uid_of(hv[pid]['img'])
    # 8. search index
    idx = regen_search_index(catalog)

    # validation on the WOULD-BE state
    errs = validate_site(files, catalog)
    ok = not errs

    # section counts recomputed for catalog.json
    for page in catalog['section_inventory']:
        catalog['section_inventory'][page] = [
            {'name': m.group('name').strip(), 'count': int(m.group('count'))}
            for m in SECTION_RE.finditer(files[page])]

    report = build_report(d, flagged_features, changed, errs)
    (HERE / 'sync-report.md').write_text(report, encoding='utf-8')
    print(report)

    if apply and ok:
        for f in sorted(changed):
            (SITE / f).write_text(files[f], encoding='utf-8')
        (SITE / 'assets' / 'search-index.js').write_text(idx, encoding='utf-8')
        catalog['generated_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
        catalog['products'] = dict(sorted(catalog['products'].items(), key=lambda kv: kv[1]['title'].lower()))
        (HERE / 'catalog.json').write_text(json.dumps(catalog, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'APPLIED: {len(changed)} html files + search-index.js + catalog.json')
    elif apply:
        print('NOT APPLIED: validation failed'); sys.exit(1)
    return ok

def build_report(d, flagged, changed, errs):
    L = [f'# qt-sync report — {datetime.now(timezone.utc).isoformat(timespec="seconds")}', '']
    def sec(title, rows, fmt):
        L.append(f'## {title} ({len(rows)})')
        L.extend(fmt(r) for r in rows) if rows else L.append('- none')
        L.append('')
    sec('Price changes applied', d['price'], lambda r: f'- {r[0]}: ${r[1]} -> ${r[2]}')
    sec('Image changes applied', d['img'], lambda r: f'- {r[0]} -> {r[1]}')
    sec('Re-listed (href swapped)', d['relist'], lambda r: f'- {r[0]} -> {r[1]}')
    sec('Delisted (cards removed)', d['gone'], lambda r: f'- {r}')
    sec('Feature slots needing manual attention', flagged, lambda r: f'- {r[0]} {r[1]!r} in {r[2]}')
    sec('Added (curated)', d['adds'], lambda r: f'- {r[0]} {r[1]!r} -> {r[2]} (${r[3]["price"]})')
    sec('Skipped: duplicate listings of on-site products', d['dups'], lambda r: f'- {r[0]} {r[1][:60]!r} = on-site {r[2]} {r[3]!r}')
    sec('REVIEW QUEUE: new physical items awaiting curation', d['review'], lambda r: f'- {r[0]} ${r[2]} {r[1][:80]!r}')
    sec('Excluded by policy (digital/merch/admin)', d['excluded'], lambda r: f'- {r[0]} {r[1][:60]!r}')
    sec('Raw Etsy title drift (display titles unchanged)', d['title_drift'], lambda r: f'- {r[0]}: {r[1][:50]!r} -> {r[2][:50]!r}')
    L.append(f'## Files changed ({len(changed)})')
    L.extend(f'- {f}' for f in sorted(changed)) if changed else L.append('- none')
    L.append('')
    L.append('## Validation')
    L.extend(f'- ERROR: {e}' for e in errs) if errs else L.append('- all checks passed')
    L.append('')
    return '\n'.join(L)

# ------------------------------------------------------------------ selftest
def selftest():
    html = (SITE / 'catalog.html').read_text(encoding='utf-8')
    # price rewrite
    h2, n = rewrite_price(html, '540986914', '76.00')
    assert n == 1 and '<span class="price">$76.00</span>' in h2 and h2.count('$76.00') == html.count('$76.00') + 1
    # removal + count
    h3, ok = remove_card(html, '540986914', 'Monograms & Name Signs')
    assert ok and 'listing/540986914' not in h3
    assert '(40)' in h3 and '(41)' not in h3
    # add + alphabetical + count
    card = make_card('999999999', 'Aardvark Test Sign', '10.00', 'https://i.etsystatic.com/x/r/il/ab/123/il_800x800.123_t.jpg', '\n')
    h4 = insert_card(html, 'Wall Decor & Signs', card, 'Aardvark Test Sign')
    cards = section_cards(h4, 'Wall Decor & Signs')
    titles = [m.group('title') for m, _, _ in cards]
    assert titles.index('Aardvark Test Sign') == 1 and titles == sorted(titles), titles  # after '"Life is..' (quote sorts first)
    assert '(43)' in h4
    # relist href swap
    h5 = rewrite_href(html, '540986914', '888888888')
    assert 'listing/888888888' in h5 and 'listing/540986914' not in h5
    # feature price rewrite on a category page
    mono = (SITE / 'monograms.html').read_text(encoding='utf-8')
    m2, k = rewrite_price(mono, '596007726', '86.00')
    assert k == 1 and '$86.00' in m2
    # malformed alt repair
    fixed = fix_malformed_alts('<img src="x" alt=""Life is Good" in Patina" loading="lazy">')
    assert fixed == '<img src="x" alt="&quot;Life is Good&quot; in Patina" loading="lazy">'
    print('selftest OK')

if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest()
    else:
        run(apply='--apply' in sys.argv)
