# qt-sync — Etsy catalog auto-sync for sites/quality-tooling

Keeps the Quality Tooling site's product data (prices, links, images, catalog
membership, search index) in step with the live Etsy shop, per the CLAUDE.md
catalog pattern. Surgical patcher, not a page generator: the approved design is
never regenerated, only product data inside it changes.

## Why the harvest needs a browser

Etsy is behind DataDome. `curl`/`urllib` get HTTP 403 even from a residential
IP (TLS fingerprint). The in-app Claude browser passes. So the pipeline is:

    browser (fetch shop pages, parse cards)  ->  POST to localhost sink  ->  harvest.json
    python sync.py                            ->  diff + patch + validate ->  site files

## Files

| file | role |
|---|---|
| `harvest.json` | live shop snapshot (id, raw title, price, thumb) — written by the harvest step |
| `catalog.json` | canonical site catalog: curated titles, prices, every placement — maintained by sync.py |
| `curation.json` | human-approved additions `{id: {title, section}}`; only ids here are ever auto-added |
| `sync.py` | diff + apply + validate + report (`--apply`, `--selftest`) |
| `extract_catalog.py` | one-time/regression: rebuild catalog.json from site HTML |
| `sink.py` | localhost receiver for the browser's harvest POST |
| `sync-report.md` | output of the last run |

## Running a sync (Claude Code session)

1. `python tools/qt-sync/sink.py tools/qt-sync/harvest.json 8377` (background)
2. Browser: navigate to `https://www.etsy.com/shop/QualityToolingLLC`
3. Browser JS: run the harvest snippet below (fetches pages 1..N with
   `sort_order=title_asc` until an empty/stale page — do NOT trust the visible
   paginator, it under-reports; page 6 existed when the bar showed 5), then
   POSTs the payload to `http://127.0.0.1:8377/harvest`.
4. `python tools/qt-sync/sync.py` — review plan/report (dry run).
5. `python tools/qt-sync/sync.py --apply`, QA (below), commit, push, verify
   the Vercel deployment is READY and spot-check the live URL.

Harvest snippet (paste into the browser JS tool on the shop page):

```js
(async () => {
  const parse = (html) => { const doc = new DOMParser().parseFromString(html, 'text/html');
    return [...doc.querySelectorAll('a.listing-link[data-listing-id]')].map(a => { const img = a.querySelector('img');
      const vals = [...a.querySelectorAll('.currency-value')].map(e => e.textContent.trim());
      return {id: a.dataset.listingId, title: (a.querySelector('h3,[class*="title"]')?.textContent || '').replace(/\s+/g, ' ').trim(),
        price: vals[0] || null, origPrice: vals[1] || null,
        img: img ? (img.getAttribute('src') || (img.getAttribute('srcset') || '').split(' ')[0]) : null}; }); };
  const byId = new Map();
  for (let p = 1; p <= 20; p++) {
    const r = await fetch(`https://www.etsy.com/shop/QualityToolingLLC?sort_order=title_asc&page=${p}`, {credentials: 'include'});
    if (!r.ok) break;
    const items = parse(await r.text()); let fresh = 0;
    for (const it of items) if (!byId.has(it.id)) { byId.set(it.id, it); fresh++; }
    if (!items.length || !fresh) break;
    await new Promise(res => setTimeout(res, 1200));
  }
  const payload = JSON.stringify({fetched_from: 'https://www.etsy.com/shop/QualityToolingLLC',
    harvested_at: new Date().toISOString(), count: byId.size, items: [...byId.values()]}, null, 1);
  await fetch('http://127.0.0.1:8377/harvest', {method: 'POST', mode: 'no-cors', body: payload});
  return 'harvested ' + byId.size;
})()
```

## What syncs automatically vs. what waits for a human

Automatic: price changes, primary-image changes, re-lists (old id gone, new id
shares the image uid -> href swap), delisted catalog cards (removed + section
count fixed), curated additions.

Report-only (never automatic): new physical items not in curation.json (review
queue), duplicate listings of on-site products (same photo, both active),
delisted products that occupy feature slots on category pages/homepage, raw
Etsy title drift (display titles are curated, never overwritten).

Excluded by policy, silently: digital files (PNG/SVG/sublimation/Cricut),
print-on-demand merch (shirts/sweatshirts/pint glass), RUSH ORDER, WHOLESALE.

## QA gates before pushing (hard rules 7 & 9)

* `sync.py` validators must pass (section counts, alphabetical order, price
  format, attribute escaping, no duplicate cards).
* Serve locally, then in the browser: fonts actually loaded (`document.fonts`),
  new card images load (probe with `new Image()` + `referrerPolicy='no-referrer'`
  — in-page lazy images never fire in a hidden pane), 4-up grid intact at 1920.
* Mobile: `documentElement.scrollWidth <= viewport` on EVERY page at 390 and
  768 (iframe sweep works in one JS call).
* After push: Vercel deployment READY + live-URL spot check.

## Notes

* Display titles on the site are curated (short, Title Case) — the sync must
  never replace them with raw Etsy SEO titles.
* New-card thumbs: upgrade CDN variant to `il_800x800` for sharpness.
* The shop runs parallel duplicate listings of some products (same photo,
  near-same title, both active). One card per product on the site; dups are
  detected by image uid and reported, not added.
