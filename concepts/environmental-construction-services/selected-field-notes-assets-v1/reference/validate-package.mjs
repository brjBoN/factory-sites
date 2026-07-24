import { createHash } from "node:crypto";
import { readFile, readdir, stat } from "node:fs/promises";
import { dirname, extname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const manifestPath = resolve(packageRoot, "manifest.json");
const failures = [];

let manifest;
try {
  manifest = JSON.parse(await readFile(manifestPath, "utf8"));
} catch (error) {
  console.error(`Could not parse manifest.json: ${error.message}`);
  process.exit(1);
}

function normalizePath(path) {
  return path.replaceAll("\\", "/");
}

async function listFiles(directory) {
  const output = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const fullPath = resolve(directory, entry.name);
    if (entry.isDirectory()) output.push(...(await listFiles(fullPath)));
    else output.push(normalizePath(relative(packageRoot, fullPath)));
  }
  return output;
}

function detectMime(bytes, path) {
  const extension = extname(path).toLowerCase();
  if (
    bytes.length >= 8 &&
    bytes.subarray(0, 8).equals(
      Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    )
  ) {
    return "image/png";
  }
  if (
    bytes.length >= 12 &&
    bytes.toString("ascii", 0, 4) === "RIFF" &&
    bytes.toString("ascii", 8, 12) === "WEBP"
  ) {
    return "image/webp";
  }
  if (
    bytes.length >= 12 &&
    bytes.toString("ascii", 4, 8) === "ftyp" &&
    ["avif", "avis", "mif1"].includes(bytes.toString("ascii", 8, 12))
  ) {
    return "image/avif";
  }
  if (extension === ".svg" && bytes.toString("utf8", 0, 512).includes("<svg")) {
    return "image/svg+xml";
  }
  const textMimes = {
    ".md": "text/markdown",
    ".json": "application/json",
    ".css": "text/css",
    ".mjs": "text/javascript",
  };
  return textMimes[extension] ?? "application/octet-stream";
}

function imageDimensions(bytes, mimeType) {
  if (mimeType === "image/png" && bytes.length >= 24) {
    return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
  }

  if (mimeType === "image/svg+xml") {
    const header = bytes.toString("utf8", 0, Math.min(bytes.length, 2048));
    const width = Number(header.match(/\bwidth="(\d+)"/)?.[1]);
    const height = Number(header.match(/\bheight="(\d+)"/)?.[1]);
    return width && height ? { width, height } : null;
  }

  if (mimeType === "image/webp" && bytes.length >= 30) {
    const chunk = bytes.toString("ascii", 12, 16);
    if (chunk === "VP8X") {
      return {
        width: 1 + bytes.readUIntLE(24, 3),
        height: 1 + bytes.readUIntLE(27, 3),
      };
    }
    if (chunk === "VP8 " && bytes.length >= 30) {
      return {
        width: bytes.readUInt16LE(26) & 0x3fff,
        height: bytes.readUInt16LE(28) & 0x3fff,
      };
    }
    if (chunk === "VP8L" && bytes.length >= 25 && bytes[20] === 0x2f) {
      const bits = bytes.readUInt32LE(21);
      return {
        width: 1 + (bits & 0x3fff),
        height: 1 + ((bits >>> 14) & 0x3fff),
      };
    }
  }

  if (mimeType === "image/avif") {
    const index = bytes.indexOf(Buffer.from("ispe"));
    if (index >= 0 && bytes.length >= index + 16) {
      return {
        width: bytes.readUInt32BE(index + 8),
        height: bytes.readUInt32BE(index + 12),
      };
    }
  }

  return null;
}

if (!Array.isArray(manifest.assets)) {
  failures.push("manifest.assets must be an array");
}

const assets = Array.isArray(manifest.assets) ? manifest.assets : [];
const seenPaths = new Set();
for (const asset of assets) {
  if (!asset.path || seenPaths.has(asset.path)) {
    failures.push(
      asset.path ? `${asset.path}: duplicate path` : "asset entry missing path",
    );
    continue;
  }
  seenPaths.add(asset.path);

  const filePath = resolve(packageRoot, asset.path);
  if (
    filePath !== packageRoot &&
    !filePath.startsWith(`${packageRoot}${sep}`)
  ) {
    failures.push(`${asset.path}: path escapes package root`);
    continue;
  }

  try {
    const fileStat = await stat(filePath);
    const fileBytes = await readFile(filePath);
    const sha256 = createHash("sha256").update(fileBytes).digest("hex");
    const mimeType = detectMime(fileBytes, asset.path);
    const dimensions = imageDimensions(fileBytes, mimeType);

    if (!fileStat.isFile()) failures.push(`${asset.path}: is not a file`);
    if (fileStat.size !== asset.bytes) {
      failures.push(
        `${asset.path}: expected ${asset.bytes} bytes, found ${fileStat.size}`,
      );
    }
    if (sha256 !== asset.sha256) {
      failures.push(`${asset.path}: SHA-256 mismatch`);
    }
    if (mimeType !== asset.mimeType) {
      failures.push(
        `${asset.path}: expected ${asset.mimeType}, detected ${mimeType}`,
      );
    }
    if (
      asset.dimensions &&
      dimensions &&
      (dimensions.width !== asset.dimensions.width ||
        dimensions.height !== asset.dimensions.height)
    ) {
      failures.push(
        `${asset.path}: expected ${asset.dimensions.width}x${asset.dimensions.height}, detected ${dimensions.width}x${dimensions.height}`,
      );
    }
  } catch (error) {
    failures.push(`${asset.path}: ${error.message}`);
  }
}

const diskFiles = (await listFiles(packageRoot))
  .filter((path) => path !== "manifest.json")
  .sort();
const manifestFiles = [...seenPaths].sort();
for (const missing of diskFiles.filter((path) => !seenPaths.has(path))) {
  failures.push(`${missing}: present on disk but missing from manifest`);
}
for (const missing of manifestFiles.filter((path) => !diskFiles.includes(path))) {
  failures.push(`${missing}: present in manifest but missing from disk`);
}

const expectedLogoHashes = {
  "brand/ecs-logo-original.png":
    "f4977e8ebd4420f689f8d46c93d474559fb673d6ce303a5022a0abb08eea5454",
  "brand/ecs-logo-as-served.avif":
    "461a69c2753b010534cbcda1cffc178ba1be6143b1631021a08c77c4352c3c6c",
};
for (const [path, expectedHash] of Object.entries(expectedLogoHashes)) {
  const asset = assets.find((item) => item.path === path);
  if (!asset || asset.sha256 !== expectedHash) {
    failures.push(`${path}: exact first-party logo hash is not preserved`);
  }
}

if (failures.length > 0) {
  console.error("Asset package validation failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(
  `Asset package validation passed: ${assets.length} manifested files; exact logo hashes preserved.`,
);
