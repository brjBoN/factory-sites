# Field Notes Implementation Blueprint

## Native interface versus supplied imagery

Build natively:

- navigation, headings, body copy, buttons, links, notices, and service labels;
- paper cards, borders, underlines, focus states, active states, and torn layout;
- responsive grids and the accessible mobile menu; and
- animation timelines with a reduced-motion fallback.

Use supplied imagery for:

- the unchanged first-party logo;
- desktop and mobile excavation/culvert hero collages;
- the six graphite service illustrations;
- paper texture; and
- small decorative topographic, grid, pin, arrow, and torn-edge utilities.

Never use the selected full-page concept as a responsive background.

## Component order

### Header

- Exact logo plus native-text business name.
- Handwritten `Moultrie, Georgia` annotation may be decorative.
- Navigation: Home, Services, About, Contact.
- Omit the decorative coordinates and `Our Process`.

### Hero

- H1: `Start with the ground.`
- Supporting copy restricted to verified service categories.
- Primary action: `Explore Services`.
- Secondary action: `Call (229) 516-0821`.
- Right-hand desktop collage; portrait collage below the actions on mobile.

### Pinned pathways

- Drainage.
- Land Clearing & Excavation.
- Site Preparation, Culverts & Driveways.

Use the pins, shadows, and small rotations as decoration. The whole card should
be a semantic link with a visible focus state.

### Service atlas

Build six linked entries using the standalone service art and native labels.
Do not imply that an illustration is a completed ECS project.

### About

The only pre-approved company-description fact is `Family-owned and
operated.` Do not invent founding year, team, biography, experience, values,
credentials, or equipment.

### Contact

Use direct phone and email links plus the corroborated address. Do not add a
form, chatbot, quote intake, scheduling widget, or file upload.

### Footer

Include the private-concept, illustrative-imagery, and no-data-collection
notices. Keep `noindex, nofollow` and block crawling for a hosted private
preview.

## Motion choreography

1. Reveal the paper field immediately.
2. Bring in the logo and location annotation with a short opacity transition.
3. Reveal the two-line headline with a restrained ink mask.
4. Draw the survey-red underline over roughly 420 ms.
5. Settle drafting and hero layers from 8–16 px offsets.
6. Let pinned cards lift 4–6 px and rotate no more than 0.5 degrees on hover.

Do not loop machinery motion, animate crude line-art strokes, scroll-jack, use
heavy particles, or delay access to navigation and content.

## Responsive composition

The mobile page should be recomposed, not proportionally shrunk:

1. Header and accessible menu.
2. Headline.
3. Verified-category copy.
4. Actions.
5. Portrait hero artwork.
6. Pinned pathways.
7. Service atlas.
8. About and contact.

Test at 320, 375, 390, 768, 900, 1024, 1280, and 1536 CSS pixels. Confirm
there is no horizontal overflow at any size.

## Visual QA target

- The logo is never distorted, filtered, clipped, or visually detached in a
  white card.
- The desktop hero preserves the full torn-paper boundary.
- The portrait hero is used on mobile and nothing important is clipped.
- The graphite illustrations retain paper padding; do not use `cover`.
- Survey red remains an accent, not a large background color.
- Body text remains high-contrast and easy to read over all texture.
- With animations disabled, every section is visible and usable.
