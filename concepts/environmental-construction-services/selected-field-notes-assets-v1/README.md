# Environmental Construction Services — Field Notes Developer Handoff

This is the complete visual and factual handoff for the human-selected
**Field Notes** website direction. It is a private design package for
Environmental Construction Services, not an official website or permission to
publish.

Start with these files:

1. `DEVELOPER_AI_BRIEF.md` — ready-to-use build brief for the developer AI.
2. `concept/selected-field-notes-reference.png` — approved visual target.
3. `reference/asset-board.png` — the implementation-ready asset family.
4. `reference/implementation-data.json` — evidence-controlled copy, routes,
   contact actions, and omissions.
5. `reference/layout-spec.json` — layout, responsive, motion, and image-fit
   guidance.
6. `brand/design-tokens.css` — palette and implementation tokens.
7. `reference/implementation-blueprint.md` — component-by-component build
   direction.

Run `node reference/validate-package.mjs` before using or transferring the
package. The validator checks inventory coverage, hashes, file sizes,
signatures, dimensions where supported, path containment, and the unchanged
first-party logo hashes.

## What to match

Preserve the concept's unexpected field-book composition:

- warm weathered engineering paper;
- oversized condensed headline;
- graphite excavation, culvert, water, and terrain drawings;
- layered tracing-paper, drafting, and topographic marks;
- restrained survey-red annotations;
- tactile pinned service cards and a torn-paper service index; and
- the exact first-party ECS logo integrated directly into the paper field.

Do not implement the selected concept as one flattened background. Build the
layout, content, buttons, navigation, cards, and responsive behavior as native
HTML and CSS. Use the supplied raster art only for the illustrations and paper
texture. Utility marks are supplied as SVG and PNG.

## Required content corrections

The approved image is a visual target, not final factual copy.

- Change `EXPLORE THE WORK` to `EXPLORE SERVICES`. No approved ECS project
  gallery exists yet.
- Use `HOME`, `SERVICES`, `ABOUT`, and `CONTACT` in the primary navigation.
- Do not add `OUR PROCESS` or process-step copy until the owner confirms the
  actual workflow.
- Do not reproduce decorative coordinates or measurements as real project or
  location data.
- Use the verified six-category service list in
  `reference/implementation-data.json`.
- Keep the visible private-concept and illustrative-imagery notices.

## Brand assets

- `brand/ecs-logo-original.png` is a pixel-equivalent PNG decode of the
  first-party AVIF.
- `brand/ecs-logo-as-served.avif` is the byte-for-byte file served by the
  business-controlled website.
- `brand/logo-placement-reference.png` shows the selected placement only.
- `brand/palette.svg`, `brand/palette.png`, and
  `brand/design-tokens.css` define the concept palette.

Do not redraw, generatively approximate, trace, crop, recolor, distort, filter,
or materially alter the logo. Scale it proportionally and request an
owner-supplied vector or higher-resolution master before production.

## Illustration assets

### Hero

- `illustrations/hero-excavation-collage-master.png` — lossless desktop master.
- `illustrations/hero-excavation-collage.webp` — delivery format.
- `illustrations/hero-excavation-collage-mobile-master.png` — separately
  composed portrait master; use it instead of shrinking the desktop scene.
- `illustrations/hero-excavation-collage-mobile.webp` — mobile delivery format.

### Six-service field atlas

`illustrations/service-sketch-atlas-master.png` contains six coordinated
drawings. Each is also provided as standalone PNG and WebP:

- `service-drainage`
- `service-land-clearing-excavation`
- `service-landscaping-hardscaping`
- `service-seawalls-retention-waterproofing`
- `service-site-prep-culverts`
- `service-driveways`

The three `pinned-*-reference.png` files are exact crops from the selected
concept. They are placement references; build card labels and links natively.

All excavation, culvert, water, driveway, hardscape, clearing, seawall, and
terrain imagery is generated and illustrative. It is not a photograph of ECS
equipment, staff, property, or completed work. Decorative instances should
normally use empty alt text or `aria-hidden="true"`.

## Texture and utility assets

The `textures/` directory includes:

- procedural paper grain;
- a concept-derived paper sample;
- survey grid and topographic line overlays;
- torn-paper edge;
- brass pin; and
- survey-red arrow.

Every utility asset is supplied as SVG and PNG. Prefer SVG for crisp,
responsive decoration. Keep utility graphics out of the accessibility tree.

## Homepage architecture

1. Accessible header with exact logo, native business name, and navigation.
2. Hero with `START WITH THE GROUND.`, verified-category summary,
   `EXPLORE SERVICES`, and `CALL (229) 516-0821`.
3. Three pinned pathways:
   - Drainage
   - Land Clearing & Excavation
   - Site Preparation, Culverts & Driveways
4. Torn-paper six-service index.
5. Six-service field atlas.
6. Minimal About section using only the verified family-owned-and-operated
   statement.
7. Direct-contact band with phone, email, and address.
8. Footer with private-concept and illustrative-imagery notices.

Do not build a project gallery until owner-controlled photography and accurate
captions are approved.

## Responsive and motion direction

- Below 900 px, stack copy above the mobile hero artwork.
- Use the portrait hero asset at mobile breakpoints.
- Reduce the wide left ledger to a thin red rule on small screens.
- Convert the pinned rail to a vertical stack or keyboard-accessible horizontal
  snap list.
- Use a two-column service index, then one column below 480 px.
- Keep every interactive target at least 44 by 44 CSS pixels.
- Prevent horizontal overflow at 320 px.

Motion should feel like a field drawing coming together:

- short ink-mask headline reveal;
- survey-red underline and arrow draw;
- 8–16 px drafting-layer settle;
- subtle paper lift and half-degree rotation on card hover; and
- very light, bounded parallax between paper, contour, and hero-art layers.

With `prefers-reduced-motion`, remove drawing animation, parallax, page wipes,
and spring effects. Use immediate or short opacity changes only.

## Accessibility

- Include a skip link and semantic landmarks.
- Use one H1 and a logical heading hierarchy.
- Make the mobile menu keyboard operable and preserve visible focus.
- Keep logo alt text empty when adjacent native text names the business.
- Treat technical marks, pins, paper scraps, and illustrative equipment as
  decorative.
- Reserve `#C6372D` for decoration or large text. Use the darker
  `--ecs-survey-red-text` token for normal-size text on paper.
- Do not encode essential meaning only through texture, color, or animation.

## Preview and data boundaries

- Add `noindex, nofollow` and a restrictive `robots.txt`.
- Display: `Private website concept — not the official Environmental
  Construction Services website.`
- Display: `Illustrative concept imagery — not photographs of completed ECS
  projects.`
- Do not add a live form, quote intake, upload, payment, account, analytics,
  cookies, or external data submission.
- Direct `tel:` and `mailto:` links are permitted with the verified values in
  `reference/implementation-data.json`.
- No public deployment, DNS change, indexing, outreach, or business
  impersonation is authorized by this package.
