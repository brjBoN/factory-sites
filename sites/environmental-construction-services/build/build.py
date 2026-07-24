"""Emit all ECS Field Notes routes as static pages (nested index.html dirs so
paths match the package's route contract without server config).

Run: python build.py   (from this directory)
"""
import html as H
from pathlib import Path
import data as D

OUT = Path(__file__).resolve().parents[1]
e = lambda s: H.escape(str(s), quote=True)

FONTS = ('https://fonts.googleapis.com/css2?family=League+Gothic&'
         'family=Courier+Prime:ital,wght@0,400;0,700;1,400&'
         'family=Barlow+Condensed:wght@400;500;600&'
         'family=Roboto+Condensed:wght@700&'
         'family=Caveat:wght@500&family=Architects+Daughter&display=swap')

NAV = [('', 'Home'), ('services/', 'Services'), ('about/', 'About'), ('contact/', 'Contact')]


def page(route, title, desc, body, note='FIELD NOTE 01', current=''):
    depth = 0 if route == '' else route.rstrip('/').count('/') + 1
    rel = '../' * depth
    nav = ''.join(
        f'<a href="{rel}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for href, label in NAV)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:image" content="{rel}assets/ecs-field-notes-og.png">
<link rel="icon" href="{rel}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="ledger" aria-hidden="true"><span>{e(note)}</span></div>
<div class="page">
<div class="wrap">
<header class="site">
  <div class="head-in">
    <a class="brand" href="{rel}">
      <img src="{rel}assets/ecs-logo-original.png" alt="">
      <span class="nm">ENVIRONMENTAL<br><span class="l2">CONSTRUCTION SERVICES</span></span>
    </a>
    <span class="locnote" aria-hidden="true"><span class="locline">{e(D.FACTS['location_annotation'])}</span><span class="coords">{e(D.FACTS['location_coords'])}</span></span>
    <button class="nav-toggle" aria-expanded="false" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="primary" aria-label="Primary">
      {nav}
    </nav>
  </div>
</header>
</div>
<main id="main">
{body}
</main>
<footer class="site">
  <div class="foot-in">
    <div>
      <h4>Environmental Construction Services</h4>
      <ul>
        <li>{e(D.FACTS['family'])}</li>
        <li>{e(D.FACTS['address'])}</li>
      </ul>
    </div>
    <div>
      <h4>Reach Us</h4>
      <ul>
        <li><a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a></li>
        <li><a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a></li>
      </ul>
    </div>
    <div>
      <h4>Concept Pages</h4>
      <ul>
        <li><a href="{rel}services/">Services</a></li>
        <li><a href="{rel}about/">About</a></li>
        <li><a href="{rel}contact/">Contact</a></li>
        <li><a href="{rel}accessibility/">Accessibility</a></li>
        <li><a href="{rel}concept-data-use/">Concept &amp; Data Use</a></li>
      </ul>
    </div>
  </div>
  <div class="notices">
{''.join(f'    <p>{e(n)}</p>' for n in D.NOTICES)}
  </div>
</footer>
</div>
<script src="{rel}assets/main.js"></script>
</body>
</html>
"""
    out = OUT / route / 'index.html' if route else OUT / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding='utf-8', newline='\n')
    print('wrote', route or '/')


def sec_head(eyebrow, title):
    return (f'<p class="eyebrow">{e(eyebrow)}</p>'
            f'<h2 class="display">{e(title)}</h2><div class="rule-red"></div>')


# --------------------------------------------------------------------- home
pinned = ''.join(f'''
  <a class="pin-card" href="{p['href']}" aria-label="{e(p['aria'])}">
    <span class="thumb"><img src="assets/{p['asset']}" alt="" aria-hidden="true"></span>
    <span class="lbl">{e(p['label'])}</span>
  </a>''' for p in D.PINNED)

# concept rail: exact labels and order from the approved reference
RAIL_LINKS = [
    ('Drainage', 'services/drainage/'),
    ('Land Clearing', 'services/land-clearing-excavation/'),
    ('Culverts', 'services/site-prep-culverts/'),
    ('Driveways', 'services/driveways/'),
    ('Hardscaping', 'services/landscaping-hardscaping/'),
    ('Seawalls', 'services/seawalls-retention-waterproofing/'),
]
rail = ''.join(f'<a href="{href}">{e(lbl)}</a>' for lbl, href in RAIL_LINKS)

atlas = ''.join(f'''
  <a href="services/{s['slug']}/">
    <span class="art"><img src="assets/{s['asset']}" alt="" aria-hidden="true"></span>
    <span class="cap"><h3>{e(s['label'])}</h3><span class="fn">{e(s['note'])}</span></span>
  </a>''' for s in D.SERVICES)

home = f"""
<div class="wrap">
<section class="hero">
  <div class="hero-copy">
    <h1 class="reveal-mask">{''.join(f'<span class="ln">{e(ln)}</span>' for ln in D.HEADLINE_LINES)}</h1>
    <div class="underline draw" aria-hidden="true"></div>
    <p class="sub settle">{e(D.HERO_COPY)}</p>
    <div class="btn-row settle-2">
      <a class="btn fill" href="services/">Explore Services</a>
      <a class="btn line" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
    </div>
  </div>
  <div class="hero-art desktop settle" aria-hidden="true"><img src="assets/hero-excavation-collage.webp" alt=""></div>
  <div class="hero-art mobile settle" aria-hidden="true"><img src="assets/hero-excavation-collage-mobile.webp" alt=""></div>
</section>
<div class="pinned">
{pinned}
</div>
</div>
<div class="torn" aria-hidden="true"></div>
<div class="rail-band"><div class="rail-links">
{rail}
</div></div>
<div class="wrap">
<section class="sec" id="atlas">
  {sec_head('the whole kit —', 'Six kinds of groundwork.')}
  <div class="atlas">
{atlas}
  </div>
</section>
<section class="sec" style="padding-top:0">
  {sec_head('who we are —', 'Family-owned. Moultrie ground.')}
  <p style="max-width:52ch;margin-top:1rem">{e(D.FACTS['family'])} Based at {e(D.FACTS['address'])}.
  The fastest way to talk through a site is a phone call.</p>
  <div class="btn-row" style="margin-top:1.2rem">
    <a class="btn fill" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
    <a class="btn line" href="{D.FACTS['email_href']}">Email Us</a>
  </div>
</section>
</div>
"""

# ------------------------------------------------------------------ services
services_body = f"""
<section class="sec">
  {sec_head('field note index —', 'Services.')}
  <p style="max-width:56ch;margin-top:1rem">Six categories of ground work. Every illustration is
  concept art — talk to us about what your site actually needs.</p>
  <div class="atlas">
{atlas.replace('href="services/', 'href="')}
  </div>
</section>
"""

# --------------------------------------------------------------- service page
def svc_body(s):
    return f"""
<section class="sec">
  <p class="crumbs"><a href="../">Services</a> / {e(s['label'])}</p>
  {sec_head(s['note'].lower() + ' —', s['label'] + '.')}
  <div class="svc-grid">
    <figure class="svc-art">
      <img src="../../assets/{s['asset']}" alt="Illustrative concept sketch for {e(s['label'].lower())} — not a photograph of completed ECS work">
      <figcaption>Illustrative concept sketch — not completed ECS work.</figcaption>
    </figure>
    <div class="svc-copy">
      <p>{e(s['blurb'])}</p>
      <p>Every property drains, grades, and wears differently. Call or write and tell us
      what the ground is doing — we'll take it from there.</p>
      <div class="btn-row">
        <a class="btn fill" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
        <a class="btn line" href="{D.FACTS['email_href']}">Email Us</a>
      </div>
    </div>
  </div>
</section>
"""

# -------------------------------------------------------------------- about
about_body = f"""
<section class="sec">
  {sec_head('field note —', 'About.')}
  <div class="svc-grid">
    <div class="svc-copy">
      <p><strong>{e(D.FACTS['family'])}</strong></p>
      <p>Environmental Construction Services works the ground: drainage, land clearing and
      excavation, landscaping and hardscaping, seawalls and retention, site preparation,
      culverts, and driveways.</p>
      <p>Based at {e(D.FACTS['address'])}. The best way to find out whether we're the right
      fit for your project is to call.</p>
      <div class="btn-row">
        <a class="btn fill" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
        <a class="btn line" href="{D.FACTS['email_href']}">Email Us</a>
      </div>
    </div>
    <figure class="svc-art">
      <img src="../assets/service-land-clearing-excavation.webp" alt="Illustrative excavation concept sketch — not a photograph of completed ECS work">
      <figcaption>Illustrative concept sketch — not completed ECS work.</figcaption>
    </figure>
  </div>
</section>
"""

# ------------------------------------------------------------------- contact
contact_body = f"""
<section class="sec">
  {sec_head('field note —', 'Contact.')}
  <p style="max-width:56ch;margin:1rem 0 1.6rem">This concept site doesn't take forms or
  collect anything — reach Environmental Construction Services directly:</p>
  <dl class="fact-card">
    <dt>Phone</dt>
    <dd><a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a></dd>
    <dt>Email</dt>
    <dd><a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a></dd>
    <dt>Address</dt>
    <dd>{e(D.FACTS['address'])}</dd>
    <dt>Ownership</dt>
    <dd>{e(D.FACTS['family'])}</dd>
  </dl>
</section>
"""

# -------------------------------------------------------------- accessibility
access_body = """
<section class="sec">
  <p class="eyebrow">the fine print —</p>
  <h2 class="display">Accessibility.</h2><div class="rule-red"></div>
  <div class="svc-copy" style="max-width:60ch;margin-top:1rem">
    <p>This concept is built to be usable by everyone: semantic landmarks and headings, a skip
    link, keyboard-operable navigation and menu, visible focus states, touch targets of at
    least 44 pixels, and text contrast that holds up over the paper textures.</p>
    <p>Animations respect your system's reduced-motion setting — with it enabled, drawing
    effects, parallax, and reveals are replaced with immediate content.</p>
    <p>Decorative illustrations are hidden from assistive technology; meaningful images carry
    descriptions that make clear they are illustrative concept art.</p>
    <p>If something on this concept doesn't work well for you, we want to fix it in the next
    revision.</p>
  </div>
</section>
"""

# ------------------------------------------------------------ concept-data-use
datause_body = f"""
<section class="sec">
  <p class="eyebrow">the fine print —</p>
  <h2 class="display">Concept &amp; Data Use.</h2><div class="rule-red"></div>
  <div class="svc-copy" style="max-width:60ch;margin-top:1rem">
    <p><strong>{e(D.NOTICES[0])}</strong></p>
    <p>This page collects nothing. There are no forms, no analytics, no cookies, no quote
    intake, no payments, no accounts, and no uploads. Fonts are loaded from Google Fonts,
    which receives standard technical request data when the page loads.</p>
    <p>{e(D.NOTICES[1])} The graphite drawings are generated concept art in a field-notes
    style, created to demonstrate a design direction.</p>
    <p>The concept is marked noindex/nofollow and its robots.txt asks crawlers to stay out.</p>
    <p>To reach the real business: <a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a>
    or <a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a>.</p>
  </div>
</section>
"""

NAME = D.FACTS['name']
W = lambda b: f'<div class="wrap">{b}</div>'  # main sits at page level; content re-enters the wrap
page('', f'{NAME} — Moultrie, GA (Concept)', 'Private field-notes website concept: drainage, land clearing, excavation, site preparation, culverts, and driveways in Moultrie, GA.', home, note='FIELD NOTE 01', current='')
page('services', f'Services — {NAME} (Concept)', 'Six categories of groundwork: drainage, clearing and excavation, landscaping, seawalls, site prep and culverts, driveways.', W(services_body), note='FIELD NOTE INDEX', current='services/')
for s in D.SERVICES:
    page(f'services/{s["slug"]}', f'{s["label"]} — {NAME} (Concept)', s['blurb'], W(svc_body(s)), note=s['note'], current='services/')
page('about', f'About — {NAME} (Concept)', 'Family-owned and operated groundwork in Moultrie, GA.', W(about_body), note='FIELD NOTE 08', current='about/')
page('contact', f'Contact — {NAME} (Concept)', 'Phone, email, and address for Environmental Construction Services.', W(contact_body), note='FIELD NOTE 09', current='contact/')
page('accessibility', f'Accessibility — {NAME} (Concept)', 'Accessibility commitments for this private concept.', W(access_body), note='APPENDIX A')
page('concept-data-use', f'Concept & Data Use — {NAME} (Concept)', 'What this private concept is, and what it does not collect.', W(datause_body), note='APPENDIX B')

(OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8', newline='\n')
print('wrote robots.txt')
print('done')
