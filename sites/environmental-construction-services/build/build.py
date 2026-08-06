"""Generate the private ECS drainage field-notes concept as static HTML.

Run ``python build.py`` from this directory. Routes are emitted as nested
``index.html`` files so every internal link remains relative and portable.
"""

import html as H
import json
from pathlib import Path

import data as D


OUT = Path(__file__).resolve().parents[1]
e = lambda value: H.escape(str(value), quote=True)
SITE_URL = 'https://ecs-drainage-field-notes.vercel.app'
BLOG_POSTS = json.loads(
    (Path(__file__).resolve().parent / 'blog-posts.json').read_text(encoding='utf-8')
)
BUSINESS_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'HomeAndConstructionBusiness',
    'name': 'Environmental Construction Services',
    'url': SITE_URL,
    'telephone': '+1-229-516-0821',
    'email': 'ecs.outdoorcustoms@gmail.com',
    'image': f'{SITE_URL}/assets/ecs-logo-plated.png',
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': '33 Pine Cone Road',
        'addressLocality': 'Moultrie',
        'addressRegion': 'GA',
        'postalCode': '31768',
        'addressCountry': 'US',
    },
    'areaServed': 'South Georgia',
    'sameAs': [
        'https://www.facebook.com/Environmentalcs/',
        'https://www.instagram.com/environmentalcs/',
    ],
}

FONTS = (
    'https://fonts.googleapis.com/css2?family=League+Gothic&'
    'family=Barlow:wght@400;500;600;700&'
    'family=Barlow+Condensed:wght@400;500;600&'
    'family=Roboto+Condensed:wght@700&'
    'family=Caveat:wght@500&family=Architects+Daughter&display=swap'
)

NAV = [
    ('', 'Home'),
    ('about/', 'About'),
    ('drainage/', 'Drainage'),
    ('services/', 'Services'),
    ('projects/', 'Projects'),
    ('blog/', 'Blog'),
    ('contact/', 'Contact'),
]


def page(route, title, desc, body, note='FIELD NOTE 01', current=None,
         kind='interior', head_extra='', og_type='website', social_image=None,
         social_alt=None, canonical=None, published_time=None, author=None,
         structured_data=None):
    """Write one page while retaining the approved blueprint wrapper."""
    depth = 0 if route == '' else route.rstrip('/').count('/') + 1
    rel = '../' * depth
    exact_nav_href = f"{route.rstrip('/')}/" if route else ''

    def nav_current(href):
        if href != current:
            return ''
        value = 'page' if href == exact_nav_href else 'location'
        return f' aria-current="{value}"'

    nav = ''.join(
        f'<a href="{rel}{href}"{nav_current(href)}>{e(label)}</a>'
        for href, label in NAV
    )
    mobile_nav = (
        nav + f'<a class="mobile-call" href="{D.FACTS["phone_href"]}">'
        f'Call {e(D.FACTS["phone_display"])}</a>'
    )
    ledger_art = (
        f'<img class="lednote" src="{rel}assets/fieldnote-01.png" alt="">'
        if kind == 'home'
        else f'<img class="ledbrad" src="{rel}assets/brad-brass.png" alt="">'
    )

    if kind == 'home':
        board_header = f"""
<div class="stage-pos d-only home-header-overlay">
 <div class="stage home-header-stage">
  <a class="logo-live" href="./" aria-label="Environmental Construction Services — home"><img src="assets/ecs-logo-plated.png" alt=""></a>
  <nav class="primary stage-nav" aria-label="Desktop primary navigation">{nav}</nav>
 </div>
</div>"""
    else:
        board_header = f"""
<div class="stage-pos d-only">
 <div class="stage">
  <div class="board-header" style="background-image:url('{rel}assets/header-strip.png')">
   <a class="logo-live" href="{rel}" aria-label="Environmental Construction Services — home"><img src="{rel}assets/ecs-logo-plated.png" alt=""></a>
   <nav class="primary stage-nav" aria-label="Desktop primary navigation">{nav}</nav>
  </div>
 </div>
</div>"""

    footer_nav = ''.join(
        f'<li><a href="{rel}{href}">{e(label)}</a></li>'
        for href, label in NAV
    )
    notices = ''.join(f'    <p>{e(item)}</p>' for item in D.NOTICES)
    page_url = f"{SITE_URL}/{route.strip('/') + '/' if route else ''}"
    canonical_url = canonical or page_url
    social_image = social_image or f'{SITE_URL}/assets/ecs-drainage-field-notes-og.png'
    social_alt = social_alt or 'Environmental Construction Services drainage and site work in South Georgia'
    article_meta = ''
    if published_time:
        article_meta += f'<meta property="article:published_time" content="{e(published_time)}">\n'
    if author:
        article_meta += f'<meta property="article:author" content="{e(author)}">\n'
    schemas = [BUSINESS_SCHEMA]
    if structured_data:
        schemas.extend(structured_data if isinstance(structured_data, list) else [structured_data])
    schema_html = '\n'.join(
        '<script type="application/ld+json">' +
        json.dumps(item, ensure_ascii=False).replace('</', '<\\/') + '</script>'
        for item in schemas
    )
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="application-name" content="Environmental Construction Services">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canonical_url)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{e(og_type)}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Environmental Construction Services">
<meta property="og:url" content="{e(canonical_url)}">
<meta property="og:image" content="{e(social_image)}">
<meta property="og:image:alt" content="{e(social_alt)}">
{article_meta}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{e(social_image)}">
{schema_html}
{head_extra}
<link rel="icon" href="{rel}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body data-page="{e(kind)}">
<script>
(function(){{var f=function(){{var z=1;
if(window.matchMedia('(min-width: 1101px)').matches){{
var w=document.documentElement.clientWidth||window.innerWidth;
z=Math.min(1,w/1536);}}
document.documentElement.style.setProperty('--zoom',z);}};
window.addEventListener('resize',f);
document.addEventListener('DOMContentLoaded',f);
window.addEventListener('load',f);
f();}})();
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
   <nav class="primary" id="primary-navigation-mobile" aria-label="Mobile primary navigation">{mobile_nav}</nav>
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
    <h2>{e(D.FACTS['name'])}</h2>
    <ul>
     <li>{e(D.FACTS['family'])}</li>
     <li><a href="{D.FACTS['map_href']}" target="_blank" rel="noreferrer">{e(D.FACTS['address'])}</a></li>
    </ul>
   </div>
   <div>
    <h2>Reach ECS</h2>
    <ul>
     <li><a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a></li>
     <li><a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a></li>
    </ul>
    <div class="social-row">
     <a href="{D.FACTS['facebook_href']}" target="_blank" rel="noreferrer">Facebook</a>
     <a href="{D.FACTS['instagram_href']}" target="_blank" rel="noreferrer">Instagram</a>
    </div>
   </div>
   <div>
    <h2>Concept Pages</h2>
    <ul>
     {footer_nav}
     <li><a href="{rel}accessibility/">Accessibility</a></li>
     <li><a href="{rel}concept-data-use/">Concept &amp; Data Use</a></li>
    </ul>
   </div>
  </div>
  <div class="footer-bottom"><span>© 2026 {e(D.FACTS['name_llc'])}</span><span>Drainage &amp; site work across South Georgia.</span></div>
  <div class="notices">
{notices}
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
    return (
        f'<p class="eyebrow">{e(eyebrow)}</p>'
        f'<h{level} class="display">{e(title)}</h{level}>'
        '<div class="rule-red" aria-hidden="true"></div>'
    )


def wrap(body):
    return f'<div class="stage-pos"><div class="stage"><div class="wrap">{body}</div></div></div>'


def check_list(items):
    return '<ul class="check-list">' + ''.join(f'<li>{e(item)}</li>' for item in items) + '</ul>'


def note_grid(items):
    cards = []
    for index, item in enumerate(items, 1):
        number = item.get('number', f'{index:02d}')
        cards.append(
            '<article class="note-card">'
            f'<span class="note-number">{e(number)}</span>'
            f'<h3>{e(item["title"])}</h3>'
            f'<p>{e(item["copy"])}</p>'
            '</article>'
        )
    return '<div class="note-grid">' + ''.join(cards) + '</div>'


def service_href(service, at_root=True):
    if service['slug'] == 'drainage':
        return 'drainage/' if at_root else '../drainage/'
    return f'services/{service["slug"]}/' if at_root else f'{service["slug"]}/'


def service_atlas(asset_prefix, at_root=True, heading_level=3):
    cards = []
    for service in D.SERVICES:
        class_attr = ' class="primary-service"' if service['slug'] == 'drainage' else ''
        cards.append(f'''
  <a{class_attr} href="{service_href(service, at_root)}">
   <span class="art"><img src="{asset_prefix}{service['asset']}" alt="" aria-hidden="true" loading="lazy"></span>
   <div class="cap"><h{heading_level}>{e(service['label'])}</h{heading_level}><span class="fn">{e(service['note'])}</span></div>
  </a>''')
    return '<div class="atlas">' + ''.join(cards) + '</div>'


def project_cards(projects, asset_prefix):
    cards = []
    for project in projects:
        cards.append(f'''
 <article class="project-card">
  <div class="project-photo"><img src="{asset_prefix}{project['asset']}" alt="{e(project['alt'])}" loading="lazy"></div>
  <div class="project-copy">
   <p class="project-kicker"><span>{e(project['number'])}</span> {e(project['category'])}</p>
   <h3>{e(project['title'])}</h3>
   <p>{e(project['copy'])}</p>
  </div>
 </article>''')
    return '<div class="projects-grid">' + ''.join(cards) + '</div>'


def cta_sheet(kicker, title, copy, contact_href, services_href=None):
    second = (
        f'<a class="btn line" href="{services_href}">Explore ECS services</a>'
        if services_href
        else f'<a class="btn line" href="{D.FACTS["phone_href"]}">Call {e(D.FACTS["phone_display"])}</a>'
    )
    return f'''
<section class="sec cta-sheet">
 <p class="eyebrow">{e(kicker)}</p>
 <h2 class="display">{e(title)}</h2>
 <div class="rule-red" aria-hidden="true"></div>
 <p class="section-intro">{e(copy)}</p>
 <div class="btn-row">
  <a class="btn fill" href="{contact_href}">Request a consultation</a>
  {second}
 </div>
</section>'''


# --------------------------------------------------------------------- home
pinned = ''.join(f'''
 <a class="pin-card" href="{item['href']}" aria-label="{e(item['aria'])}">
  <img class="pin-card-art" src="assets/{item['asset']}" alt="" aria-hidden="true">
 </a>''' for item in D.PINNED)

rail_links = ''.join(
    f'<a href="{service_href(service, True)}">{e(service["rail_label"])}</a>'
    for service in D.SERVICES
)

card_specs = [
    ('drainage/', 'CONTROL WATER — explore ECS drainage solutions',
     62, 745, 406, 125),
    ('services/land-clearing-excavation/',
     'CLEAR & PREP — explore land clearing and excavation',
     490, 738, 368, 132),
    ('services/site-prep-culverts/',
     'BUILD ACCESS — explore site preparation and culvert work',
     881, 749, 372, 121),
]
cards_live = ''.join(f'''
 <a class="card-hit" style="left:{x/14.48:.3f}%;top:{y/8.85:.3f}%;width:{w/14.48:.3f}%;height:{h/8.85:.3f}%" href="{href}" aria-label="{e(aria)}"></a>'''
    for href, aria, x, y, w, h in card_specs)
hero_lines = ''.join(f'<span>{e(line)}</span>' for line in D.HERO['lines'])
original_card_tags = ''.join(
    f'<span>{e(label)}</span>' for label in D.ORIGINAL_HOME['cards']
)
archive_service_cards = ''.join(f'''
   <a href="{service_href(service, True)}">
    <span class="art"><img src="assets/{e(D.ORIGINAL_SERVICE_NOTES[service['slug']]['asset'])}" alt="" aria-hidden="true" loading="lazy"></span>
    <div class="cap"><h4>{e(D.ORIGINAL_SERVICE_NOTES[service['slug']]['label'])}</h4><span class="fn">{e(service['note'])}</span></div>
   </a>'''
    for service in D.SERVICES)

home = f'''
<div class="stage-pos d-only">
 <div class="stage">
  <section class="board">
   <div class="desktop-copy">
    <h1>{hero_lines}</h1>
    <span class="desktop-underline" aria-hidden="true"></span>
    <p>{e(D.HERO['lede'])}</p>
   </div>
   <div class="btn-row stage-cta settle-2">
    <a class="btn fill" href="services/">{e(D.HERO['cta'])}</a>
    <a class="btn line" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
   </div>{cards_live}
  </section>
 </div>
</div>
<div class="torn2 d-only" aria-hidden="true"></div>
<div class="rail2 d-only">
 <nav class="rail-hit" aria-label="Service index">{rail_links}</nav>
 <span class="rail-notice" aria-hidden="true">Private website concept</span>
</div>
<div class="m-only">
 <div class="wrap">
  <section class="hero">
   <div class="hero-copy">
    <div class="m-hero-top">
     <h1 class="m-headline settle">{hero_lines}</h1>
     <div class="hero-art mobile settle" aria-hidden="true"><img src="assets/hero-collage-mobile-sheet.png" alt=""></div>
    </div>
    <p class="sub settle">{e(D.HERO['lede'])}</p>
    <div class="btn-row settle-2">
     <a class="btn fill" href="services/">{e(D.HERO['cta'])}</a>
     <a class="btn line" href="{D.FACTS['phone_href']}">CALL {e(D.FACTS['phone_display'])}</a>
    </div>
   </div>
   <div class="hero-art desktop settle" aria-hidden="true"><img src="assets/hero-excavation-collage.webp" alt=""></div>
  </section>
  <div class="pinned">{pinned}</div>
 </div>
 <div class="torn" aria-hidden="true"></div>
 <div class="rail-band"><div class="rail-links">{rail_links}</div></div>
</div>
{wrap(f'''
<section class="sec primary-service">
 {sec_head('drainage expertise —', 'A better drainage plan starts with the whole property.')}
 <div class="svc-grid">
  <figure class="svc-art">
   <img src="assets/project-grading.jpg" alt="Tracked equipment grading a South Georgia project site" loading="lazy">
   <figcaption>Local conditions — South Georgia</figcaption>
  </figure>
  <div class="svc-copy">
   <p class="section-intro">Standing water is only the symptom. The real work is understanding where runoff starts, how grade and soil influence it, and where the water can safely go.</p>
   <p>ECS brings the earthwork, drainage, culvert, and site-preparation capabilities together so the solution is considered as one working system—not a patch placed on top of the problem.</p>
   {check_list(['Residential and commercial drainage', 'Drain tile, French drains, basins, and solid pipe', 'Grading, culverts, erosion control, and site work'])}
   <a class="btn line" href="drainage/">Learn about ECS drainage services</a>
  </div>
 </div>
</section>
<section class="sec">
 {sec_head('drainage & site services —', 'Coordinate the work from the ground up.')}
 <p class="section-intro">From drainage and excavation to driveways, hardscaping, and shoreline protection, ECS coordinates the work your property needs from the ground up.</p>
 {service_atlas('assets/', True)}
</section>
<section class="sec">
 {sec_head('how ECS solves drainage problems —', 'Collection, conveyance, grading, and discharge—planned together.')}
 <p class="section-intro">The right combination depends on the grade, soil, runoff, and available discharge point.</p>
 {note_grid(D.HOME_SOLUTIONS)}
</section>
<section class="sec">
 {sec_head('project gallery —', 'See ECS work across South Georgia.')}
 <p class="section-intro">From drainage excavation to concrete driveways and land clearing, every image on this site comes from ECS work and the people behind it.</p>
 {project_cards(D.PROJECTS[:3], 'assets/')}
 <div class="btn-row"><a class="btn line" href="projects/">View project gallery</a></div>
</section>
<section class="sec blueprint-archive">
 <p class="eyebrow">original blueprint field note —</p>
 <h2 class="display">{e(D.ORIGINAL_HOME['headline'])}</h2>
 <div class="rule-red" aria-hidden="true"></div>
 <p class="section-intro">{e(D.ORIGINAL_HOME['copy'])}</p>
 <div class="btn-row"><a class="btn line" href="services/">{e(D.ORIGINAL_HOME['cta'])}</a></div>
 <div class="tag-row archive-tags">{original_card_tags}</div>
 <div class="blueprint-archive-grid">
  <div class="archive-service-panel">
   <p class="eyebrow">{e(D.ORIGINAL_HOME['eyebrow'])}</p>
   <h3>{e(D.ORIGINAL_HOME['title'])}</h3>
   <div class="atlas archive-atlas" aria-label="Six kinds of groundwork">{archive_service_cards}</div>
  </div>
  <div class="archive-about-panel">
   <p class="eyebrow">{e(D.ORIGINAL_HOME['about_eyebrow'])}</p>
   <h3>{e(D.ORIGINAL_HOME['about_title'])}</h3>
   <p>{e(D.ORIGINAL_HOME['about_copy'])}</p>
   <div class="btn-row"><a class="btn fill" href="{D.FACTS['phone_href']}">Call {e(D.FACTS['phone_display'])}</a><a class="btn line" href="{D.FACTS['email_href']}">Email ECS</a></div>
  </div>
 </div>
</section>
<section class="sec testimonial-sheet">
 <p class="eyebrow">client feedback —</p>
 <blockquote>“{e(D.MARCY_TESTIMONIAL['quote'])}”<cite>— {e(D.MARCY_TESTIMONIAL['name'])}</cite></blockquote>
</section>
<section class="sec">
 {sec_head('service area —', 'Serving residential and commercial properties across South Georgia.')}
 <p class="section-intro">Family-owned and operated from 33 Pine Cone Road in Moultrie, Georgia.</p>
 <a class="btn line" href="about/">About ECS</a>
</section>
{cta_sheet('have a project in mind? —', 'Tell us about your property.', 'Whether the need is drainage, excavation, clearing, a driveway, hardscaping, or shoreline work, ECS can help define the next step.', 'contact/')}
''')}
'''


# ------------------------------------------------------------------ drainage
drainage_capabilities = ''.join(f'''
 <article class="note-card drainage-details">
  <h3>{e(item['title'])}</h3>
  <p>{e(item['copy'])}</p>
  {check_list(item['items'])}
 </article>''' for item in D.DRAINAGE_CAPABILITIES)

faqs = ''.join(f'''
 <details>
  <summary>{e(question)}</summary>
  <p>{e(answer)}</p>
 </details>''' for question, answer in D.DRAINAGE_FAQS)

drainage_body = f'''
<section class="sec primary-service">
 <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../">Home</a></li><li aria-current="page">Drainage</li></ol></nav>
 {sec_head('drainage solutions —', 'Drainage solutions for the whole property.', level=1)}
 <div class="svc-grid">
  <div class="svc-copy">
   <p class="section-intro">ECS evaluates grade, runoff, soil conditions, crossings, and available outlets, then builds a drainage system suited to the site.</p>
   <div class="btn-row">
    <a class="btn fill" href="../contact/">Request an assessment</a>
    <a class="btn line" href="{D.FACTS['phone_href']}">Call {e(D.FACTS['phone_display'])}</a>
   </div>
  </div>
  <figure class="svc-art"><img src="../assets/photo-drainage.jpg" alt="ECS excavator installing a subsurface drainage holding system in Moultrie"><figcaption>Assessment, design &amp; installation — Photo: Environmental Construction Services, from their public site.</figcaption></figure>
 </div>
</section>
<section class="sec">
 {sec_head('common drainage problems —', 'Drainage problems rarely begin where the water collects.')}
 <p class="section-intro">Effective drainage begins by looking beyond the wet spot. Grade, runoff, crossings, soil disturbance, and the final discharge point all affect the path.</p>
 {note_grid(D.DRAINAGE_PROBLEMS)}
</section>
<section class="sec" id="assessment">
 {sec_head('site assessment —', 'Find the cause before choosing the fix.')}
 <p class="section-intro">Water problems are connected to the rest of the property. ECS considers the collection area, the path between components, and where the water can discharge before settling on an approach.</p>
 {note_grid(D.DRAINAGE_ASSESSMENT)}
</section>
<section class="sec">
 {sec_head('drainage capabilities —', 'Collection, conveyance, grading, and discharge—planned together.')}
 <p class="section-intro">Every recommendation is property-specific. These are the drainage and supporting site services ECS can bring together.</p>
 <div class="note-grid">{drainage_capabilities}</div>
 <a class="btn line" href="../services/">View all ECS services</a>
</section>
<section class="sec" id="process">
 {sec_head('our process —', 'A practical plan from assessment through installation.')}
 {note_grid(D.DRAINAGE_PROCESS)}
</section>
<section class="sec">
 <div class="svc-grid">
  <figure class="svc-art"><img src="../assets/project-grading.jpg" alt="ECS tracked equipment grading a local project site" loading="lazy"><figcaption>33 Pine Cone Road — Moultrie, Georgia</figcaption></figure>
  <div class="svc-copy">
   {sec_head('local experience —', 'Designed for South Georgia soil, storms, and site conditions.')}
   <p class="kicker">Drainage + site work</p>
   <p class="section-intro">Around Moultrie and South Georgia, a drainage plan has to work with the actual grade, drive crossings, neighboring runoff, existing structures, and available discharge point.</p>
   <p>Environmental Construction Services is family-owned and operated in Moultrie. Because ECS also handles grading, culverts, excavation, and site preparation, the drainage route can be considered alongside the work needed to build it.</p>
  </div>
 </div>
</section>
<section class="sec original-field-note">
 {sec_head('original drainage field note —', D.ORIGINAL_SERVICE_NOTES['drainage']['label'])}
 <p class="section-intro">{e(D.ORIGINAL_SERVICE_NOTES['drainage']['copy'])}</p>
 <p>{e(D.ORIGINAL_HOME['consultation'])}</p>
</section>
<section class="sec">
 {sec_head('questions about drainage —', 'What to know before the site visit.')}
 <p class="section-intro">These answers provide a starting point. The site itself determines the final recommendation.</p>
 <div class="faq-list">{faqs}</div>
</section>
{cta_sheet('talk with ECS —', 'Schedule a drainage assessment.', 'Tell ECS where water collects, when it appears, and what it affects. The team will follow up to discuss the property and the appropriate next step.', '../contact/')}
'''


# ------------------------------------------------------------------ services
services_body = f'''
<section class="sec">
 {sec_head('services —', 'One contractor for drainage & site work.', level=1)}
 <p class="section-intro">From drainage and excavation to driveways, hardscaping, and shoreline protection, ECS coordinates the work your property needs from the ground up.</p>
 <p class="kicker">Drainage, earthwork &amp; finished-site construction</p>
 <div class="btn-row"><a class="btn fill" href="../contact/">Discuss your project</a><a class="btn line" href="{D.FACTS['phone_href']}">Call {e(D.FACTS['phone_display'])}</a></div>
</section>
<section class="sec primary-service">
 {sec_head('drainage expertise —', 'Drainage is planned with the rest of the site.')}
 <p class="section-intro">{e(D.SERVICES[0]['blurb'])}</p>
 <div class="note-grid">
  <article class="note-card"><span class="note-number">01</span><h3>Drain tile and French drains</h3><p>Underground routes for moving collected water through the property.</p></article>
  <article class="note-card"><span class="note-number">02</span><h3>Drain fields and septic systems</h3><p>Site-specific installation and supporting work for subsurface systems.</p></article>
  <article class="note-card"><span class="note-number">03</span><h3>Lift stations and maintenance</h3><p>Service for systems that need mechanical lift or ongoing attention.</p></article>
  <article class="note-card"><span class="note-number">04</span><h3>Grading and culverts</h3><p>Supporting site work that shapes and carries the route above and below grade.</p></article>
 </div>
 <a class="btn line" href="../drainage/">View drainage services</a>
</section>
<section class="sec">
 {sec_head('full-service capabilities —', 'Coordinate the work from excavation through the finished site.')}
 <p class="section-intro">Each capability can stand on its own. They become especially useful when excavation, access, water, grade, and the finished property need to be coordinated as one job.</p>
 <p class="kicker">Six categories of ground work, shown in photographs of Environmental Construction Services’ own projects.</p>
 {service_atlas('../assets/', False, 2)}
</section>
<section class="sec">
 {sec_head('project gallery —', 'See ECS services working together in the field.')}
 <p class="section-intro">Browse ECS project photography to see drainage, clearing, excavation, concrete, landscaping, and site work in progress and complete.</p>
 <a class="btn line" href="../projects/">View project gallery</a>
</section>
{cta_sheet('have a project in mind? —', 'Discuss your project with ECS.', 'Share the work you need completed and the current site conditions. ECS will help determine the services the project requires.', '../contact/')}
'''


def service_body(service):
    original = D.ORIGINAL_SERVICE_NOTES[service['slug']]
    drainage_link = (
        '\n    <a class="btn line" href="../../drainage/">View complete drainage field note</a>'
        if service['slug'] == 'drainage' else ''
    )
    return f'''
<section class="sec">
 <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../">Services</a></li><li aria-current="page">{e(service['label'])}</li></ol></nav>
 {sec_head(service['eyebrow'].lower() + ' —', service['title'], level=1)}
 <div class="svc-grid">
  <figure class="svc-art">
   <img src="../../assets/{service['asset']}" alt="{e(service['alt'])}">
   <figcaption>Environmental Construction Services field work</figcaption>
  </figure>
  <div class="svc-copy">
   <p class="section-intro">{e(service['blurb'])}</p>
   {check_list(service['bullets'])}
   <div class="btn-row">
    <a class="btn fill" href="../../contact/">Discuss this service</a>
    <a class="btn line" href="{D.FACTS['phone_href']}">Call {e(D.FACTS['phone_display'])}</a>
   </div>
  </div>
 </div>
</section>
<section class="sec original-field-note">
 {sec_head('original field note —', original['label'])}
 <div class="svc-grid">
  <figure class="svc-art">
   <img src="../../assets/{e(original['asset'])}" alt="{e(original['alt'])}" loading="lazy">
   <figcaption>Photo: Environmental Construction Services — from their public site.</figcaption>
  </figure>
  <div class="svc-copy">
   <p class="section-intro">{e(original['copy'])}</p>
   <p>{e(D.ORIGINAL_HOME['consultation'])}</p>
   <div class="btn-row">
    <a class="btn fill" href="{D.FACTS['phone_href']}">Call {e(D.FACTS['phone_display'])}</a>
    <a class="btn line" href="{D.FACTS['email_href']}">Email ECS</a>{drainage_link}
   </div>
  </div>
 </div>
</section>
{cta_sheet('have a project in mind? —', 'Tell ECS what needs to be done.', 'Share the site conditions, current problem, and work you have in mind. ECS will follow up to discuss the project.', '../../contact/', '../../services/')}
'''


drainage_redirect = f'''
<section class="sec primary-service">
 {sec_head('drainage specialty —', 'Drainage has its own field note.', level=1)}
 <p class="section-intro">Explore residential and commercial drainage solutions from Environmental Construction Services in Moultrie, including drain tile, French drains, grading, culverts, drain fields, lift stations, and maintenance.</p>
 <a class="btn fill" href="../../drainage/">View drainage solutions</a>
</section>
'''


# ------------------------------------------------------------------- projects
projects_body = f'''
<section class="sec">
 {sec_head('project gallery —', 'Drainage & site work across South Georgia.', level=1)}
 <p class="section-intro">A look at ECS drainage, earthwork, concrete, clearing, and site-finish projects at different stages of the job.</p>
 <div class="tag-row"><span>Drainage</span><span>Earthwork</span><span>Concrete</span><span>Site finish</span></div>
</section>
<section class="sec">
 {sec_head('recent work —', 'A closer look at ECS projects in progress and complete.')}
 <p class="section-intro">These photographs show real ECS work in progress and completed field areas. They are presented honestly: every final scope depends on the grade, soil, access, water volume, and a responsible place to direct runoff.</p>
 {project_cards(D.PROJECTS, '../assets/')}
</section>
{cta_sheet('planning a project? —', 'Tell us what needs to change on your property.', 'If you are dealing with standing water, erosion, a failing drive, or a site that needs to be prepared, start by telling ECS what you are seeing.', '../contact/', '../drainage/')}
<section class="sec original-field-note">
 {sec_head('have a project in mind? —', 'Tell ECS what needs to be done.')}
 <p class="section-intro">Share the site conditions, current problem, and work you have in mind. ECS will follow up to discuss the project.</p>
 <a class="btn fill" href="../contact/">Discuss your project</a>
</section>
'''


# ---------------------------------------------------------------------- about
principles = [
    ('01', 'Understand the site', 'Grade, soil, runoff, access, and the intended discharge point all shape the right plan. The first step is looking at the property as one connected system.'),
    ('02', 'Explain the plan', 'Brandon and the ECS team put a premium on responsiveness and practical explanations, so the property owner understands what is being built and why.'),
    ('03', 'Complete the work carefully', 'Drainage, earthwork, culverts, concrete, clearing, and finish work are approached with the same straightforward goal: solve the problem in front of the crew.'),
]
principles_html = ''.join(f'''
 <article class="principle-card"><span class="note-number">{number}</span><h3>{e(title)}</h3><p>{e(copy)}</p></article>'''
    for number, title, copy in principles)

about_facts_html = ''.join(f'''
 <div class="fact-strip-item"><span>{e(label)}</span><strong>{e(value)}</strong></div>'''
    for label, value in D.ABOUT_FACTS)

testimonials_html = ''.join(f'''
 <blockquote><p>“{e(item['quote'])}”</p><cite>— {e(item['name'])}</cite></blockquote>'''
    for item in D.TESTIMONIALS)

about_body = f'''
<section class="sec primary-service">
 {sec_head('family owned in Moultrie —', 'A local team serving South Georgia.', level=1)}
 <div class="svc-grid">
  <div class="svc-copy">
   <p class="section-intro">Led by Brandon Joins, ECS combines drainage expertise with practical earthwork and site construction for residential and commercial properties.</p>
   <div class="btn-row"><a class="btn fill" href="../projects/">See the work</a><a class="btn line" href="{D.FACTS['phone_href']}">Call Brandon</a></div>
  </div>
  <figure class="svc-art"><img src="../assets/family-current.jpeg" alt="Brandon Joins with his family in Moultrie, Georgia"><figcaption>Moultrie, Georgia — ECS in the field</figcaption></figure>
 </div>
</section>
<section class="sec fact-strip" aria-label="Environmental Construction Services at a glance">
 <div class="fact-strip-grid">{about_facts_html}</div>
</section>
<section class="sec">
 {sec_head('how ECS works —', 'Every project starts with understanding the site.')}
 <div class="svc-copy">
  <p class="section-intro">Standing water, soft ground, erosion, and repeated washouts are symptoms. ECS looks at the larger site: where the water begins, how the grade influences it, and what the property needs to function better.</p>
  <p>That understanding of grade, runoff, access, and soil carries through the rest of the company’s work. Culverts, site preparation, land clearing, driveways, hardscaping, and shoreline work all depend on understanding the ground before construction begins.</p>
  <p>Brandon’s approach is direct: communicate clearly, bring the right equipment, and stay focused on the actual field conditions. It is a local family business, and the relationship with the property owner matters alongside the finished work.</p>
  {check_list(['Drainage is treated as a complete site system', 'Residential and commercial work', 'Based in Moultrie and serving surrounding communities'])}
 </div>
</section>
<section class="sec original-about-note">
 {sec_head('original company field note —', 'About ECS.')}
 <div class="svc-grid">
  <div class="svc-copy">
   <p class="section-intro">{e(D.ORIGINAL_ABOUT['copy'])}</p>
   <p>{e(D.ORIGINAL_ABOUT['fit'])}</p>
   <p class="kicker">Site conditions guide the work.</p>
  </div>
  <figure class="svc-art"><img src="../assets/{e(D.ORIGINAL_ABOUT['asset'])}" alt="{e(D.ORIGINAL_ABOUT['alt'])}" loading="lazy"><figcaption>Photo: Environmental Construction Services — from their public site.</figcaption></figure>
 </div>
</section>
<section class="sec">
 {sec_head('what clients can expect —', 'Clear recommendations and dependable field work.')}
 <p class="section-intro">The scope changes from property to property. The standard for understanding it does not.</p>
 <div class="principles-grid">{principles_html}</div>
</section>
<section class="sec testimonial-sheet">
 <p class="eyebrow">client feedback —</p>
 <h2 class="display">What property owners say about ECS.</h2>
 <div class="rule-red" aria-hidden="true"></div>
 <div class="testimonial-grid">{testimonials_html}</div>
 <div class="btn-row"><a class="btn line" href="../projects/">View project gallery</a></div>
</section>
{cta_sheet('talk with ECS —', 'Tell us about the work you need.', 'Whether the need is drainage, clearing, grading, access, or finished construction, the conversation begins with the property.', '../contact/')}
'''


# -------------------------------------------------------------------- contact
contact_tags = ''.join(f'<span>{e(tag)}</span>' for tag in D.CONTACT_SERVICE_TAGS)
contact_service_options = ''.join(
    f'<option>{e(option)}</option>' for option in D.CONTACT_SERVICE_TAGS
)
contact_timing_options = ''.join(
    f'<option>{e(option)}</option>' for option in D.CONTACT_TIMING_OPTIONS
)
contact_body = f'''
<section class="sec">
 {sec_head('contact ECS —', 'Tell us about your property.', level=1)}
 <p class="section-intro">Describe the drainage concern, site conditions, or work you have in mind. ECS will help determine the best next step.</p>
</section>
<section class="sec contact-layout">
 <div class="contact-sheet">
  {sec_head('Moultrie, Georgia —', 'Speak directly with the ECS team.')}
  <p>Based in Moultrie and serving surrounding South Georgia properties. Free estimates are available.</p>
  <div class="contact-links">
   <a href="{D.FACTS['phone_href']}"><span>Phone</span><strong>{e(D.FACTS['phone_display'])}</strong></a>
   <a href="{D.FACTS['email_href']}"><span>Email</span><strong>{e(D.FACTS['email_display'])}</strong></a>
   <a href="{D.FACTS['map_href']}" target="_blank" rel="noreferrer"><span>Address</span><strong>{e(D.FACTS['address_street'])}<br>Moultrie, GA 31768</strong></a>
   <div class="contact-fact"><span>Ownership</span><strong>Family-owned and operated.</strong></div>
  </div>
  <div class="social-row"><a href="{D.FACTS['facebook_href']}" target="_blank" rel="noreferrer">Facebook</a><a href="{D.FACTS['instagram_href']}" target="_blank" rel="noreferrer">Instagram</a></div>
 </div>
 <form class="prep-sheet assessment-form" data-ecs-request action="{D.FACTS['email_href']}" method="post" enctype="text/plain" novalidate>
  <div class="form-heading">
   <p class="eyebrow">project details —</p>
   <h2>Request a site consultation</h2>
   <p>Share the basics and your email app will open with a complete request ready to send directly to ECS.</p>
  </div>
  <p class="form-status" role="status" aria-live="polite"></p>
  <div class="form-grid">
   <label for="request-name"><span>Name *</span></label>
   <input id="request-name" name="name" autocomplete="name" required>
   <label for="request-phone"><span>Phone</span></label>
   <input id="request-phone" name="phone" type="tel" autocomplete="tel">
   <label for="request-email"><span>Email</span></label>
   <input id="request-email" name="email" type="email" autocomplete="email">
   <label for="request-location"><span>Property city or address</span></label>
   <input id="request-location" name="location" autocomplete="street-address">
   <label for="request-service"><span>What can we help with? *</span></label>
   <select id="request-service" name="service" required>{contact_service_options}</select>
   <label for="request-timing"><span>Project timing</span></label>
   <select id="request-timing" name="timing">{contact_timing_options}</select>
   <label for="request-issue"><span>What is happening on the property? *</span></label>
   <textarea id="request-issue" name="issue" rows="5" placeholder="For drainage: where does water collect, where does it seem to come from, and what have you noticed after heavy rain?" required></textarea>
   <label for="request-notes"><span>Anything else we should know?</span></label>
   <textarea id="request-notes" name="notes" rows="3"></textarea>
  </div>
  <div class="form-submit-row">
   <button class="btn fill" type="submit">Prepare project request</button>
   <a href="{D.FACTS['email_href']}">Or email ECS directly</a>
  </div>
  <p class="form-privacy">This private concept does not send or store the form. Selecting “Prepare project request” opens your own email app; review the message there, then choose whether to send it.</p>
 </form>
</section>
<section class="sec">
 {sec_head('what can ECS help with? —', 'Drainage first, with the site work around it.')}
 <div class="tag-row">{contact_tags}</div>
</section>
{cta_sheet('project details —', 'Request a site consultation.', 'Share the basics directly with ECS so the team can discuss the property and the appropriate next step.', D.FACTS['email_href'])}
'''


# ---------------------------------------------------------------------- blog
def local_blog_asset(source):
    """Map the drainage site's public image URLs to this concept's local assets."""
    filename = Path(source).name
    if filename == 'ecs-cleared-property.jpg':
        return 'project-cleared-property.jpg'
    return filename


def post_body_html(post):
    parts = []
    list_open = False
    paragraph_count = 0

    def close_list():
        nonlocal list_open
        if list_open:
            parts.append('</ul>')
            list_open = False

    for block in post['body']:
        tag = block['type']
        if tag == 'image' and block['src'] == post['cover']:
            continue
        if tag == 'image':
            close_list()
            alt = block.get('alt') or post['title']
            asset = local_blog_asset(block['src'])
            parts.append(
                f'<figure class="post-img"><img src="../../assets/{e(asset)}" '
                f'alt="{e(alt)}" loading="lazy"><figcaption>{e(alt)}</figcaption></figure>'
            )
        elif tag == 'heading':
            close_list()
            parts.append(f'<h2>{e(block["text"])}</h2>')
        elif tag == 'subheading':
            close_list()
            parts.append(f'<h3>{e(block["text"])}</h3>')
        elif tag == 'listItem':
            if not list_open:
                parts.append('<ul>')
                list_open = True
            parts.append(f'<li>{e(block["text"])}</li>')
        else:
            close_list()
            cls = ' class="lead"' if paragraph_count == 0 else ''
            parts.append(f'<p{cls}>{e(block["text"])}</p>')
            paragraph_count += 1
    close_list()
    return '\n'.join(parts)


def fmt_date(date):
    try:
        year, month, day = date.split('-')
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        return f'{months[int(month)]} {int(day)}, {year}'
    except Exception:
        return date


def card_thumb(post):
    asset = local_blog_asset(post['cover'])
    return f'<span class="log-thumb"><img src="../assets/{e(asset)}" alt="" loading="lazy"></span>'


blog_cards = ''.join(f'''
 <a class="log-card has-thumb{' is-featured' if index == 1 else ''}" href="../blog/{post['slug']}/">
  {card_thumb(post)}<div class="log-body">
   <span class="meta">{'Latest field note' if index == 1 else f'Log {index:02d}'} — {e(post['category'])} — {e(post['readingTime'])} — {e(fmt_date(post['date']))}</span>
   <h2>{e(post['title'])}</h2>
   <p>{e(post['description'])}</p>
   <span class="go">Read the article &#8594;</span>
  </div>
 </a>''' for index, post in enumerate(BLOG_POSTS, 1))

blog_body = f'''
<section class="sec">
 {sec_head('ECS field notes —', 'Practical guidance for better properties.', level=1)}
 <p class="section-intro">Straightforward resources on drainage, grading, land management, and the site conditions that shape work across South Georgia.</p>
 <p class="blog-origin">Notes from the ground — every entry below is reproduced from Environmental Construction Services’ own blog.</p>
</section>
<section class="sec">
 {sec_head('the complete library —', 'Field notes from ECS.')}
 <p class="section-intro">Browse every article from the Environmental Construction Services resource library.</p>
 <div class="log-list">{blog_cards}</div>
</section>
{cta_sheet('need help on your property? —', 'Put the field notes into practice.', 'Share what the water, soil, access, or site is doing. ECS can evaluate the property and recommend a practical next step.', '../contact/')}
'''


def post_page_body(post):
    cover_asset = local_blog_asset(post['cover'])
    related = [item for item in BLOG_POSTS if item['slug'] != post['slug']][:3]
    related_html = ''.join(f'''
 <a class="related-card" href="../../blog/{item['slug']}/">
  <span>{e(item['category'])}</span><strong>{e(item['title'])}</strong>
  <small>{e(fmt_date(item['date']))} &#8594;</small>
 </a>''' for item in related)
    return f'''
<section class="sec">
 <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../../">Home</a></li><li><a href="../../blog/">Field notes</a></li><li aria-current="page">{e(post['category'])}</li></ol></nav>
 <article class="post post-rich">
  <p class="meta">{e(post['category'])} — {e(fmt_date(post['date']))} — {e(post['readingTime'])} — Environmental Construction Services</p>
  {sec_head('field note —', post['title'], level=1)}
  <p class="post-description">{e(post['description'])}</p>
  <figure class="post-img cover"><img src="../../assets/{e(cover_asset)}" alt="{e(post['coverAlt'])}"></figure>
  <div class="article-layout">
   <aside class="article-sidebar">
    <p class="eyebrow">ECS field notes —</p>
    <h2>Questions about your property?</h2>
    <p>Every site behaves differently. ECS can evaluate the real conditions before recommending work.</p>
    <a class="btn fill" href="../../contact/">Request a consultation</a>
   </aside>
   <div class="article-body">
    <p class="article-origin-note">This article first appeared in the Environmental Construction Services resource library. General guidance is provided for education; actual site conditions and project requirements vary.</p>
    {post_body_html(post)}
    <div class="article-end"><span>Environmental Construction Services</span><strong>Drainage and site work for South Georgia properties.</strong></div>
    <p class="post-src">Reproduced from Environmental Construction Services’ public blog (environmentalconstructions.com). Part of this private website concept.</p>
   </div>
  </div>
 </article>
</section>
<section class="sec related-notes">
 {sec_head('keep reading —', 'More field notes.')}
 <div class="related-grid">{related_html}</div>
 <div class="btn-row"><a class="btn line" href="../../blog/">View all articles</a><a class="text-link" href="../../blog/">&#8592; Back to all field notes</a></div>
</section>
{cta_sheet('ready to discuss the site? —', 'Get recommendations for your property.', 'Share what you are seeing on the ground. ECS can help assess the conditions and define a practical scope of work.', '../../contact/')}
'''


# -------------------------------------------------------------- accessibility
access_body = f'''
<section class="sec">
 {sec_head('the fine print —', 'Accessibility.', level=1)}
 <div class="svc-copy" style="max-width:60ch;margin-top:1rem">
  <p><strong>WCAG 2.2 Level AA is the ongoing accessibility target for this concept.</strong> We continue reviewing its structure, navigation, focus indicators, text contrast, responsive behavior, and controls as the site changes.</p>
  <p><strong>Last reviewed:</strong> August 5, 2026.</p>
  <p>Animations respect your system’s reduced-motion setting — with it enabled, drawing effects, parallax, and reveals are replaced with immediate content.</p>
  <p>Except for the business logo, page text is rendered as real text so it can be resized and adapted. Decorative illustrations are hidden from assistive technology; meaningful project photographs include descriptions.</p>
  <p>If something on this concept does not work well for you, call <a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a> or email <a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a>.</p>
 </div>
</section>
'''


datause_body = f'''
<section class="sec">
 {sec_head('the fine print —', 'Concept & Data Use.', level=1)}
 <div class="svc-copy" style="max-width:60ch;margin-top:1rem">
  <p><strong>{e(D.NOTICES[0])}</strong></p>
  <p>This site stores nothing. Its project worksheet runs only in the browser and opens the visitor’s own email app; it does not submit to or save data on this website. There are no analytics, cookies, payments, accounts, or uploads. Fonts are loaded from Google Fonts, which receives standard technical request data when the page loads.</p>
  <p>{e(D.NOTICES[1])} The landing page’s graphite drawings are generated concept art in a field-notes style, created to demonstrate a design direction. The project photographs on the service and about pages come from Environmental Construction Services’ own public website and were not altered beyond cropping and resizing.</p>
  <p>The concept is marked noindex/nofollow and its robots.txt asks crawlers to stay out.</p>
  <p>To reach the real business: <a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone_display'])}</a> or <a href="{D.FACTS['email_href']}">{e(D.FACTS['email_display'])}</a>.</p>
 </div>
</section>
'''


# --------------------------------------------------------------------- output
NAME = D.FACTS['name']
page(
    '',
    f'Drainage & Site Work in Moultrie, GA — {NAME} (Concept)',
    ('Private field-notes website concept for drainage, grading, excavation, '
     'clearing, culverts, driveways, hardscaping, and shoreline work in South Georgia.'),
    home,
    note='FIELD NOTE 01',
    current='',
    kind='home',
)
page(
    'drainage',
    f'Drainage Solutions in Moultrie, GA — {NAME} (Concept)',
    ('Residential and commercial drainage solutions including drain tile, French '
     'drains, grading, culverts, drain fields, lift stations, and maintenance.'),
    wrap(drainage_body),
    note='DRAINAGE FIELD NOTE',
    current='drainage/',
)
page(
    'services',
    f'Drainage, Excavation & Site Services in Moultrie, GA — {NAME} (Concept)',
    ('Drainage, excavation, forestry mulching, site preparation, culverts, driveways, '
     'hardscaping, landscaping, seawalls, retaining walls, and waterproofing.'),
    wrap(services_body),
    note='FIELD NOTE INDEX',
    current='services/',
)
page(
    'services/drainage',
    f'Drainage Solutions — {NAME} (Concept)',
    D.SERVICES[0]['blurb'],
    wrap(service_body(D.SERVICES[0])),
    note='FIELD NOTE 02',
    current='services/',
)
for service in D.SERVICES[1:]:
    page(
        f'services/{service["slug"]}',
        f'{service["label"]} — {NAME} (Concept)',
        service['blurb'],
        wrap(service_body(service)),
        note=service['note'],
        current='services/',
    )
page(
    'projects',
    f'Drainage & Site Work Projects in South Georgia — {NAME} (Concept)',
    ('Real ECS drainage, grading, site preparation, concrete, clearing, and landscape '
     'work from the field.'),
    wrap(projects_body),
    note='PROJECT FIELD LOG',
    current='projects/',
)
page(
    'about',
    f'About ECS in Moultrie, GA — {NAME} (Concept)',
    ('Meet Brandon Joins and the Moultrie family behind Environmental Construction '
     'Services, providing drainage, earthwork, and site construction across South Georgia.'),
    wrap(about_body),
    note='FIELD NOTE 08',
    current='about/',
)
page(
    'blog',
    f'Field Notes — Drainage & Site Work Resources — {NAME} (Concept)',
    ('Practical field notes about drainage, grading, land clearing, demolition, '
     'property care, and site planning in South Georgia.'),
    wrap(blog_body),
    note='FIELD LOG',
    current='blog/',
)
for index, post in enumerate(BLOG_POSTS, 1):
    canonical = f'{SITE_URL}/blog/{post["slug"]}/'
    social_image = f'{SITE_URL}/assets/{local_blog_asset(post["cover"])}'
    blog_posting = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': post['title'],
        'description': post['description'],
        'datePublished': post['date'],
        'dateModified': post['date'],
        'image': social_image,
        'mainEntityOfPage': canonical,
        'author': {'@type': 'Organization', 'name': NAME},
        'publisher': {
            '@type': 'Organization',
            'name': NAME,
            'logo': {'@type': 'ImageObject', 'url': f'{SITE_URL}/assets/ecs-logo-plated.png'},
        },
    }
    page(
        f'blog/{post["slug"]}',
        f'{post["title"]} — {NAME} (Concept)',
        post['description'],
        wrap(post_page_body(post)),
        note=f'LOG {index:02d}',
        current='blog/',
        og_type='article',
        social_image=social_image,
        social_alt=post['coverAlt'],
        canonical=canonical,
        published_time=f'{post["date"]}T12:00:00Z',
        author=NAME,
        structured_data=blog_posting,
        head_extra=f'<meta property="article:section" content="{e(post["category"])}">',
    )
    page(
        f'post/{post["slug"]}',
        f'{post["title"]} — {NAME} (Concept)',
        post['description'],
        wrap(post_page_body(post)),
        note=f'LOG {index:02d}',
        current='blog/',
        og_type='article',
        social_image=social_image,
        social_alt=post['coverAlt'],
        canonical=canonical,
        published_time=f'{post["date"]}T12:00:00Z',
        author=NAME,
        structured_data=blog_posting,
        head_extra=f'<meta property="article:section" content="{e(post["category"])}">',
    )
page(
    'contact',
    f'Contact ECS in Moultrie, GA — {NAME} (Concept)',
    ('Contact Environmental Construction Services in Moultrie about drainage, grading, '
     'culverts, land clearing, driveways, hardscaping, or seawalls.'),
    wrap(contact_body),
    note='FIELD NOTE 09',
    current='contact/',
)
page(
    'accessibility',
    f'Accessibility — {NAME} (Concept)',
    'Accessibility commitments for this private concept.',
    wrap(access_body),
    note='APPENDIX A',
)
page(
    'concept-data-use',
    f'Concept & Data Use — {NAME} (Concept)',
    'What this private concept is, and what it does not collect.',
    wrap(datause_body),
    note='APPENDIX B',
)

(OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8', newline='\n')
print('wrote robots.txt')
print('done')
