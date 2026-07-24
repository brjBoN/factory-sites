# Small Business Website Factory — factory-sites

You are working inside Braden's website factory. This repo produces private redesign-concept
websites for local businesses (Moultrie, GA area) that are pitched to owners as an upgrade.
This file is the complete operating manual. Read it fully before touching anything.

## What this repo is

- `sites/<slug>/` — one static site per prospect (plain HTML/CSS/JS, no build step).
- `index.html` (repo root) — PRIVATE directory of all prospect sites. Never send this URL in outreach.
- `outreach/<slug>-handoff.md` — per-prospect brief for the outreach person (contacts, URLs, selling points).
- `tools/qt-sync/` — Quality Tooling Etsy auto-sync (browser harvest + diff/apply engine; see its README).
  Runs as scheduled task `qt-etsy-sync`, Mondays 8am. Reusable pattern for future catalog-backed prospects.
- `push.bat` — legacy one-click deploy from the Cowork cloud era. In Claude Code you just run
  `git add -A && git commit && git push` directly instead.
- Vercel auto-deploys `main` on every push. Two kinds of projects, all in team `bo-n`
  (team_tRrJbLnPlRP8HY0lkcprm2rU):
  - `factory-sites` → root of repo → factory-sites-bo-n.vercel.app (internal directory, all sites as subpaths)
  - One dedicated project per outreach-ready prospect, rootDirectory = `sites/<slug>`:
    - `quality-tooling` → https://quality-tooling.vercel.app
  - Creating a new dedicated project: vercel.com/new → import factory-sites → set Project Name to
    the slug → Root Directory = sites/<slug> → preset "Other", no build command → Deploy. (~30s, once per prospect.)
  - OUTREACH RULE: only ever send the dedicated per-prospect domain. Prospects must never see other prospects' work.

## Prospect status

| Prospect | Folder | Live | Status |
|---|---|---|---|
| Scrap Now Metal Recycling | sites/scrap-now-metal | factory-sites-bo-n.vercel.app/sites/scrap-now-metal/ | done; needs dedicated Vercel project before outreach |
| Quality Tooling, LLC | sites/quality-tooling | quality-tooling.vercel.app | done, approved; Etsy auto-sync live; handoff: outreach/quality-tooling-handoff.md |
| Three Crazy Bakers | sites/three-crazy-bakers | factory-sites-bo-n.vercel.app/sites/three-crazy-bakers/ | done, approved; handoff: outreach/three-crazy-bakers-handoff.md (+.pdf); NEEDS dedicated Vercel project before outreach |

## The workflow (per prospect)

1. **Research**: crawl the business's current site (sitemap.xml → full page inventory), directories,
   Etsy/social. Record name, phone, email, address, hours, services, products+prices, socials, trust
   stats (review counts, years in business). Verify facts; never publish invented claims, prices, or hours.
   **Absence claims need real-browser verification**: fetch-based crawls miss JS-injected content
   (entry popups, chat/order widgets) — TCB's on-load DoorDash popup was invisible to page fetches
   and "their site has no path to online ordering" nearly shipped in an outreach doc. Before
   asserting a competitor site LACKS something, load it in a real browser and watch what appears.
2. **Concept**: generate 2–3 landing-page concept images in-house (`tools/concept_gen.py`,
   gpt-image-1; OPENAI_API_KEY is a machine env var — never in repo/chat) from a
   research-grounded brief, save under `concepts/<slug>/`, present to Braden. He approves ONE.
   This gate is mandatory. Image concepts are the standard: they set a visual bar the coded
   build must match with minimal revisions — see "Concept fidelity protocol" below.
3. **Build**: implement the approved concept EXACTLY (see Hard Rules), all pages, then QA.
4. **Deploy**: git push → verify the Vercel deployment state and the live URL in a real browser.
5. **Handoff**: write `outreach/<slug>-handoff.md` for whoever runs outreach. Required contents:
   the target's logo at the top (relative image ref into `sites/<slug>/assets/` — the
   background-removed original), contact info (phone, email, address, person names + roles —
   mine the Etsy/Facebook "about" pages for who actually runs what), original site URL, our
   concept URL (dedicated per-prospect domain ONLY), ranked selling points/upgrades (lead with
   anything automated — e.g. the Etsy auto-sync), a 60-second demo flow, likely objections with
   honest answers, cautions (noindex is intentional; never send the factory directory URL;
   don't promise pages the original lacked), and a **domain-connection walkthrough tailored to
   where their domain actually lives** (for Wix domains: Wix account → Domains → Advanced →
   Edit DNS; A `@` → Vercel's displayed IP, CNAME `www` → cname.vercel-dns.com; registration
   never moves for launch). No trust-stats section — fold any needed rapport facts into the
   contacts/one-liner. Reference example: `outreach/quality-tooling-handoff.md`.
   **The human deliverable is a PDF**: `python tools/handoff_pdf.py <slug>` renders the .md to
   `outreach/<slug>-handoff.pdf` styled with the prospect's design tokens (add the slug to
   TOKENS in the script). The .md stays the source of truth — regenerate the PDF after every
   edit, and visually QA it by rendering pages to PNG (pypdfium2) before committing.
   Deps: `pip install reportlab pillow pypdfium2`. The PDF footer marks it internal-only.
6. Braden (or the outreach person) handles outreach.

## HARD RULES (each one exists because a violation caused a rework round)

1. **Unique design per client.** Never reuse a previous prospect's style, palette, or layout DNA.
2. **Feature parity is a floor.** Every page and feature of the original site must exist in ours —
   including search bars, gift cards, category pages, social links. Empty original pages become
   properly designed inquiry pages. NO new pages the original didn't have (a Custom Orders page
   got cut for this).
3. **Implement the approved concept EXACTLY.** Full-bleed sections stay full-bleed at 1920+.
   Typography must match the concept's class (Quality Tooling's was Times-class → Tinos, NOT
   Playfair). Icons: crop them from the concept image itself (background-removed) rather than
   redrawing approximations. Match proportions (panel aspect ratios), arrow styles (long thin
   strokes), letterspacing, caps treatment.
4. **No "private concept" banner bars.** Invisible robots noindex + one muted footer line only.
5. **Original assets at full resolution.** Product photos come from the source CDN originals
   (e.g. static.wixstatic.com media IDs, i.etsystatic.com thumbs — hotlink Etsy with
   referrerpolicy="no-referrer"), NEVER from screenshot crops. Logos: pull the original file and
   background-remove with color unmixing (alpha = max((bg−rgb)/bg); ink = (rgb−(1−a)·bg)/a).
   In Code you have open network: just curl/download the originals directly.
6. **Products link directly to their own Etsy/store listings** with the listing's current price.
   Harvest the whole catalog (id, price, title, thumb) and build a full illustrated catalog section.
7. **QA at 1920×1080 minimum**, with real webfonts, before showing Braden anything. Never show
   fallback-font renders or stale screenshots. Verify the LIVE deployed site in a real browser as
   the final step. Sub-checks that have bitten before: nav scale/position, image sharpness at
   full-bleed widths, strip rows fitting on one line, favicon = business's actual logo mark,
   Home as first nav item, no un-centered images.
8. **Inpainting photo zones**: for removing baked-in text/buttons from concept images, TELEA works
   on smooth zones; on textured zones (wood, brushed steel) use cv2.seamlessClone with tiled clean
   strips — blur-fill smudges are unacceptable.
9. **Mobile QA is mandatory on EVERY page before delivery** (390×844 and ~768 wide). Programmatic
   check, not eyeball: `document.documentElement.scrollWidth` must equal the viewport width on every
   page — any horizontal scroll is a defect. Known trap that caused one: CSS grid items default to
   min-width:auto, so wide child content (buttons with tracked caps, fixed max-width labels) silently
   widens hero panels past the viewport — set `min-width:0` + `overflow:hidden` on grid panels and
   scale button/label type down in the mobile media query. The overlay hamburger menu must be:
   centered (flex column + align-items:center + text-align:center), scroll-locked (body.nav-open
   {overflow:hidden;position:fixed;width:100%} toggled in JS), and close on link tap. Test the open
   menu and the search box at mobile width with screenshots before showing Braden anything.

## Concept fidelity protocol (mastering image → code with minimal revisions)

The generated image sets the bar; Braden's review must find nothing left to fix. Every QT
revision cause is now a pre-delivery check you run yourself — he is the final gate, not the
first QA pass.

1. **Brief → prompt**: ground it in research facts; give palette as literal hex, typography as
   a CLASS ("Times-class serif display caps" — never a font name for the model to mangle), and
   layout structurally (split hero panels, tracked-caps utility bar, 4-card product strip).
   Prefer buildable compositions — don't prompt for effects you can't reproduce in CSS.
2. **Extract ground truth from the approved image BEFORE coding**: sample palette hexes from
   the pixels (the model drifts from the brief — the pixels win); classify the typeface against
   Google Fonts specimens (Tinos-not-Playfair cost a rework round); measure panel aspect
   ratios, gutters, letterspacing, and arrow proportions from the image; crop + background-
   remove icons/motifs straight from the concept (never redraw — hard rule 3); inpaint
   baked-in text zones per hard rule 8 before reusing photo/texture regions.
3. **Parity pass before Braden sees anything**: full-page screenshot at 1920 laid side-by-side
   with the concept image, then walk the fixed checklist — typography class, full-bleed at
   1920+, palette hex match, icon fidelity, panel ratios, arrow style, letterspacing/caps,
   Home-first nav, favicon = logo mark, centering, strip rows on one line. Fix everything
   visible, then present.
4. **Region-parity verification (the TCB landing-page lesson — geometry is not enough)**:
   crop element-aligned windows of concept vs build for EVERY distinct region and judge
   RENDERED APPEARANCE, adversarially, until nothing major remains. The failure classes that
   got through geometric checks: (a) asset integration — an "RGBA" PNG with baked-in paper
   background reads as a messy cutout; check real transparency with PIL, fix by edge-trim +
   alpha-unmix (hard rule 5) + mix-blend-mode multiply, and prefer cropping art straight from
   the concept canvas at native proportions; (b) component chrome — a broader selector
   (nav.primary a) silently out-specified the button class and collapsed it; verify computed
   boxes against concept-measured boxes (measure the concept with PIL color-scans);
   (c) texture — if a blank patch's luminance stddev is ~0 the paper grain isn't rendering
   (section backgrounds cover the body tile; use a fixed multiply overlay); (d) ornaments —
   crop them from the concept, never approximate with CSS shapes. Tools: Playwright headless
   Chromium is installed for screenshots (position:fixed overlays cause false seams in
   full-page stitched captures — confirm with viewport shots); concept color samples include
   generative grain, so the package's design tokens stay canonical for flat colors while a
   real grain overlay recreates the sampled look. FOLD-FIT (Braden requirement, TCB round):
   the landing composition must end its bottom band cleanly at the first-viewport bottom —
   flex the hero via 100vh-derived custom property, let the band stretch, give it a border
   terminus, and make decorative overlays (ornament strips) track the hero height so they
   never bleed at shorter folds. Verify the fold at 1920×1080, ~2000×1132 (4K logical), and
   2560×1440 — not just at the concept's 1536×1024 canvas size.
5. **Revision-loop discipline** (every one of these caused a Braden-visible defect on TCB):
   - **A fix can become next round's bug.** The worst TCB defect (two overlapping courthouse
     drawings) was created by an earlier fix: an audit said "courthouse missing from hero
     corner" and a NEW asset was added, when the finding actually described the streetscape's
     own tower. Before adding an asset to satisfy a "missing art" finding, zoom the concept
     region and check whether an existing/recroppable asset already contains it. After every
     fix round, assert no duplicated motifs programmatically.
   - **One source of truth per drawing.** When a package crop is inadequate (truncated tower
     tips, baked backgrounds), re-crop from the concept canvas at native proportions and
     RETIRE the old asset everywhere — never leave two crops of the same subject in play.
   - **px sizes frozen at concept scale read wrong at 1920+/4K.** Chrome type (nav, buttons)
     needs vw-clamps (nav went 15px fixed → clamp(15px, 1.05vw, 21px) after Braden called it
     too small on 4K). Concept-exact at 1536 is the floor, not the ceiling.
   - **Grounded art anchors to its section's bottom edge** (object-position: * bottom) so
     illustrations meet the fold at ANY viewport height — verified by asserting
     art.bottom == band.bottom, not by looking at one screenshot.
   - **QA is measured assertions, not eyeballs**: the standing Playwright harness asserts
     foldDelta ≤ 2px, seam gaps == 0, copy scrollHeight ≤ clientHeight, no duplicate motifs,
     scrollWidth ≤ viewport, at 1920×1080 / 2000×1132 / 2560×1440 / one tall viewport +
     390 / 768. Run it after EVERY styling change, not just before delivery.
   - **Braden's live review outranks the concept.** Apply his deviations (gap removal, section
     renames) as isolated, clearly-labeled commits so any one is revertible with a single
     `git revert <sha>`, and note the original values in a CSS comment.

## Quality Tooling reference implementation

`sites/quality-tooling/` is the gold standard — study it before building the next site.
Design tokens: cream #F1EDE4 / navy #1E3A5C / orange #E05A2B; Tinos (serif caps display) +
Inter (tracked caps labels). Pages are generated by a Python builder (pattern worth reusing:
single build script emits all pages from shared header/footer + a catalog data module with
harvested listings). Client-side search indexes all products + pages (assets/search-index.js).

## Business facts on file

- **Quality Tooling, LLC**: 315 Wesley Chapel Rd, Moultrie, GA 31788 · 1-229-324-2124 ·
  quality_tooling@windstream.net · since 1985 · etsy.com/shop/QualityToolingLLC (4.8★, 1.3k reviews,
  7.3k sales, on Etsy since 2013) · FB @QualityToolingLLC · IG @quality_tooling_llc ·
  original site: qualitytoolingllc.com (Wix) · people: John (Owner) + Janice (Co-Owner), founders;
  Jennifer — runs metal art dept + the Etsy shop (primary outreach contact); Timothy — CNC/laser.
- **Scrap Now Metal Recycling**: Moultrie GA 31788 · (229) 985-1041 · info@scrapnowmetal.com ·
  scrapnowmetal.com. CAUTION: street address (550 Industrial Rd vs 305 Industrial Pkwy) and hours
  conflict across sources; site shows first-party info with "call to confirm" notes.
- **Three Crazy Bakers**: 102 S Main St, Moultrie, GA 31768 · (229) 985-8809 (no public email) ·
  Mon–Sat 10–9, Sun 11–8 · est. 1998 by Larry & Donna Grimm + daughter Paige; owners now
  Maggie & Hart Brown · threecrazybakers.com (WordPress ~2013; menus are JPEG scans) ·
  IG @threecrazybakers · X @3crazybaker (FB page looks unclaimed — verify) · DoorDash ordering:
  order.online/business/Three%20Crazy%20Bakers-308079 · DNS on ns-cloud-e*.googledomains.com
  (ex-Google Domains → likely Squarespace Domains post-2023) · LIVE MX → their web host:
  domain email probably exists; never touch MX at cutover, and warn them cancelling WP hosting
  could kill email. Menu data transcribed in sites/three-crazy-bakers/build/data.py.

## Client launch checklist (domain cutover — SEO-safe)

When a prospect becomes a client and their real domain points at our site, execute ALL of this.
The domain is NOT "transferred" — the client keeps their registrar; we add the domain to the
prospect's dedicated Vercel project and they update DNS (A/CNAME per Vercel's instructions).
Wix-registered domains: edit records in Wix under Domains → <domain> → Advanced → Edit DNS
(A `@` → Vercel's displayed IP, CNAME `www` → cname.vercel-dns.com); Wix warns about pointing
away from the Wix site — expected. Client keeps paying only Wix's small domain-registration fee
and can cancel the Wix *site plan* once cutover verifies. Moving the registration off Wix is
optional later housekeeping (auth code via Transfer-away flow; blocked within 60 days of
registration/renewal), never a launch requirement. Domain email would ride on untouched MX
records, but check first whether they even use domain email (QT doesn't — windstream.net).
Domain-level SEO equity (backlinks, Google Business Profile, age) survives automatically.
The risks are URL-level and crawl-directive-level:

1. **REMOVE the demo blocks — the #1 landmine.** Every page ships with
   `<meta name="robots" content="noindex, nofollow">` and robots.txt is Disallow-all (intentional
   for private concepts). Launching like that doesn't damage SEO, it deletes it. Flip to indexable,
   write a real robots.txt, drop the "Website concept" footer line.
2. **301-map every old URL.** Enable `cleanUrls: true` in vercel.json so /about serves about.html —
   because of Hard Rule 2 (feature parity), our filenames already mirror the old site's paths
   almost 1:1. Redirect the leftovers (e.g. Wix's /home → /, /etsy-shop → Etsy). Crawl the old
   site's sitemap.xml for the definitive URL list; nothing may 404.
3. **Add sitemap.xml + canonical tags**, submit the domain in Google Search Console, and request
   recrawl. Add JSON-LD LocalBusiness schema (verified NAP only).
4. **Update the Google Business Profile** website link if it pointed at a now-redirected URL.
5. Keep the old site live until DNS + redirects are verified, then expect a brief (days-to-weeks)
   ranking wobble while Google recrawls — normal. Net effect should be positive: static-fast Core
   Web Vitals, semantic HTML, and richer content than the Wix/Sites originals, with the client's
   existing keyword language preserved in the copy.
6. Optional hardening at launch: self-host the Etsy-hotlinked catalog images.

## Ecosystem

- GitHub: brjBoN/factory-sites (public repo — flip private in settings if desired; Vercel keeps working).
- Vercel + Supabase are connected as Claude connectors (OAuth) — also available in Claude Code via MCP.
- Supabase: intended as the prospect-pipeline database (prospects, status, URLs, outreach dates) — not yet built.
- A parallel ChatGPT-built factory lives in Documents\Factories\local-business-website-factory-scrap-now-starter
  (reference only; its evidence.json research pattern for Scrap Now is good prior art).
- Cowork (cloud) sessions share a claude.ai Project "Small Business Website Factory" with build logs.
  Claude Code can't read that project — this file is the source of truth for Code sessions.
