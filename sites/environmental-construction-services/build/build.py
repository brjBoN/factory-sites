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


def page(route, title, desc, body, note='FIELD NOTE 01', current='', kind='interior'):
    depth = 0 if route == '' else route.rstrip('/').count('/') + 1
    rel = '../' * depth
    nav = ''.join(
        f'<a href="{rel}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for href, label in NAV)
    # painted brad+FIELD NOTE 01 on home; brad alone on interior pages
    ledger_art = (f'<img class="lednote" src="{rel}assets/fieldnote-01.png" alt="">'
                  if kind == 'home' else
                  f'<img class="ledbrad" src="{rel}assets/brad-brass.png" alt="">')
    # desktop header for interior pages: painted concept strip + live logo/nav
    board_header = '' if kind == 'home' else f"""
<div class="stage-pos d-only">
 <div class="stage">
  <header class="board-header" style="background-image:url('{rel}assets/header-strip.png')">
    <a class="logo-live" href="{rel}" aria-label="Environmental Construction Services — home"><img src="{rel}assets/ecs-logo-plated.png" alt=""></a>
    <nav class="primary stage-nav" aria-label="Primary">{nav}</nav>
  </header>
 </div>
</div>"""
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
<body data-page="{kind}">
<script>
(function(){{var f=function(){{var z=1;
if(window.matchMedia('(min-width: 901px)').matches){{z=window.innerWidth/1536;
if(document.body.dataset.page==='home')z=Math.min(z,window.innerHeight/1024);}}
document.documentElement.style.setProperty('--zoom',z);}};
window.addEventListener('resize',f);f();}})();
</script>
<a class="skip-link" href="#main">Skip to content</a>
<div class="ledger" aria-hidden="true">{ledger_art}<span>{e(note)}</span></div>
<div class="page">
<div class="wrap m-only">
<header class="site">
  <div class="head-in">
    <a class="brand" href="{rel}">
      <img src="{rel}assets/ecs-logo-plated.png" alt="">
      <span class="nm">ENVIRONMENTAL<br><span class="l2">CONSTRUCTION SERVICES</span></span>
    </a>
    <span class="locnote" aria-hidden="true"><span class="locline">{e(D.FACTS['location_annotation'])}</span><span class="coords">{e(D.FACTS['location_coords'])}</span></span>
    <button class="nav-toggle" aria-expanded="false" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="primary" aria-label="Primary">
      {nav}
    </nav>
  </div>
</header>
</div>{board_header}
<main id="main">
{body}
</main>
<footer class="site">
<div class="stage-pos"><div class="stage">
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
</div></div>
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

# live overlays sit at concept-canvas coordinates (minus the 88px ledger strip)
# the painted cards stay untouched in the canvas; each gets an invisible hitbox
# whose background clones the same canvas region (pixel-aligned by construction)
# and only shows on hover, so parity at rest is exact
CARDS_LIVE = [
    ('services/drainage/', 'Explore drainage services', 62, 745, 404, 141),
    ('services/land-clearing-excavation/',
     'Explore land clearing, excavation, and site preparation services', 475, 742, 415, 144),
    ('services/site-prep-culverts/',
     'Explore culvert and driveway services', 897, 755, 405, 131),
]
cards_live = ''.join(f'''
    <a class="card-hit" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background-position:-{x}px -{y}px" href="{href}" aria-label="{e(aria)}"></a>'''
                     for href, aria, x, y, w, h in CARDS_LIVE)

# rail hitboxes: label ink spans measured from the concept rail strip (of 1536)
RAIL_HITS = [
    ('Drainage', 'services/drainage/', 74, 209),
    ('Land Clearing', 'services/land-clearing-excavation/', 314, 513),
    ('Culverts', 'services/site-prep-culverts/', 612, 745),
    ('Driveways', 'services/driveways/', 841, 984),
    ('Hardscaping', 'services/landscaping-hardscaping/', 1086, 1254),
    ('Seawalls', 'services/seawalls-retention-waterproofing/', 1275, 1478),
]
rail_hits = ''.join(
    f'<a href="{href}" style="left:{x0/15.36:.2f}%;width:{(x1-x0)/15.36:.2f}%">'
    f'<span class="sr-only">{e(lbl)}</span></a>'
    for lbl, href, x0, x1 in RAIL_HITS)

home = f"""
<div class="stage-pos d-only">
 <div class="stage">
  <section class="board">
    <h1 class="sr-only">{e(D.HEADLINE)}</h1>
    <p class="sr-only">{e(D.HERO_COPY)} {e(D.FACTS['family'])} Based in Moultrie, Georgia.</p>
    <a class="logo-live" href="./" aria-label="Environmental Construction Services — home"><img src="assets/ecs-logo-plated.png" alt=""></a>
    <nav class="primary stage-nav" aria-label="Primary">
      <a href="./" aria-current="page">Home</a><a href="services/">Services</a><a href="about/">About</a><a href="contact/">Contact</a>
    </nav>
    <div class="btn-row stage-cta settle-2">
      <a class="btn fill" href="services/">{e(D.CTA_LABEL)}</a>
      <a class="btn line" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
    </div>{cards_live}
  </section>
 </div>
</div>
<div class="torn2 d-only" aria-hidden="true"></div>
<div class="rail2 d-only">
  <nav class="rail-hit" aria-label="Service index">{rail_hits}</nav>
</div>
<div class="m-only">
<div class="wrap">
<section class="hero">
  <div class="hero-copy">
    <h1 class="reveal-mask">{''.join(f'<span class="ln">{e(ln)}</span>' for ln in D.HEADLINE_LINES)}</h1>
    <div class="underline draw" aria-hidden="true"></div>
    <p class="sub settle">{e(D.HERO_COPY)}</p>
    <div class="btn-row settle-2">
      <a class="btn fill" href="services/">{e(D.CTA_LABEL)}</a>
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
</div>
<div class="stage-pos"><div class="stage"><div class="wrap">
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
</div></div></div>
"""

# ------------------------------------------------------------------ services
services_body = f"""
<section class="sec">
  {sec_head('field note index —', 'Services.')}
  <p style="max-width:56ch;margin-top:1rem">Six categories of ground work, shown in photographs
  of Environmental Construction Services' own projects.</p>
  <div class="atlas">
{atlas.replace('href="services/', 'href="').replace('src="assets/', 'src="../assets/')}
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
      <img src="../../assets/{s['asset']}" alt="Environmental Construction Services {e(s['label'].lower())} project photo">
      <figcaption>Photo: Environmental Construction Services — from their public site.</figcaption>
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
      <img src="../assets/photo-about-family.jpg" alt="The family behind Environmental Construction Services">
      <figcaption>Photo: Environmental Construction Services — from their public site.</figcaption>
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
    <p>{e(D.NOTICES[1])} The landing page's graphite drawings are generated concept art in a
    field-notes style, created to demonstrate a design direction; the project photographs on
    the service and about pages come from Environmental Construction Services' own public
    website and were not altered beyond cropping and resizing.</p>
    <p>The concept is marked noindex/nofollow and its robots.txt asks crawlers to stay out.</p>
    <p>To reach the real business: <a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a>
    or <a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a>.</p>
  </div>
</section>
"""

NAME = D.FACTS['name']
W = lambda b: f'<div class="stage-pos"><div class="stage"><div class="wrap">{b}</div></div></div>'
page('', f'{NAME} — Moultrie, GA (Concept)', 'Private field-notes website concept: drainage, land clearing, excavation, site preparation, culverts, and driveways in Moultrie, GA.', home, note='FIELD NOTE 01', current='', kind='home')
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
