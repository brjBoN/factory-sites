# Outreach Handoff — Three Crazy Bakers

![Three Crazy Bakers logo](../sites/three-crazy-bakers/assets/three-crazy-bakers-logo-white.png)

Prepared 2026-07-24 · Concept approved · Site live, fold-verified at 1080p/1440p/4K

## The one-liner

The #1-ranked restaurant in Moultrie (of 46 on TripAdvisor) — a 27-year institution on the
Square — has a fixed-width website from around 2013 whose menus are photo scans Google can't
read, and whose only path to online ordering is a dismissible popup. We built the full redesign
from their own identity
(their storefront sign literally reads "On the Square · Established 1998"), with every menu as
live text and their DoorDash ordering wired into every page.

## Who to talk to

| Person | Role | Why they matter |
|---|---|---|
| **Maggie & Hart Brown** | Owners | **Start here.** They took over the legacy from the founding family — newer owners of an old name are exactly who invests in modernizing it. |
| Larry & Donna Grimm + daughter Paige | Founders (1998) | The origin story. "Three crazy people who wanted a bakery." Honor them in the room; the site's story section already does. |

## Contact details

- **Phone:** (229) 985-8809 — their primary channel; no public email is listed anywhere
- **Address:** 102 S Main St, Moultrie, GA 31768 (corner of S Main & 1st Ave, on the Square)
- **Hours:** Mon–Sat 10am–9pm · Sun 11am–8pm, seven days a week
- **Original website:** https://threecrazybakers.com (WordPress, ~2013 era)
- **Our concept site:** https://three-crazy-bakers.vercel.app ← the ONLY link you ever send
  (Braden must create this dedicated Vercel project before outreach — see cautions)
- **Socials:** Instagram @threecrazybakers · X @3crazybaker (a Facebook page exists but looks
  unclaimed/legacy — verify with the owners before referencing it)

> ⚠️ **Never send any factory-sites-bo-n.vercel.app URL.** That's the internal directory with
> other prospects' work on it. The prospect sees three-crazy-bakers.vercel.app and nothing else.

## What we built — selling points, strongest first

1. **Menus Google can actually read.** Their current menus are JPEG scans inside a webpage —
   invisible to search engines, unreadable for accessibility, painful on phones. We transcribed
   every one: 18 roll-ups, burgers & sandwiches, salads, quiche, soups, full dinner menu,
   breakfast, all ten take-and-bake casseroles, catering — every item with its description and
   posted price, as live text.
2. **Works on phones.** The current site is fixed-width desktop-only; most restaurant traffic
   is mobile. The redesign is verified overflow-free at phone/tablet width on every page.
3. **Built from their own identity, not a template.** The wordmark matches their storefront
   sign, the headline is their window banner ("On the Square · Established 1998"), and the
   pencil heritage illustrations echo the courthouse drawing printed on their actual menus.
   Show them the storefront photo on the site and let them make the connection.
4. **Ordering that's always in reach.** Today their DoorDash lives in a popup that appears
   when you land — close it (or let a popup blocker eat it) and the path to order is gone.
   Ours keeps a persistent ORDER NOW button in the header of every page, wired to the same
   DoorDash storefront: no interruption, never more than one click away.
5. **Take & Bake gets the spotlight.** Their most distinctive offering — ten casseroles,
   order by 2pm, pick up by 3pm — was buried on a text page; it's now a signature section with
   its own page, linked from the landing rail.
6. **The story told right.** Est. 1998 by the Grimms, carried forward by the Browns, with the
   real storefront photo — small-town credibility their current site never conveys.
7. **Nothing lost, launch is safe.** All 9 pages of the original exist here under matching
   paths (menu, breakfast, dinner-specials, dinner-casseroles, catering, pics, directions,
   privacy), so the SEO cutover is a clean 1:1 redirect map.

## Suggested demo flow (60 seconds)

1. Open **three-crazy-bakers.vercel.app** — the whole first screen is the pitch: their sign
   as a website.
2. Scroll: story section with their real storefront photo → "that's your sign."
3. Open **MENU** — scroll the live text menu. "Google can read this now. Your scans, it can't."
4. Click **ORDER NOW** — their real DoorDash storefront opens. "Same ordering you have today —
   but it lives in the corner of every page instead of a popup people close."
5. Pull it up on your phone next to their current site on your phone. That contrast closes.

## Honest answers to likely questions

- **"We already have a website."** → Same pages, same information — but your menus become
  searchable text instead of photos, ordering is one click from anywhere, and it works on
  phones. It's your site, brought up to what customers expect now.
- **"How much work is this for us?"** → None to start: we transcribed everything from your
  posted menus. Menu changes after launch are text edits — send a photo of the new menu and
  it's updated same-day.
- **"We're already busy — why bother?"** → This isn't about the regulars; it's about the
  Highway 319 traveler googling "restaurants in Moultrie" who lands on a JPEG menu and leaves.
  You're the #1-rated restaurant in town; your website should say so.
- **"Will we lose our Google ranking?"** → No — you keep the domain; every old URL redirects
  1:1 to its new page, and we hand Google the new sitemap. The plan is written down before
  anything changes.

## Cautions

- **Create the dedicated Vercel project first** (vercel.com/new → import factory-sites →
  name `three-crazy-bakers` → Root Directory `sites/three-crazy-bakers` → no build command →
  Deploy, ~30 seconds). Do not do outreach until three-crazy-bakers.vercel.app resolves.
- The concept site is intentionally **hidden from Google** (noindex) while it's a private
  pitch — a feature, not a bug.
- **Prices are from their posted menus** (dinner menu 2022, lunch menu 2023, casseroles page)
  with a "call to confirm" line on every menu page. Have the owners confirm current prices at
  launch; don't quote prices as current in the meeting.
- The **hero food photo is an illustrative composite** grounded in their own photography —
  never present it as a photo of a current dish. Every other photo on the site is genuinely theirs.
- **Their current site DOES offer DoorDash ordering** — via a popup on page load. Never
  claim they have no online ordering; the pitch is presentation (persistent button on every
  page vs. a dismissible popup), not absence.
- Verify the **DoorDash storefront link still works** the morning of any demo.
- Don't promise pages their current site doesn't have (we mirror their structure on purpose).
- Don't reference any other business's concept site.

## If they say yes — connecting their domain

The say-in-the-room line: **"You keep your domain and your email. It's two DNS records, we do
it together on a screen-share, and your old site stays up until the new one is verified live."**

Where their domain actually lives: DNS is served by Google Cloud nameservers
(ns-cloud-e*.googledomains.com) — the old **Google Domains** setup, which Google handed to
**Squarespace Domains** in 2023. So they most likely log in at Squarespace Domains (or with
their Google account if it never migrated). **First step on the screen-share: ask where they
manage the domain and confirm.**

1. We prep launch on our side first (remove noindex, sitemap, 1:1 redirects per the CLAUDE.md
   launch checklist).
2. We add `threecrazybakers.com` + `www` to the Vercel project; Vercel displays the exact two
   records.
3. In their DNS manager: **A record** for `@` → the IP Vercel shows; **CNAME** for `www` →
   `cname.vercel-dns.com`. Change nothing else.
4. **Touch nothing about MX.** Their domain has live MX records pointing at their current web
   host — that means email on the domain probably exists even though none is published. Ask
   the owners whether they use @threecrazybakers.com email. If yes: their email rides on the
   current hosting, so they must **keep the hosting plan** (or migrate email) even after the
   website moves — cancelling WordPress hosting would kill their email, not just the old site.
5. Propagation minutes-to-hours; SSL automatic; old site keeps serving until verified. Expect
   a brief, normal ranking wobble; the redirect map carries the equity.
