"""Emit all Three Crazy Bakers pages from shared chrome + data.py.

Run: python build.py   (from this directory; writes ../*.html)
Filenames mirror the original site's paths for a 1:1 launch redirect map
(hard rule 2): menu, breakfast, dinner-specials, dinner-casseroles, catering,
pics, directions, privacy-policy.
"""
import html as H
from pathlib import Path
import data as D

OUT = Path(__file__).resolve().parents[1]
e = lambda s: H.escape(str(s), quote=True)

FONTS = ('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&'
         'family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&'
         'family=Barlow+Condensed:wght@400;500;600&display=swap')

NAV = [('index.html', 'HOME'), ('menu.html', 'MENU'), ('dinner-casseroles.html', 'TAKE & BAKE'),
       ('catering.html', 'CATERING'), ('index.html#story', 'OUR STORY'), ('directions.html', 'VISIT')]

RAIL = [('menu.html#bakery', 'BAKERY'), ('menu.html', 'LUNCH'), ('dinner-specials.html', 'DINNER'),
        ('dinner-casseroles.html', 'CASSEROLES'), ('catering.html', 'CATERING')]

DIA = '<span class="dia">&#9670;</span>'

def page(fname, title, desc, body, current=''):
    nav = ''.join(
        f'<a href="{href}"{" class=\"current\"" if href == current else ""}>{label}</a>'
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
<meta property="og:image" content="assets/three-crazy-bakers-og.png">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="mast">
  <div class="mast-in">
    <a class="logo" href="index.html"><img src="assets/three-crazy-bakers-logo-white.png" alt="Three Crazy Bakers"></a>
    <button class="nav-toggle" aria-expanded="false" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="primary">
      {nav}
      <a class="order-btn" href="{D.FACTS['order_url']}" target="_blank" rel="noopener">ORDER NOW</a>
    </nav>
  </div>
</header>
<main>
{body}
</main>
<footer>
  <div class="foot-in">
    <div>
      <img class="flogo" src="assets/three-crazy-bakers-logo-white.png" alt="">
      <p style="max-width:34ch;font-size:.92rem">On the Square in historic Moultrie since {D.FACTS['est']}. Bakery treats, lunch, dinner, take-home casseroles and catering.</p>
    </div>
    <div>
      <h4>FIND US</h4>
      <ul>
        <li>{e(D.FACTS['address_short'])}</li>
        <li><a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone'])}</a></li>
        <li>Mon&ndash;Sat 10am&ndash;9pm</li>
        <li>Sun 11am&ndash;8pm</li>
      </ul>
    </div>
    <div>
      <h4>EXPLORE</h4>
      <ul>
        <li><a href="menu.html">Lunch Menu</a></li>
        <li><a href="dinner-specials.html">Dinner Menu</a></li>
        <li><a href="breakfast.html">Breakfast</a></li>
        <li><a href="dinner-casseroles.html">Take &amp; Bake Casseroles</a></li>
        <li><a href="catering.html">Catering</a></li>
        <li><a href="pics.html">Gallery</a></li>
        <li><a href="privacy-policy.html">Privacy Policy</a></li>
      </ul>
    </div>
  </div>
  <div class="foot-note">Website concept &middot; prepared for Three Crazy Bakers &middot; not the official site</div>
</footer>
<script src="assets/main.js"></script>
</body>
</html>
"""
    (OUT / fname).write_text(doc, encoding='utf-8', newline='\n')
    print('wrote', fname)

def menu_items(items):
    out = []
    for it in items:
        name, price, desc = (it + ('',))[:3] if len(it) == 3 else (it[0], it[1], '')
        out.append(
            f'<div class="mi"><div class="row"><h3>{e(name)}</h3><span class="dots"></span>'
            f'<span class="price">{e(price)}</span></div>'
            + (f'<p>{e(desc)}</p>' if desc else '') + '</div>')
    return '\n'.join(out)

def sec_head(txt):
    return (f'<div class="menu-sec-head"><h2>{e(txt)}</h2>'
            f'<div class="rulewrap"><span>&#9670;</span></div></div>')

def rail_html():
    cells = ''.join(f'<a class="cell" href="{href}">{DIA}{label}</a>' for href, label in RAIL)
    return f"""<div class="rail"><div class="rail-in">
  <div class="art"><img src="assets/heritage-streetscape-left-alpha.png" alt=""></div>
  {cells}
  <div class="art"><img src="assets/heritage-building-right-alpha.png" alt=""></div>
</div></div>"""

divider = '<div class="divider"><img src="assets/heritage-divider.svg" alt=""></div>'

# --------------------------------------------------------------------- home
home = f"""
<section class="hero">
  <div class="hero-copy">
    <h1><span class="l1">ON THE SQUARE.</span><span class="l2">AT THE TABLE.</span></h1>
    <p class="sub">Bakery treats, lunch, dinner, and<br>take-home casseroles in historic Moultrie.</p>
    <div class="btn-row">
      <a class="btn fill" href="menu.html">VIEW THE MENU</a>
      <a class="btn line" href="directions.html">PLAN A VISIT</a>
    </div>
    <img class="hero-pencil" src="assets/courthouse-pencil-alpha.png" alt="">
  </div>
  <div class="hero-photo"><img src="assets/hero-menu-spread.webp" alt="Illustrative restaurant menu spread"></div>
</section>
{rail_html()}
<section class="band2">
  <div class="panel-navy">
    <h2>MENU INDEX</h2>
    <hr class="ded">
    <ul class="index-links">
      <li><a href="breakfast.html">BREAKFAST</a></li>
      <li><a href="menu.html">LUNCH &mdash; SERVED ALL DAY</a></li>
      <li><a href="dinner-specials.html">DINNER OPTIONS</a></li>
      <li><a href="menu.html#bakery">BAKERY CASE</a></li>
      <li><a href="dinner-casseroles.html">TAKE &amp; BAKE CASSEROLES</a></li>
      <li><a href="catering.html">CATERING</a></li>
    </ul>
  </div>
  <div class="panel-paper">
    <img class="pencil-l" src="assets/courthouse-band-alpha.png" alt="">
    <div class="pencil-body">
      <h2>DOWNTOWN<br>LOCATION</h2>
      <div class="loc-copy">
        <p class="addr">{e(D.FACTS['address_short'])}</p>
        <p>On the Square in historic Moultrie &mdash; a block from the Colquitt County courthouse. Open seven days a week.</p>
        <p><a class="go" style="font-family:var(--label);font-weight:600;font-size:14px;letter-spacing:.22em;color:var(--tomato);text-decoration:none" href="directions.html">DIRECTIONS &rarr;</a></p>
      </div>
    </div>
    <img class="pencil-r" src="assets/tree-band-alpha.png" alt="">
  </div>
</section>
<section class="sec" id="story">
  <div class="wrap">
    <div class="story-grid">
      <div>
        <p class="eyebrow">Our Story &middot; Est. {D.FACTS['est']}</p>
        <h2 class="display">Three crazy people<br>wanted a bakery.</h2>
        <blockquote>&ldquo;{e(D.FACTS['origin'])}&rdquo;</blockquote>
        <p>{e(D.FACTS['founders'])} opened the bakery in {D.FACTS['est']} on the corner of South Main Street and First Avenue &mdash; and it has been there ever since. What started with cinnamon rolls and pies grew into a full-service restaurant serving lunch and dinner seven days a week.</p>
        <p>Today, owners {e(D.FACTS['owners'])} carry the tradition forward with the same scratch-made baking that started it all. {e(D.FACTS['closing_line'])}</p>
      </div>
      <div class="photo"><img src="assets/storefront-sign.jpg" alt="The Three Crazy Bakers storefront sign on the Square in Moultrie"></div>
    </div>
  </div>
</section>
{divider}
<section class="sec" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">What we&rsquo;re known for</p>
    <h2 class="display" style="margin-bottom:2rem">From the case, the kitchen, and the oven.</h2>
    <div class="tiles">
      <div class="tile"><div class="ph"><img src="assets/bakery-cake.jpg" alt="A layer cake from the bakery case"></div>
        <div class="tx"><h3>The Bakery Case</h3><p>Cinnamon rolls, brownies, lemon squares and key lime pie &mdash; baked from scratch every day.</p><a class="go" href="menu.html#bakery">SEE BAKERY FAVORITES</a></div></div>
      <div class="tile"><div class="ph"><img src="assets/quiche-plate.jpg" alt="Quiche plate with fresh fruit"></div>
        <div class="tx"><h3>Lunch &amp; Dinner</h3><p>Famous roll-ups, burgers, salads and quiche all day &mdash; steaks, seafood pasta and shrimp &amp; grits at supper.</p><a class="go" href="menu.html">VIEW THE MENUS</a></div></div>
      <div class="tile"><div class="ph"><img src="assets/food-2015-b.jpg" alt="A take-and-bake casserole"></div>
        <div class="tx"><h3>Take &amp; Bake</h3><p>Ten family-size casseroles made daily &mdash; order by 2pm, pick up by 3pm, dinner solved.</p><a class="go" href="dinner-casseroles.html">SEE THIS WEEK&rsquo;S CASSEROLES</a></div></div>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------- menu
menu = f"""
<div class="page-head">
  <p class="eyebrow">Served all day</p>
  <h1>Lunch Options</h1>
  <p class="lede">Our famous roll-ups, burgers &amp; sandwiches, salads, quiche and soups &mdash; served all day, dine in or to-go.</p>
  <p class="menu-note">{e(D.ROLLUPS_NOTE)}</p>
</div>
<section class="sec" style="padding-top:1.5rem">
  <div class="wrap">
    {sec_head('Roll Ups')}
    <div class="menu-cols">{menu_items(D.ROLLUPS)}</div>
    {sec_head('Burgers & Sandwiches')}
    <div class="menu-cols">{menu_items(D.BURGERS)}</div>
    {sec_head('Salads')}
    <div class="menu-cols">{menu_items(D.SALADS)}</div>
    <p class="menu-note">{e(D.DRESSINGS)}</p>
    {sec_head('Quiche')}
    <p class="menu-note">{e(D.QUICHE['varieties'])}</p>
    <div class="menu-cols">{menu_items(D.QUICHE['items'])}</div>
    {sec_head('Soup')}
    <div class="menu-cols">{menu_items([(n, p, '') for n, p in D.SOUP])}</div>
    {sec_head('A La Carte')}
    <div class="menu-cols">{menu_items([(n, p, '') for n, p in D.A_LA_CARTE])}</div>
    <p class="menu-note">{e(D.LITTLE_BAKERS)}</p>
    <div id="bakery"></div>
    {sec_head('The Bakery Case')}
    <p class="menu-note">Cinnamon rolls, sausage rolls, brownies, lemon squares, cookies, key lime pie and whole pies &mdash; fresh from the oven daily. Selection varies; call {e(D.FACTS['phone'])} for today&rsquo;s case.</p>
    <p class="fineprint">{e(D.PRICE_NOTE)}</p>
    <p class="fineprint">{e(D.DISCLAIMER)}</p>
  </div>
</section>
"""

breakfast = f"""
<div class="page-head">
  <p class="eyebrow">Morning</p>
  <h1>Breakfast</h1>
  <p class="lede">Quiche plates, sausage &amp; cheese rolls, and the cinnamon rolls that started it all.</p>
</div>
<section class="sec" style="padding-top:1.5rem">
  <div class="wrap">
    {sec_head('Breakfast Plates & Pastries')}
    <div class="menu-cols">{menu_items(D.BREAKFAST['items'])}</div>
    {sec_head('Beverages')}
    <div class="menu-cols">{menu_items([(n, p, '') for n, p in D.BREAKFAST['beverages']])}</div>
    <p class="fineprint">{e(D.PRICE_NOTE)}</p>
  </div>
</section>
"""

dinner = f"""
<div class="page-head">
  <p class="eyebrow">Evenings</p>
  <h1>Dinner Options</h1>
  <p class="lede">{e(D.DINNER['entree_note'])}</p>
</div>
<section class="sec" style="padding-top:1.5rem">
  <div class="wrap">
    {sec_head('Starters')}
    <div class="menu-cols">{menu_items(D.DINNER['starters'])}</div>
    {sec_head('Entrées')}
    <div class="menu-cols">{menu_items(D.DINNER['entrees'])}</div>
    <p class="fineprint">{e(D.PRICE_NOTE)}</p>
    <p class="fineprint">{e(D.DISCLAIMER)}</p>
  </div>
</section>
"""

casseroles = f"""
<div class="page-head">
  <p class="eyebrow">Take &amp; Bake</p>
  <h1>Dinner Casseroles</h1>
  <p class="lede">{e(D.CASSEROLES['note'])} Call {e(D.FACTS['phone'])} to confirm today&rsquo;s availability.</p>
</div>
<section class="sec" style="padding-top:1.5rem">
  <div class="wrap">
    {sec_head('The Casseroles')}
    <div class="menu-cols">{menu_items([(n, '', d) for n, d in D.CASSEROLES['items']])}</div>
    <p class="fineprint">{e(D.PRICE_NOTE)}</p>
  </div>
</section>
"""

catering = f"""
<div class="page-head">
  <p class="eyebrow">Let us bring the table to you</p>
  <h1>Catering</h1>
  <p class="lede">{e(D.CATERING['intro'])} Call {e(D.FACTS['phone'])} to plan your order.</p>
</div>
<section class="sec" style="padding-top:1.5rem">
  <div class="wrap">
    {sec_head('Breakfast')}
    <div class="menu-cols">{menu_items([(x, '', '') for x in D.CATERING['breakfast']])}</div>
    {sec_head('Lunch & Dinner')}
    <div class="menu-cols">{menu_items([(x, '', '') for x in D.CATERING['lunch_dinner']])}</div>
    <p class="fineprint">{e(D.PRICE_NOTE)}</p>
  </div>
</section>
"""

gal_imgs = (['gallery-main.jpg', 'gallery-dining.jpg', 'gallery-counter.jpg', 'gallery-street.jpg',
             'food-2015-a.jpg', 'food-2015-c.jpg', 'quiche-plate.jpg', 'bakery-cake.jpg']
            + [f'gallery-{i:02d}.jpg' for i in range(1, 16)])
pics = f"""
<div class="page-head">
  <p class="eyebrow">From our kitchen &amp; dining room</p>
  <h1>Gallery</h1>
  <p class="lede">A few snapshots from over the years on the Square.</p>
</div>
<section class="sec" style="padding-top:1.8rem">
  <div class="wrap">
    <div class="gal">
      {''.join(f'<figure><img src="assets/{f}" alt="Three Crazy Bakers — from our kitchen and dining room" loading="lazy"></figure>' for f in gal_imgs)}
    </div>
  </div>
</section>
"""

MAPS_Q = 'https://www.google.com/maps?q=Three+Crazy+Bakers,+102+S+Main+St,+Moultrie,+GA+31768'
directions = f"""
<div class="page-head">
  <p class="eyebrow">Plan a visit</p>
  <h1>Find Us on the Square</h1>
  <p class="lede">{e(D.FACTS['address'])} &mdash; on the Square in historic downtown Moultrie.</p>
</div>
<section class="sec" style="padding-top:1.8rem">
  <div class="wrap">
    <div class="visit-grid">
      <div>
        <div class="map-frame">
          <iframe title="Map to Three Crazy Bakers" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            src="https://www.google.com/maps?q=102+S+Main+St,+Moultrie,+GA+31768&output=embed"></iframe>
        </div>
        <p class="city-links">An easy drive from Adel, Albany, Camilla, Sylvester, Thomasville, Tifton and Quitman &mdash;
          <a href="{MAPS_Q}" target="_blank" rel="noopener" style="color:var(--tomato)">open in Google Maps</a>.</p>
      </div>
      <div>
        <div class="hours-card">
          <h3>Hours</h3>
          <table>
            {''.join(f'<tr><td>{e(d)}</td><td>{e(h)}</td></tr>' for d, h in D.FACTS['hours'])}
            <tr><td>Phone</td><td><a href="{D.FACTS['phone_href']}" style="color:inherit">{e(D.FACTS['phone'])}</a></td></tr>
          </table>
        </div>
        <div style="margin-top:1.4rem"><img src="assets/storefront-sign-1200.jpg" alt="Three Crazy Bakers storefront on the Square" style="border:1.5px solid var(--rule);border-radius:3px"></div>
      </div>
    </div>
  </div>
</section>
"""

privacy = f"""
<div class="page-head">
  <p class="eyebrow">The fine print</p>
  <h1>Privacy Policy</h1>
</div>
<section class="sec" style="padding-top:1.5rem">
  <div class="wrap" style="max-width:52rem">
    <p>This website does not collect personal information, set marketing cookies, or run analytics that identify you. Fonts are served by Google Fonts and the map on our directions page is embedded from Google Maps; those services may receive standard technical request data (like your IP address) when the page loads.</p>
    <p style="margin-top:1rem">Online ordering is handled by our ordering partner on their own site and under their own privacy policy.</p>
    <p style="margin-top:1rem">Questions? Call us at <a href="{D.FACTS['phone_href']}">{e(D.FACTS['phone'])}</a> or visit us at {e(D.FACTS['address'])}.</p>
  </div>
</section>
"""

page('index.html', 'Three Crazy Bakers — On the Square in Moultrie, GA', 'Bakery treats, lunch, dinner, and take-home casseroles on the Square in historic Moultrie, Georgia. Est. 1998.', home, current='index.html')
page('menu.html', 'Lunch Menu — Three Crazy Bakers, Moultrie GA', 'Roll-ups, burgers, salads, quiche and soups — served all day at Three Crazy Bakers in Moultrie.', menu, current='menu.html')
page('breakfast.html', 'Breakfast — Three Crazy Bakers, Moultrie GA', 'Quiche plates, sausage rolls and cinnamon rolls at Three Crazy Bakers in Moultrie.', breakfast)
page('dinner-specials.html', 'Dinner Menu — Three Crazy Bakers, Moultrie GA', 'Steaks, seafood pasta, shrimp & grits and more — dinner at Three Crazy Bakers in Moultrie.', dinner)
page('dinner-casseroles.html', 'Take & Bake Casseroles — Three Crazy Bakers', 'Family-size take-and-bake dinner casseroles made daily at Three Crazy Bakers in Moultrie.', casseroles, current='dinner-casseroles.html')
page('catering.html', 'Catering — Three Crazy Bakers, Moultrie GA', 'Breakfast, lunch and dinner catering for business events in Moultrie from Three Crazy Bakers.', catering, current='catering.html')
page('pics.html', 'Gallery — Three Crazy Bakers, Moultrie GA', 'Photos from Three Crazy Bakers on the Square in Moultrie.', pics)
page('directions.html', 'Directions & Hours — Three Crazy Bakers, Moultrie GA', 'Find Three Crazy Bakers at 102 S Main St on the Square in Moultrie, GA. Hours and directions.', directions, current='directions.html')
page('privacy-policy.html', 'Privacy Policy — Three Crazy Bakers', 'Privacy policy for the Three Crazy Bakers website.', privacy)
print('done')
