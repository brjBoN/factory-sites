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

NAV = [('', 'Home'), ('services/', 'Services'), ('blog/', 'Blog'), ('about/', 'About'), ('contact/', 'Contact')]


def page(route, title, desc, body, note='FIELD NOTE 01', current=None, kind='interior'):
    depth = 0 if route == '' else route.rstrip('/').count('/') + 1
    rel = '../' * depth
    exact_nav_href = f"{route.rstrip('/')}/" if route else ''

    def nav_current(href):
        if href != current:
            return ''
        value = 'page' if href == exact_nav_href else 'location'
        return f' aria-current="{value}"'

    nav = ''.join(
        f'<a href="{rel}{href}"{nav_current(href)}>{label}</a>'
        for href, label in NAV)
    # painted brad+FIELD NOTE 01 on home; brad alone on interior pages
    ledger_art = (f'<img class="lednote" src="{rel}assets/fieldnote-01.png" alt="">'
                  if kind == 'home' else
                  f'<img class="ledbrad" src="{rel}assets/brad-brass.png" alt="">')
    # Keep repeated desktop navigation outside the main landmark so the skip
    # link bypasses it on every route, including the concept-canvas homepage.
    if kind == 'home':
        board_header = f"""
<div class="stage-pos d-only home-header-overlay">
 <div class="stage home-header-stage">
    <a class="logo-live" href="./" aria-label="Environmental Construction Services — home"><img src="assets/ecs-logo-plated.png" alt=""></a>
    <span class="desktop-locnote" aria-hidden="true">
      <span class="desktop-locline">{e(D.FACTS['location_annotation'])}</span>
      <span class="desktop-coords">{e(D.FACTS['location_coords'])}</span>
    </span>
    <nav class="primary stage-nav" aria-label="Desktop primary navigation">{nav}</nav>
 </div>
</div>"""
    else:
        board_header = f"""
<div class="stage-pos d-only">
 <div class="stage">
  <div class="board-header" style="background-image:url('{rel}assets/header-strip.png')">
    <a class="logo-live" href="{rel}" aria-label="Environmental Construction Services — home"><img src="{rel}assets/ecs-logo-plated.png" alt=""></a>
    <span class="desktop-locnote" aria-hidden="true">
      <span class="desktop-locline">{e(D.FACTS['location_annotation'])}</span>
      <span class="desktop-coords">{e(D.FACTS['location_coords'])}</span>
    </span>
    <nav class="primary stage-nav" aria-label="Desktop primary navigation">{nav}</nav>
  </div>
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
if(window.matchMedia('(min-width: 1101px)').matches){{
z=Math.min(1,window.innerWidth/1536);}}
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
      <img class="nm-ink" src="{rel}assets/wordmark-ink.png" alt="Environmental Construction Services">
    </a>
    <span class="locnote" aria-hidden="true"><span class="locline">{e(D.FACTS['location_annotation'])}</span><span class="coords">{e(D.FACTS['location_coords'])}</span></span>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation-mobile" aria-label="Open menu"><span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span></button>
    <nav class="primary" id="primary-navigation-mobile" aria-label="Mobile primary navigation">
      {nav}
    </nav>
  </div>
</header>
</div>{board_header}
<main id="main" tabindex="-1">
{body}
</main>
<footer class="site">
<div class="stage-pos"><div class="stage">
  <div class="foot-in">
    <div>
      <h2>Environmental Construction Services</h2>
      <ul>
        <li>{e(D.FACTS['family'])}</li>
        <li>{e(D.FACTS['address'])}</li>
      </ul>
    </div>
    <div>
      <h2>Reach Us</h2>
      <ul>
        <li><a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a></li>
        <li><a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a></li>
      </ul>
    </div>
    <div>
      <h2>Concept Pages</h2>
      <ul>
        <li><a href="{rel}services/">Services</a></li>
        <li><a href="{rel}blog/">Blog</a></li>
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


def sec_head(eyebrow, title, level=2):
    if level not in (1, 2):
        raise ValueError('section heading level must be 1 or 2')
    return (f'<p class="eyebrow">{e(eyebrow)}</p>'
            f'<h{level} class="display">{e(title)}</h{level}><div class="rule-red" aria-hidden="true"></div>')


# --------------------------------------------------------------------- home
# Live-text paper cards, stacked full-width on the responsive home layout.
pinned = ''.join(f'''
  <a class="pin-card" href="{p['href']}" aria-label="{e(p['aria'])}">
    <span class="thumb" aria-hidden="true"><img src="assets/{p['asset']}" alt=""></span>
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
    <div class="cap"><h3>{e(s['label'])}</h3><span class="fn">{e(s['note'])}</span></div>
  </a>''' for s in D.SERVICES)

# Live card links sit at the concept-canvas coordinates. Each real-text label
# covers the rasterized label in the underlying art while retaining its card.
CARDS_LIVE = [
    ('services/drainage/', 'CONTROL WATER', 'CONTROL WATER — explore drainage services', 62, 745, 406, 125),
    ('services/land-clearing-excavation/',
     'CLEAR & PREP', 'CLEAR & PREP — explore land clearing, excavation, and site preparation services', 490, 738, 368, 132),
    ('services/site-prep-culverts/',
     'BUILD ACCESS', 'BUILD ACCESS — explore culvert and driveway services', 881, 749, 372, 121),
]
cards_live = ''.join(f'''
    <a class="card-hit" style="left:{x/14.48:.3f}%;top:{y/8.85:.3f}%;width:{w/14.48:.3f}%;height:{h/8.85:.3f}%" href="{href}" aria-label="{e(aria)}"><span class="card-label" aria-hidden="true">{e(label)}</span></a>'''
                     for href, label, aria, x, y, w, h in CARDS_LIVE)

# The desktop rail uses live text rather than rasterized labels.
RAIL_HITS = [
    ('Drainage', 'services/drainage/'),
    ('Land Clearing', 'services/land-clearing-excavation/'),
    ('Culverts', 'services/site-prep-culverts/'),
    ('Driveways', 'services/driveways/'),
    ('Hardscaping', 'services/landscaping-hardscaping/'),
    ('Seawalls', 'services/seawalls-retention-waterproofing/'),
]
rail_hits = ''.join(
    f'<a href="{href}">{e(lbl)}</a>'
    for lbl, href in RAIL_HITS)

home = f"""
<div class="stage-pos d-only">
 <div class="stage">
  <section class="board">
    <div class="desktop-copy">
      <h1><span>Start with</span><span>the ground.</span></h1>
      <span class="desktop-underline" aria-hidden="true"></span>
      <p>{e(D.HERO_COPY)}</p>
    </div>
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
  <span class="rail-notice" aria-hidden="true">Private website concept</span>
</div>
<div class="m-only">
<div class="wrap">
<section class="hero">
  <div class="hero-copy">
    <div class="m-hero-top">
      <h1 class="m-headline settle"><span>Start with</span><span>the ground.</span></h1>
      <div class="hero-art mobile settle" aria-hidden="true"><img src="assets/hero-collage-mobile-sheet.png" alt=""></div>
    </div>
    <p class="sub settle">{e(D.HERO_COPY)}</p>
    <div class="btn-row settle-2">
      <a class="btn fill" href="services/">{e(D.CTA_LABEL)}</a>
      <a class="btn line" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
    </div>
  </div>
  <div class="hero-art desktop settle" aria-hidden="true"><img src="assets/hero-excavation-collage.webp" alt=""></div>
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
  {sec_head('field note index —', 'Services.', level=1)}
  <p style="max-width:56ch;margin-top:1rem">Six categories of ground work, shown in photographs
  of Environmental Construction Services' own projects.</p>
  <div class="atlas">
{atlas.replace('href="services/', 'href="').replace('src="assets/', 'src="../assets/').replace('<h3>', '<h2>').replace('</h3>', '</h2>')}
  </div>
</section>
"""

# --------------------------------------------------------------- service page
def svc_body(s):
    return f"""
<section class="sec">
  <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../">Services</a></li><li aria-current="page">{e(s['label'])}</li></ol></nav>
  {sec_head(s['note'].lower() + ' —', s['label'] + '.', level=1)}
  <div class="svc-grid">
    <figure class="svc-art">
      <img src="../../assets/{s['asset']}" alt="{e(s['alt'])}">
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
  {sec_head('field note —', 'About.', level=1)}
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
  {sec_head('field note —', 'Contact.', level=1)}
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

# --------------------------------------------------------------------- blog
import blog_data as B

def post_body_html(post):
    parts = []
    for i, el in enumerate(post['body']):
        tag, txt = el[0], el[1]
        if tag == 'img':
            if parts and parts[-1].endswith('</li>'):
                parts.append('</ul>')
            alt = el[2] if len(el) > 2 and el[2] else post['title']
            parts.append(f'<figure class="post-img"><img src="../../assets/{txt}" alt="{e(alt)}" loading="lazy"></figure>')
        elif tag in ('h2', 'h3'):
            if parts and parts[-1].endswith('</li>'):
                parts.append('</ul>')
            parts.append(f'<h2>{e(txt)}</h2>')
        elif tag == 'li':
            if not parts or not parts[-1].endswith('</li>'):
                parts.append('<ul>')
            parts.append(f'<li>{e(txt)}</li>')
        elif tag == 'kick':
            if parts and parts[-1].endswith('</li>'):
                parts.append('</ul>')
            parts.append(f'<p class="kicker">{e(txt)}</p>')
        else:
            if parts and parts[-1].endswith('</li>'):
                parts.append('</ul>')
            cls = ' class="lead"' if not any(p.startswith('<p') for p in parts) else (
                ' class="kicker"' if len(txt) < 60 and txt.endswith(':') else '')
            parts.append(f'<p{cls}>{e(txt)}</p>')
    if parts and parts[-1].endswith('</li>'):
        parts.append('</ul>')
    return '\n'.join(parts)

def fmt_date(d):
    try:
        y, m, dd = d.split('-')
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        return f'{months[int(m)]} {int(dd)}, {y}'
    except Exception:
        return d

def excerpt(t, n=210):
    if len(t) <= n:
        return t
    return t[:n].rsplit(' ', 1)[0].rstrip(',;:') + ' …'

def card_thumb(p):
    if not p.get('cover'):
        return ''
    return f'<span class="log-thumb"><img src="../assets/{p["cover"]}" alt="" loading="lazy"></span>'

COVER_ALTS = {
    'blog-img-01.jpg': 'Standing water pooled beside a wet residential walkway',
    'blog-img-09.jpg': 'A grass-lined drainage channel carrying water between homes',
    'blog-img-11.jpg': 'Excavators working beside a partially demolished building',
}

def cover_alt(p):
    cover = p.get('cover')
    if not cover:
        return ''
    # When the same photograph appears later with a full description, keep the
    # editorial cover decorative so screen readers do not hear it twice.
    if any(el[0] == 'img' and el[1] == cover for el in p['body']):
        return ''
    return COVER_ALTS.get(cover, '')

blog_cards = ''.join(f'''
  <a class="log-card{" has-thumb" if p.get("cover") else ""}" href="../post/{p['slug']}/">
    {card_thumb(p)}<div class="log-body">
    <span class="meta">Log {i:02d} — {e(fmt_date(p['date']))}</span>
    <h2>{e(p['title'])}</h2>
    <p>{e(excerpt(p['desc']))}</p>
    <span class="go">Read the entry &#8594;</span>
    </div>
  </a>''' for i, p in enumerate(B.POSTS, 1))

blog_body = f"""
<section class="sec">
  {sec_head('the field log —', 'Blog.', level=1)}
  <p style="max-width:60ch;margin-top:1rem">Notes from the ground — every entry below is
  reproduced from Environmental Construction Services' own blog.</p>
  <div class="log-list">
{blog_cards}
  </div>
</section>
"""

def post_page_body(p):
    return f"""
<section class="sec">
  <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../../blog/">Blog</a></li><li aria-current="page">Field log</li></ol></nav>
  <article class="post">
    <p class="meta">{e(fmt_date(p['date']))} — Environmental Construction Services</p>
    {sec_head('field log —', p['title'], level=1)}
    {f'<figure class="post-img cover"><img src="../../assets/{p["cover"]}" alt="{e(cover_alt(p))}"></figure>' if p.get('cover') else ''}
    {post_body_html(p)}
    <p class="post-src">Reproduced from Environmental Construction Services' public blog
    (environmentalconstructions.com). Part of this private website concept.</p>
  </article>
</section>
"""

# -------------------------------------------------------------- accessibility
access_body = """
<section class="sec">
  <p class="eyebrow">the fine print —</p>
  <h1 class="display">Accessibility.</h1><div class="rule-red" aria-hidden="true"></div>
  <div class="svc-copy" style="max-width:60ch;margin-top:1rem">
    <p><strong>WCAG 2.2 Level AA is the ongoing accessibility target for this concept.</strong>
    We continue reviewing its structure, navigation, focus indicators, text contrast,
    responsive behavior, and controls as the site changes.</p>
    <p><strong>Last reviewed:</strong> July 27, 2026.</p>
    <p>Animations respect your system's reduced-motion setting — with it enabled, drawing
    effects, parallax, and reveals are replaced with immediate content.</p>
    <p>Except for the business logo, page text is rendered as real text so it can be resized
    and adapted. Decorative illustrations are hidden from assistive technology; meaningful
    project photographs include descriptions.</p>
    <p>If something on this concept doesn't work well for you, call
    <a href="tel:+12295160821">(229) 516-0821</a> or email
    <a href="mailto:ecs.outdoorcustoms@gmail.com">ecs.outdoorcustoms@gmail.com</a>.</p>
  </div>
</section>
"""

# ------------------------------------------------------------ concept-data-use
datause_body = f"""
<section class="sec">
  <p class="eyebrow">the fine print —</p>
  <h1 class="display">Concept &amp; Data Use.</h1><div class="rule-red" aria-hidden="true"></div>
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
page('blog', f'Blog — {NAME} (Concept)', 'Field log: drainage, grading, clearing, and land management notes from Environmental Construction Services.', W(blog_body), note='FIELD LOG', current='blog/')
for i, p in enumerate(B.POSTS, 1):
    page(f'post/{p["slug"]}', f'{p["title"]} — {NAME} (Concept)', p['desc'][:150],
         W(post_page_body(p)), note=f'LOG {i:02d}', current='blog/')
page('about', f'About — {NAME} (Concept)', 'Family-owned and operated groundwork in Moultrie, GA.', W(about_body), note='FIELD NOTE 08', current='about/')
page('contact', f'Contact — {NAME} (Concept)', 'Phone, email, and address for Environmental Construction Services.', W(contact_body), note='FIELD NOTE 09', current='contact/')
page('accessibility', f'Accessibility — {NAME} (Concept)', 'Accessibility commitments for this private concept.', W(access_body), note='APPENDIX A')
page('concept-data-use', f'Concept & Data Use — {NAME} (Concept)', 'What this private concept is, and what it does not collect.', W(datause_body), note='APPENDIX B')

(OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8', newline='\n')
print('wrote robots.txt')
print('done')
