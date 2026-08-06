"""Verified ECS drainage content used by the field-notes static generator.

The page builder deliberately keeps the private-concept notices separate from
the business copy. Service language, contact details, project captions, and
client feedback below are drawn from the reviewed ECS drainage site.
"""

FACTS = {
    'name': 'Environmental Construction Services',
    'name_llc': 'Environmental Construction Services LLC',
    'family': 'Family-owned and operated in Moultrie, Georgia.',
    'address_street': '33 Pine Cone Road',
    'address': '33 Pine Cone Road, Moultrie, GA 31768',
    'map_href': 'https://maps.google.com/?q=33+Pine+Cone+Road+Moultrie+GA+31768',
    'phone_display': '(229) 516-0821',
    'phone_href': 'tel:+12295160821',
    'email_display': 'ecs.outdoorcustoms@gmail.com',
    'email_href': 'mailto:ecs.outdoorcustoms@gmail.com',
    'facebook_href': 'https://www.facebook.com/Environmentalcs/',
    'instagram_href': 'https://www.instagram.com/environmentalcs/',
    'location_annotation': 'Moultrie, Georgia',
    # Decorative survey coordinates retained from the approved blueprint
    # wrapper. They identify Moultrie, not the business parcel.
    'location_coords': '31° 11′ 45″ N  83° 46′ 21″ W',
}

NOTICES = [
    'Private website concept — not the official Environmental Construction Services website.',
    'Landing-page illustrations are concept art; project photographs are Environmental '
    'Construction Services’ own, from their public website and posts.',
    ('This concept does not transmit or store quote requests, inquiries, files, payments, '
     'or customer information; its project worksheet opens the visitor’s own email app.'),
]

HERO = {
    'lines': ('Drainage &', 'site work for', 'South Georgia.'),
    'lede': ('ECS handles drainage, grading, excavation, culverts, clearing, driveways, '
             'hardscaping, and shoreline work for residential and commercial properties.'),
    'cta': 'Explore ECS services',
}

# Copy retained from the first blueprint concept. It is shown below the new
# drainage-first material so the change in emphasis does not erase information.
ORIGINAL_HOME = {
    'headline': 'Start with the ground.',
    'copy': 'Drainage, clearing, excavation, site preparation, and outdoor construction.',
    'cta': 'Explore the Work',
    'cards': ('CONTROL WATER', 'CLEAR & PREP', 'BUILD ACCESS'),
    'eyebrow': 'the whole kit —',
    'title': 'Six kinds of groundwork.',
    'about_eyebrow': 'who we are —',
    'about_title': 'Family-owned. Moultrie ground.',
    'about_copy': ('Family-owned and operated. Based at 33 Pine Cone Road, Moultrie, GA. '
                   'The fastest way to talk through a site is a phone call.'),
    'consultation': ('Every property drains, grades, and wears differently. Call or write '
                     'and tell us what the ground is doing — we’ll take it from there.'),
}

PINNED = [
    {'label': 'CONTROL WATER', 'aria': 'CONTROL WATER — explore ECS drainage solutions',
     'href': 'drainage/', 'asset': 'mobile-card-1.png'},
    {'label': 'CLEAR & PREP', 'aria': 'CLEAR & PREP — explore land clearing and excavation',
     'href': 'services/land-clearing-excavation/', 'asset': 'mobile-card-2.png'},
    {'label': 'BUILD ACCESS', 'aria': 'BUILD ACCESS — explore site preparation and culvert work',
     'href': 'services/site-prep-culverts/', 'asset': 'mobile-card-3.png'},
]

SERVICES = [
    {
        'slug': 'drainage',
        'rail_label': 'Drainage',
        'label': 'Drainage',
        'eyebrow': 'Drainage specialty',
        'title': 'Drainage solutions for the whole property.',
        'asset': 'photo-drainage.jpg',
        'alt': 'ECS excavator installing a subsurface drainage holding system in Moultrie',
        'note': 'FIELD NOTE 02',
        'blurb': ('ECS provides residential and commercial drainage work built around '
                  'collection, conveyance, grade, and a defined outlet. The goal is a '
                  'complete path, not a disconnected patch.'),
        'bullets': [
            'Drain tile and French drains',
            'Drain fields and septic systems',
            'Lift stations and maintenance',
            'Grading and culverts',
        ],
    },
    {
        'slug': 'land-clearing-excavation',
        'rail_label': 'Land Clearing',
        'label': 'Excavation & Forestry Mulching',
        'eyebrow': 'Land clearing & preparation',
        'title': 'Excavation & forestry mulching.',
        'asset': 'project-forestry-mulching.jpg',
        'alt': 'ECS excavator forestry mulching on a wooded project site',
        'note': 'FIELD NOTE 03',
        'blurb': ('ECS clears overgrowth, removes site obstacles, and uses excavation and '
                  'forestry mulching to prepare land for the work that follows.'),
        'bullets': [
            'Excavation & land leveling',
            'Forestry mulching',
            'Selective clearing & site preparation',
        ],
    },
    {
        'slug': 'landscaping-hardscaping',
        'rail_label': 'Hardscaping',
        'label': 'Landscaping, Patios & Hardscaping',
        'eyebrow': 'Outdoor construction',
        'title': 'Landscaping, patios & hardscaping.',
        'asset': 'project-paver-pool-deck.jpg',
        'alt': 'Completed ECS poolside paver patio and hardscape project',
        'note': 'FIELD NOTE 04',
        'blurb': ('Landscape installation and hardscape construction bring durable '
                  'structure and finished outdoor spaces together around the property.'),
        'bullets': [
            'Landscape installation',
            'Patios & walkways',
            'Hardscaping & retaining walls',
        ],
    },
    {
        'slug': 'seawalls-retention-waterproofing',
        'rail_label': 'Seawalls',
        'label': 'Seawalls, Retaining Walls & Waterproofing',
        'eyebrow': 'Shoreline & structural protection',
        'title': 'Seawalls, retaining walls & waterproofing.',
        'asset': 'photo-seawalls-retention-waterproofing.jpg',
        'alt': 'Completed shoreline seawall and retaining edge',
        'note': 'FIELD NOTE 05',
        'blurb': ('ECS builds seawall and retaining-wall solutions and provides '
                  'waterproofing services where water, soil, and structures meet.'),
        'bullets': ['Seawalls', 'Retaining walls', 'Waterproofing'],
    },
    {
        'slug': 'site-prep-culverts',
        'rail_label': 'Culverts',
        'label': 'Grading, Site Preparation & Culverts',
        'eyebrow': 'Site access & drainage',
        'title': 'Grading, site preparation & culverts.',
        'asset': 'project-ballfield-restoration.jpg',
        'alt': 'ECS grading and restoring a ballfield after drainage work',
        'note': 'FIELD NOTE 06',
        'blurb': ('Site preparation establishes the working surface and access a project '
                  'needs. Culvert installation helps carry water beneath driveways and '
                  'crossings as part of that larger site plan.'),
        'bullets': ['Site preparation', 'Culvert installation', 'Grading support'],
    },
    {
        'slug': 'driveways',
        'rail_label': 'Driveways',
        'label': 'Concrete, Paver & Gravel Driveways',
        'eyebrow': 'Driveway construction',
        'title': 'Concrete, paver & gravel driveways.',
        'asset': 'photo-driveways.jpg',
        'alt': 'Crew placing and finishing a new concrete driveway',
        'note': 'FIELD NOTE 07',
        'blurb': ('ECS installs concrete, paver, and gravel driveways, coordinating the '
                  'surface, grade, and drainage considerations around the finished approach.'),
        'bullets': ['Concrete driveways', 'Paver driveways', 'Gravel driveways'],
    },
]

ORIGINAL_SERVICE_NOTES = {
    'drainage': {
        'label': 'Drainage',
        'asset': 'photo-drainage.jpg',
        'alt': 'Excavator installing a buried drainage tank in a trench',
        'copy': ('Standing water, washouts, and soggy ground all start as a drainage '
                 'problem. This is the category of work that moves water where it belongs.'),
    },
    'land-clearing-excavation': {
        'label': 'Land Clearing & Excavation',
        'asset': 'photo-land-clearing-excavation.jpg',
        'alt': 'Excavator beside a cleared residential lot with a burn pile and soil mound',
        'copy': ('Overgrowth out, grades cut, ground opened. Clearing and excavation take '
                 'a site from raw to ready.'),
    },
    'landscaping-hardscaping': {
        'label': 'Landscaping & Hardscaping',
        'asset': 'photo-landscaping-hardscaping.jpg',
        'alt': 'New sod and concrete walkways around a playground',
        'copy': ('The finished layer — plantings, stonework, and the outdoor spaces people '
                 'actually use.'),
    },
    'seawalls-retention-waterproofing': {
        'label': 'Seawalls, Retention & Waterproofing',
        'asset': 'photo-seawalls-retention-waterproofing.jpg',
        'alt': 'Rock-lined bank along a wooded pond',
        'copy': ('Where land meets water, the edge has to hold. Seawalls, retention, and '
                 'waterproofing are that edge.'),
    },
    'site-prep-culverts': {
        'label': 'Site Preparation & Culverts',
        'asset': 'photo-site-prep-culverts.jpg',
        'alt': 'Excavator installing a buried drainage tank in a trench',
        'copy': ('Before anything goes vertical, the pad, the pipe, and the path have to '
                 'be right.'),
    },
    'driveways': {
        'label': 'Driveways',
        'asset': 'photo-driveways.jpg',
        'alt': 'Crew leveling freshly poured concrete for a driveway',
        'copy': ('The way in and the way home — built to take traffic and weather, season '
                 'after season.'),
    },
}

ORIGINAL_ABOUT = {
    'copy': ('Environmental Construction Services works the ground: drainage, land clearing '
             'and excavation, landscaping and hardscaping, seawalls and retention, site '
             'preparation, culverts, and driveways.'),
    'fit': ('Based at 33 Pine Cone Road, Moultrie, GA. The best way to find out whether '
            'we’re the right fit for your project is to call.'),
    'asset': 'photo-about-family.jpg',
    'alt': 'The family behind Environmental Construction Services',
}

HOME_SOLUTIONS = [
    {
        'number': '01',
        'title': 'Surface water collection',
        'copy': ('Grading, swales, inlets, catch basins, and trench drains collect '
                 'stormwater before it settles where it should not.'),
    },
    {
        'number': '02',
        'title': 'Underground conveyance',
        'copy': ('French drains, drain tile, solid pipe, and connected basins create a '
                 'dependable route away from problem areas.'),
    },
    {
        'number': '03',
        'title': 'Site grading & protection',
        'copy': ('Culverts, erosion control, site grading, and thoughtful discharge points '
                 'help the solution work with the property around it.'),
    },
]

DRAINAGE_PROBLEMS = [
    {
        'title': 'Standing water',
        'copy': ('Standing water after rain can point to a low area, restricted outlet, '
                 'or an incomplete route across the property.'),
    },
    {
        'title': 'Runoff near structures',
        'copy': ('Water collecting beside a home, building, driveway, or outdoor space '
                 'deserves a site-wide look before it causes more disruption.'),
    },
    {
        'title': 'Erosion and soft ground',
        'copy': ('Erosion, ruts, and persistently soft areas show where moving water and '
                 'soil are working against the site.'),
    },
]

DRAINAGE_ASSESSMENT = [
    {
        'number': '01',
        'title': 'Identify the source.',
        'copy': ('Note roof runoff, neighboring grade, paved areas, and other sources '
                 'feeding the wet area.'),
    },
    {
        'number': '02',
        'title': 'Evaluate the grade.',
        'copy': ('Check low points, drive crossings, structures, and existing drainage '
                 'components.'),
    },
    {
        'number': '03',
        'title': 'Plan the discharge.',
        'copy': ('Confirm where collected water can go so the system resolves the problem '
                 'responsibly.'),
    },
]

DRAINAGE_CAPABILITIES = [
    {
        'title': 'Collection',
        'copy': ('Identify where water enters and gathers, then shape a practical '
                 'collection point for the conditions on the property.'),
        'items': ['Drain fields', 'Surface grading', 'Connected collection areas'],
    },
    {
        'title': 'Conveyance',
        'copy': ('Create a dependable route that moves water away from the problem area '
                 'instead of shifting it a few feet away.'),
        'items': ['French drains', 'Drain tile', 'Culvert installation'],
    },
    {
        'title': 'System support & maintenance',
        'copy': ('Coordinate the drainage system with the rest of the site and keep '
                 'serviceable components working as intended.'),
        'items': ['Lift stations', 'Septic systems', 'Drainage maintenance'],
    },
]

DRAINAGE_PROCESS = [
    {
        'number': '01',
        'title': 'Site assessment',
        'copy': ('Start with the symptom, then trace the grade, inflow, low points, '
                 'crossings, and possible outlets around it.'),
    },
    {
        'number': '02',
        'title': 'System design',
        'copy': ('Match the route and drainage components to the property instead of '
                 'forcing a one-size-fits-all trench into the site.'),
    },
    {
        'number': '03',
        'title': 'Installation & site finish',
        'copy': ('Install the connected path, restore the work area, and give runoff '
                 'somewhere practical to go.'),
    },
]

DRAINAGE_FAQS = [
    (
        'What is the first step when I have standing water?',
        ('Start with a property assessment. Where the water appears is not always where '
         'the problem begins, so ECS looks at the surrounding grade, runoff path, and '
         'available outlet before recommending a solution.'),
    ),
    (
        'What types of drainage work does ECS handle?',
        ('ECS works with drain fields, drain tile, French drains, septic systems, lift '
         'stations, drainage maintenance, grading, and culvert installation. The right '
         'combination depends on the site.'),
    ),
    (
        'Do you work on residential and commercial properties?',
        ('Yes. Environmental Construction Services provides drainage work for both '
         'residential and commercial properties in Moultrie and surrounding South '
         'Georgia communities.'),
    ),
    (
        'Will grading alone solve my drainage problem?',
        ('Sometimes grading is part of the answer, but not every site can be corrected by '
         'reshaping the surface alone. Collection, underground conveyance, a culvert, or '
         'another outlet may also be needed.'),
    ),
    (
        'Can ECS maintain an existing drainage system?',
        ('Yes. Drainage maintenance is one of the services ECS offers. Call with what you '
         'are seeing and any details you have about the existing system.'),
    ),
]

PROJECTS = [
    {
        'number': '01', 'category': 'Drainage',
        'title': 'Below-grade drainage installation',
        'copy': ('Excavation, tank placement, and pipe routing underway as part of an ECS '
                 'water-management job.'),
        'asset': 'photo-drainage.jpg',
        'alt': 'Excavator setting grade beside a below-ground drainage tank and piping',
    },
    {
        'number': '02', 'category': 'Drainage',
        'title': 'Ballfield grading and restoration',
        'copy': ('ECS reshaped and restored this ballfield area after drainage work to '
                 'leave a smooth, usable finished grade.'),
        'asset': 'project-ballfield-restoration.jpg',
        'alt': 'Graded and restored ballfield area after ECS drainage work',
    },
    {
        'number': '03', 'category': 'Drainage',
        'title': 'Foundation drainage excavation',
        'copy': ('Careful excavation beside a home created access for foundation drainage '
                 'and the supporting site work.'),
        'asset': 'project-foundation-drainage.jpg',
        'alt': 'ECS excavator opening a foundation drainage trench beside a home',
    },
    {
        'number': '04', 'category': 'Driveways',
        'title': 'Concrete placement',
        'copy': ('An ECS crew placing, leveling, and shaping concrete during an active '
                 'driveway project.'),
        'asset': 'project-driveway-concrete.jpeg',
        'alt': 'Crew placing and leveling concrete for a driveway',
    },
    {
        'number': '05', 'category': 'Site work',
        'title': 'Demolition and clearing',
        'copy': ('An excavator removing an existing structure and opening the area for the '
                 'site work that follows.'),
        'asset': 'project-demolition.jpeg',
        'alt': 'Yellow ECS excavator removing an existing block structure',
    },
    {
        'number': '06', 'category': 'Earthwork',
        'title': 'Base material and grading',
        'copy': ('Fill material delivered for ground preparation, grade building, and the '
                 'next stage of construction.'),
        'asset': 'project-house-pad.jpg',
        'alt': 'Dump trailer delivering fill material at an ECS project site',
    },
    {
        'number': '07', 'category': 'Hardscaping',
        'title': 'Paver patio and fire pit',
        'copy': ('A completed paver gathering space with a built-in fire pit and a finished '
                 'retaining edge.'),
        'asset': 'project-paver-fire-pit.jpg',
        'alt': 'Completed ECS paver patio, fire pit, and retaining wall',
    },
    {
        'number': '08', 'category': 'Land clearing',
        'title': 'Forestry mulching and clearing',
        'copy': ('An ECS excavator opening overgrown ground and preparing the property for '
                 'the work that follows.'),
        'asset': 'project-forestry-mulching.jpg',
        'alt': 'ECS excavator forestry mulching on a wooded project site',
    },
]

TESTIMONIALS = [
    {
        'quote': ('Working with Environmental Construction Services was a fantastic experience. '
                  'Their attention to detail and commitment to environmental sustainability '
                  'truly sets them apart. I couldn’t be happier with the transformation they '
                  'brought to my outdoor space.'),
        'name': 'Whitney Smith',
    },
    {
        'quote': ('Brandon and his ECS team are extremely professional and reliable! They were '
                  'immediately responsive, communicated along the way, and did a fantastic job. '
                  'The customer service was wonderful. I’d highly recommend Brandon and his '
                  'Environmental Construction Services team!'),
        'name': 'Marcy Sullivan',
    },
    {
        'quote': ('Brandon is a professional and is very conscientious. Always comes when he '
                  'says and doesn’t leave until the job is done.'),
        'name': 'ECS client',
    },
]

MARCY_TESTIMONIAL = TESTIMONIALS[1]

ABOUT_FACTS = [
    ('Home base', 'Moultrie, Georgia'),
    ('Lead specialty', 'Drainage & water management'),
    ('Project types', 'Residential & commercial'),
    ('Approach', 'Clear communication & careful field work'),
]

CONTACT_SERVICE_TAGS = [
    'Drainage assessment',
    'Site preparation or grading',
    'Culvert installation',
    'Land clearing or excavation',
    'Driveway or patio',
    'Hardscaping or landscaping',
    'Seawall or retaining wall',
    'Something else',
]

CONTACT_TIMING_OPTIONS = [
    'I am gathering information',
    'As soon as practical',
    'Within the next month',
    'Within the next few months',
    'I have a specific date',
]
