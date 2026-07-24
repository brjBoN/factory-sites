# Small Business Website Factory — factory-sites

You are working inside Braden's website factory. This repo produces private redesign-concept
websites for local businesses (Moultrie, GA area) that are pitched to owners as an upgrade.
This file is the complete operating manual. Read it fully before touching anything.

## What this repo is

- `sites/<slug>/` — one static site per prospect (plain HTML/CSS/JS, no build step).
- `index.html` (repo root) — PRIVATE directory of all prospect sites. Never send this URL in outreach.
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
| Quality Tooling, LLC | sites/quality-tooling | quality-tooling.vercel.app | done, approved by Braden |

## The workflow (per prospect)

1. **Research**: crawl the business's current site (sitemap.xml → full page inventory), directories,
   Etsy/social. Record name, phone, email, address, hours, services, products+prices, socials, trust
   stats (review counts, years in business). Verify facts; never publish invented claims, prices, or hours.
2. **Concept**: Braden generates 2–3 landing-page concept images in ChatGPT (he is the image-gen
   courier) OR you design coded concepts. He approves ONE. This gate is mandatory.
3. **Build**: implement the approved concept EXACTLY (see Hard Rules), all pages, then QA.
4. **Deploy**: git push → verify the Vercel deployment state and the live URL in a real browser.
5. Braden handles outreach.

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

## Quality Tooling reference implementation

`sites/quality-tooling/` is the gold standard — study it before building the next site.
Design tokens: cream #F1EDE4 / navy #1E3A5C / orange #E05A2B; Tinos (serif caps display) +
Inter (tracked caps labels). Pages are generated by a Python builder (pattern worth reusing:
single build script emits all pages from shared header/footer + a catalog data module with
harvested listings). Client-side search indexes all products + pages (assets/search-index.js).

## Business facts on file

- **Quality Tooling, LLC**: 315 Wesley Chapel Rd, Moultrie, GA 31788 · 1-229-324-2124 ·
  quality_tooling@windstream.net · since 1985 · etsy.com/shop/QualityToolingLLC (4.8★, 1.3k reviews,
  7.3k sales, 12 yrs) · FB @QualityToolingLLC · IG @quality_tooling_llc.
- **Scrap Now Metal Recycling**: Moultrie GA 31788 · (229) 985-1041 · info@scrapnowmetal.com ·
  scrapnowmetal.com. CAUTION: street address (550 Industrial Rd vs 305 Industrial Pkwy) and hours
  conflict across sources; site shows first-party info with "call to confirm" notes.

## Client launch checklist (domain cutover — SEO-safe)

When a prospect becomes a client and their real domain points at our site, execute ALL of this.
The domain is NOT "transferred" — the client keeps their registrar; we add the domain to the
prospect's dedicated Vercel project and they update DNS (A/CNAME per Vercel's instructions).
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
- Higgsfield (AI image/video gen — use it to GENERATE CONCEPT IMAGES natively, replacing the
  ChatGPT-courier step in workflow step 2): connected on claude.ai as a custom connector
  (URL https://mcp.higgsfield.ai/mcp, OAuth). To wire it in Claude Code, the transport flag is the
  usual failure point — run exactly:
  `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`
  then run `/mcp` inside the session and complete the browser OAuth. Generations spend Braden's
  Higgsfield plan credits; always present 2–3 concept options for his approval before building.
- Supabase: intended as the prospect-pipeline database (prospects, status, URLs, outreach dates) — not yet built.
- A parallel ChatGPT-built factory lives in Documents\Factories\local-business-website-factory-scrap-now-starter
  (reference only; its evidence.json research pattern for Scrap Now is good prior art).
- Cowork (cloud) sessions share a claude.ai Project "Small Business Website Factory" with build logs.
  Claude Code can't read that project — this file is the source of truth for Code sessions.
