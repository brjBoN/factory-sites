# Developer AI Brief — Build the ECS Field Notes Website

Implement a private, responsive, multi-page website concept for Environmental
Construction Services that matches
`concept/selected-field-notes-reference.png` as closely as practical while
remaining native, accessible, and responsive.

Before building, read:

1. `README.md`
2. `reference/implementation-data.json`
3. `reference/layout-spec.json`
4. `reference/implementation-blueprint.md`
5. `reference/provenance.md`
6. `reference/owner-asset-checklist.md`
7. `manifest.json`

Use `reference/asset-board.png` to understand the complete visual system.

## Non-negotiable implementation requirements

- Build all navigation, headings, copy, buttons, cards, links, service labels,
  notices, and responsive layout as native HTML and CSS.
- Do not use the full selected-concept PNG as a page background.
- Use the exact separate logo in `brand/ecs-logo-original.png`; never redraw,
  approximate, trace, crop, recolor, filter, distort, or materially alter it.
- Use the supplied desktop and mobile hero assets at their appropriate
  breakpoints.
- Use the six standalone service illustrations for the service architecture.
- Change the visual reference's `EXPLORE THE WORK` button to
  `EXPLORE SERVICES`.
- Primary navigation is `HOME`, `SERVICES`, `ABOUT`, and `CONTACT`.
- Do not build `OUR PROCESS`, process steps, or a project gallery until the
  owner supplies and confirms the missing information and assets.
- Implement every route listed in `reference/implementation-data.json`, using
  only the allowed facts and service-category wording in that file.
- Show the private-concept, illustrative-imagery, and no-data-collection
  notices.
- Add `noindex, nofollow` and a disallow-all `robots.txt`.
- Do not add a live form, quote intake, chatbot, upload, scheduling,
  reservation, payment, account, analytics, cookies, or customer-data
  collection.
- Do not deploy publicly or contact the business.

## Visual target

The result should feel like a tactile civil-engineering field notebook:
weathered cream paper, graphite drawings, drafting grids, contour marks,
tracing-paper collage, brass pins, torn edges, oversized condensed typography,
and sparse survey-red annotation. It should not resemble a generic contractor
template.

Use restrained motion:

- ink-mask headline reveal;
- survey-red line draw;
- subtle 8–16 px drafting-layer settle;
- gentle paper-card lift and no more than 0.5 degrees of rotation; and
- very light, bounded parallax.

Honor `prefers-reduced-motion` by removing drawing animations, parallax,
spring effects, and page wipes.

## Required quality checks

- Production build, lint, and type-check pass.
- Every route renders without console errors or broken links.
- Keyboard navigation, mobile menu, focus states, skip link, landmarks, and
  heading hierarchy pass.
- Automated accessibility scan returns no serious or critical issue.
- No horizontal overflow at 320, 375, 390, 768, 900, 1024, 1280, and 1536 CSS
  pixels.
- The logo is proportional and unclipped.
- Desktop and portrait hero art are never clipped with `cover`.
- All generated art is described as illustrative, not completed ECS work.
- No unsupported fact from the restriction list appears.
- The private concept remains unindexed, non-collecting, and undeployed.

Run `node reference/validate-package.mjs` before starting so asset integrity is
known-good.
