import assert from "node:assert/strict";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const blogPosts = JSON.parse(readFileSync(path.join(root, "build", "blog-posts.json"), "utf8"));

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#x27;");
}

function formatDate(date) {
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${date}T12:00:00Z`));
}

function localBlogAsset(source) {
  const filename = path.basename(new URL(source, "https://example.invalid").pathname);
  return filename === "ecs-cleared-property.jpg" ? "project-cleared-property.jpg" : filename;
}

function walk(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    if ([".git", ".vercel", "build", "tests"].includes(entry.name)) return [];
    const target = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(target) : [target];
  });
}

const requiredRoutes = [
  "index.html",
  "drainage/index.html",
  "services/index.html",
  "projects/index.html",
  "about/index.html",
  "blog/index.html",
  "contact/index.html",
  "accessibility/index.html",
  "concept-data-use/index.html",
  ...blogPosts.flatMap(({ slug }) => [
    `blog/${slug}/index.html`,
    `post/${slug}/index.html`,
  ]),
];

for (const route of requiredRoutes) {
  assert.ok(existsSync(path.join(root, route)), `missing route: ${route}`);
}

assert.ok(
  existsSync(path.join(root, "assets", "ecs-drainage-field-notes-og.png")),
  "missing drainage-first social card",
);

const htmlFiles = walk(root).filter((file) => file.endsWith(".html"));
assert.equal(htmlFiles.length, 31, "unexpected generated-page count");

for (const file of htmlFiles) {
  const html = readFileSync(file, "utf8");
  const relativeFile = path.relative(root, file);

  assert.match(html, /<meta name="viewport"/i, `${relativeFile}: missing viewport metadata`);
  assert.match(html, /<meta name="robots" content="noindex, nofollow">/i, `${relativeFile}: preview must remain noindex`);
  assert.match(html, /<title>[^<]+<\/title>/i, `${relativeFile}: missing title`);
  assert.match(html, /class="skip-link"/i, `${relativeFile}: missing skip link`);
  assert.match(html, /"@type": "HomeAndConstructionBusiness"/, `${relativeFile}: missing business structured data`);

  const references = [...html.matchAll(/(?:href|src)="([^"]+)"/gi)].map((match) => match[1]);
  for (const reference of references) {
    if (
      !reference ||
      reference.startsWith("#") ||
      /^(?:https?:|mailto:|tel:|data:|javascript:|\/\/)/i.test(reference)
    ) {
      continue;
    }

    const clean = reference.split(/[?#]/, 1)[0];
    let target = path.resolve(path.dirname(file), clean);
    if (clean.endsWith("/") || (existsSync(target) && statSync(target).isDirectory())) {
      target = path.join(target, "index.html");
    }
    assert.ok(existsSync(target), `${relativeFile}: broken local reference ${reference}`);
  }
}

const contentChecks = new Map([
  ["index.html", ["Drainage &amp;", "site work for", "South Georgia.", "A better drainage plan starts with the whole property", "Start with the ground.", "Drainage, clearing, excavation, site preparation, and outdoor construction.", "Explore the Work", "CONTROL WATER", "CLEAR &amp; PREP", "BUILD ACCESS", "Six kinds of groundwork.", "Family-owned. Moultrie ground."]],
  ["drainage/index.html", ["Drainage solutions", "Find the cause before choosing the fix", "What is the first step when I have standing water?"]],
  ["services/index.html", ["One contractor", "Excavation &amp; Forestry Mulching", "Seawalls, Retaining Walls &amp; Waterproofing"]],
  ["projects/index.html", ["Drainage &amp; site work", "Below-grade drainage installation", "Forestry mulching and clearing"]],
  ["about/index.html", ["A local team", "Brandon Joins", "Understand the site", "Home base", "Drainage &amp; water management", "Whitney Smith", "Marcy Sullivan", "ECS client", "Environmental Construction Services works the ground", "Site conditions guide the work."]],
  ["contact/index.html", ["Tell us about your property", "(229) 516-0821", "ecs.outdoorcustoms@gmail.com", "Ownership", "Request a site consultation", "Prepare project request", "Something else", "I have a specific date"]],
]);

for (const [route, phrases] of contentChecks) {
  const html = readFileSync(path.join(root, route), "utf8");
  for (const phrase of phrases) {
    assert.ok(html.includes(phrase), `${route}: missing expected copy: ${phrase}`);
  }
}

const homepageHtml = readFileSync(path.join(root, "index.html"), "utf8");
const desktopNav = homepageHtml.match(/<nav class="primary stage-nav"[^>]*>([\s\S]*?)<\/nav>/)?.[1] ?? "";
const desktopNavLabels = [...desktopNav.matchAll(/<a\b[^>]*>([^<]+)<\/a>/g)].map((match) => match[1]);
assert.deepEqual(
  desktopNavLabels,
  ["Home", "About", "Drainage", "Services", "Projects", "Blog", "Contact"],
  "desktop navigation must begin with Home and About",
);
assert.ok(
  homepageHtml.includes('<div class="atlas archive-atlas" aria-label="Six kinds of groundwork">'),
  "Six kinds of groundwork must include its archival service atlas",
);
assert.equal(
  (homepageHtml.match(/<div class="cap"><h4>/g) ?? []).length,
  6,
  "Six kinds of groundwork must include all six service cards",
);

assert.ok(
  homepageHtml.includes('<a class="primary-service" href="drainage/">'),
  "homepage drainage service must receive the primary visual treatment",
);

const serviceNotes = new Map([
  ["services/drainage/index.html", "Standing water, washouts, and soggy ground all start as a drainage problem."],
  ["services/land-clearing-excavation/index.html", "Overgrowth out, grades cut, ground opened."],
  ["services/landscaping-hardscaping/index.html", "The finished layer — plantings, stonework, and the outdoor spaces people actually use."],
  ["services/seawalls-retention-waterproofing/index.html", "Where land meets water, the edge has to hold."],
  ["services/site-prep-culverts/index.html", "Before anything goes vertical, the pad, the pipe, and the path have to be right."],
  ["services/driveways/index.html", "The way in and the way home — built to take traffic and weather, season after season."],
]);

for (const [route, note] of serviceNotes) {
  const html = readFileSync(path.join(root, route), "utf8");
  assert.ok(html.includes(escapeHtml(note)), `${route}: missing original blueprint service note`);
  assert.ok(html.includes("Every property drains, grades, and wears differently."), `${route}: missing original consultation copy`);
  assert.ok(html.includes("Photo: Environmental Construction Services — from their public site."), `${route}: missing original photo attribution`);
}

const contactHtml = readFileSync(path.join(root, "contact", "index.html"), "utf8");
for (const name of ["name", "phone", "email", "location", "service", "timing", "issue", "notes"]) {
  assert.match(contactHtml, new RegExp(`name="${name}"`), `contact: missing ${name} worksheet field`);
}
assert.ok(contactHtml.includes("This private concept does not send or store the form."), "contact: missing mail-app privacy explanation");
const mainJs = readFileSync(path.join(root, "assets", "main.js"), "utf8");
assert.ok(mainJs.includes("Website request — "), "request worksheet: missing prepared-email subject");
assert.ok(mainJs.includes("Please add your name, one way to reach you"), "request worksheet: missing validation guidance");
assert.ok(mainJs.includes("Your email app is opening"), "request worksheet: missing success guidance");

const blogIndex = readFileSync(path.join(root, "blog", "index.html"), "utf8");
assert.ok(blogIndex.includes("reproduced from Environmental Construction Services’ own blog"), "blog: missing original provenance statement");
assert.equal(blogPosts.length, 8, "blog archive must contain eight posts");

for (const post of blogPosts) {
  const canonicalRoute = path.join(root, "blog", post.slug, "index.html");
  const aliasRoute = path.join(root, "post", post.slug, "index.html");
  const html = readFileSync(canonicalRoute, "utf8");
  const alias = readFileSync(aliasRoute, "utf8");
  const canonicalUrl = `https://ecs-drainage-field-notes.vercel.app/blog/${post.slug}/`;
  const coverAsset = localBlogAsset(post.cover);

  for (const value of [post.title, post.description, post.category, post.readingTime, formatDate(post.date), post.coverAlt]) {
    assert.ok(html.includes(escapeHtml(value)), `${post.slug}: missing canonical blog value: ${value}`);
  }
  assert.ok(html.includes(`<link rel="canonical" href="${canonicalUrl}">`), `${post.slug}: wrong canonical URL`);
  assert.ok(alias.includes(`<link rel="canonical" href="${canonicalUrl}">`), `${post.slug}: legacy alias lacks canonical URL`);
  assert.ok(html.includes('<meta property="og:type" content="article">'), `${post.slug}: missing article Open Graph type`);
  assert.ok(html.includes(`article:published_time" content="${post.date}T12:00:00Z`), `${post.slug}: missing publication date metadata`);
  assert.ok(html.includes('"@type": "BlogPosting"'), `${post.slug}: missing BlogPosting structured data`);
  assert.ok(html.includes("Questions about your property?"), `${post.slug}: missing consultation panel`);
  assert.ok(html.includes("More field notes."), `${post.slug}: missing related field notes`);
  assert.ok(html.includes("Get recommendations for your property."), `${post.slug}: missing final consultation band`);
  assert.ok(existsSync(path.join(root, "assets", coverAsset)), `${post.slug}: missing cover asset ${coverAsset}`);
  assert.equal(
    [...html.matchAll(new RegExp(`<img src="\\.\\.\\/\\.\\.\\/assets/${coverAsset.replaceAll(".", "\\.")}"`, "g"))].length,
    1,
    `${post.slug}: cover image should render once`,
  );

  const articleStart = html.indexOf('<div class="article-body">');
  const articleEnd = html.indexOf("</article>", articleStart);
  assert.ok(articleStart >= 0 && articleEnd > articleStart, `${post.slug}: missing article body boundary`);
  const articleBody = html.slice(articleStart, articleEnd);
  const expectedCounts = post.body.reduce((counts, block) => {
    if (block.type === "image" && block.src === post.cover) return counts;
    counts[block.type] += 1;
    return counts;
  }, { paragraph: 0, heading: 0, subheading: 0, listItem: 0, image: 0 });
  assert.equal([...articleBody.matchAll(/<h2>/g)].length, expectedCounts.heading, `${post.slug}: heading count differs from canonical JSON`);
  assert.equal([...articleBody.matchAll(/<h3>/g)].length, expectedCounts.subheading, `${post.slug}: subheading count differs from canonical JSON`);
  assert.equal([...articleBody.matchAll(/<li>/g)].length, expectedCounts.listItem, `${post.slug}: list-item count differs from canonical JSON`);
  assert.equal([...articleBody.matchAll(/<figure class="post-img">/g)].length, expectedCounts.image, `${post.slug}: body-image count differs from canonical JSON`);
  assert.equal([...articleBody.matchAll(/<p(?:\s|>)/g)].length, expectedCounts.paragraph + 2, `${post.slug}: paragraph count differs from canonical JSON`);

  for (const block of post.body) {
    if (block.type === "image") {
      const asset = localBlogAsset(block.src);
      assert.ok(existsSync(path.join(root, "assets", asset)), `${post.slug}: missing body image ${asset}`);
      assert.ok(html.includes(escapeHtml(block.alt)), `${post.slug}: missing image description`);
      continue;
    }
    const expected = escapeHtml(block.text);
    const tag = block.type === "heading" ? "h2" : block.type === "subheading" ? "h3" : block.type === "listItem" ? "li" : "p";
    assert.ok(html.includes(`<${tag}`) && html.includes(expected), `${post.slug}: missing ${block.type}: ${block.text}`);
  }
}

assert.ok(
  readFileSync(path.join(root, "blog", blogPosts[0].slug, "index.html"), "utf8").includes("1. Clay Soil and Poor Absorption"),
  "blog copy must not be rewritten during generation",
);

for (const file of walk(root).filter((candidate) => /\.(?:html|css|js|json|txt)$/i.test(candidate))) {
  const content = readFileSync(file, "utf8");
  assert.ok(
    !content.includes("environmental-construction-services.vercel.app") &&
      !content.includes("ecs-drainage.vercel.app"),
    `${path.relative(root, file)}: references an existing production domain`,
  );
}

console.log(`Validated ${htmlFiles.length} HTML files and all local references.`);
