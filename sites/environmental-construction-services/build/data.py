"""ECS Field Notes — contract data, transcribed from the asset package's
reference/implementation-data.json. ONLY facts allowed by the package appear
on the site; copy restrictions are enforced here by simply not having the
restricted content available to the builder.
"""

FACTS = {
    'name': 'Environmental Construction Services',
    'name_llc': 'Environmental Construction Services LLC',
    'family': 'Family-owned and operated.',
    'address': '33 Pine Cone Road, Moultrie, GA',
    'phone_display': '(229) 516-0821',
    'phone_href': 'tel:+12295160821',
    'email_display': 'ecs.outdoorcustoms@gmail.com',
    'email_href': 'mailto:ecs.outdoorcustoms@gmail.com',
    'location_annotation': 'Moultrie, Georgia',
}

HEADLINE = 'Start with the ground.'

HERO_COPY = ('Drainage, land clearing and excavation, landscaping and hardscaping, '
             'seawalls and retention, site preparation, culverts, and driveways — '
             'the work that everything else is built on.')

NOTICES = [
    'Private website concept — not the official Environmental Construction Services website.',
    'Illustrative concept imagery — not photographs of completed ECS projects.',
    'This concept does not accept quote requests, inquiries, files, payments, or customer information.',
]

SERVICES = [
    {
        'slug': 'drainage',
        'label': 'Drainage',
        'asset': 'service-drainage.webp',
        'note': 'FIELD NOTE 02',
        'blurb': 'Standing water, washouts, and soggy ground all start as a drainage problem. This is the category of work that moves water where it belongs.',
    },
    {
        'slug': 'land-clearing-excavation',
        'label': 'Land Clearing & Excavation',
        'asset': 'service-land-clearing-excavation.webp',
        'note': 'FIELD NOTE 03',
        'blurb': 'Overgrowth out, grades cut, ground opened. Clearing and excavation take a site from raw to ready.',
    },
    {
        'slug': 'landscaping-hardscaping',
        'label': 'Landscaping & Hardscaping',
        'asset': 'service-landscaping-hardscaping.webp',
        'note': 'FIELD NOTE 04',
        'blurb': 'The finished layer — plantings, stonework, and the outdoor spaces people actually use.',
    },
    {
        'slug': 'seawalls-retention-waterproofing',
        'label': 'Seawalls, Retention & Waterproofing',
        'asset': 'service-seawalls-retention-waterproofing.webp',
        'note': 'FIELD NOTE 05',
        'blurb': 'Where land meets water, the edge has to hold. Seawalls, retention, and waterproofing are that edge.',
    },
    {
        'slug': 'site-prep-culverts',
        'label': 'Site Preparation & Culverts',
        'asset': 'service-site-prep-culverts.webp',
        'note': 'FIELD NOTE 06',
        'blurb': 'Before anything goes vertical, the pad, the pipe, and the path have to be right.',
    },
    {
        'slug': 'driveways',
        'label': 'Driveways',
        'asset': 'service-driveways.webp',
        'note': 'FIELD NOTE 07',
        'blurb': 'The way in and the way home — built to take traffic and weather, season after season.',
    },
]

PINNED = [
    {'label': 'CONTROL WATER', 'aria': 'Explore drainage services',
     'href': 'services/drainage/', 'asset': 'service-drainage.webp'},
    {'label': 'CLEAR & PREP', 'aria': 'Explore land clearing, excavation, and site preparation services',
     'href': 'services/land-clearing-excavation/', 'asset': 'service-land-clearing-excavation.webp'},
    {'label': 'BUILD ACCESS', 'aria': 'Explore culvert and driveway services',
     'href': 'services/site-prep-culverts/', 'asset': 'service-driveways.webp'},
]
