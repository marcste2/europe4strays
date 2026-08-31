/* Europe4strays gallery builder.
   Reads photos/gallery/<year>/ and photos/gallery/vorher-nachher/,
   converts them to web-sized webp in assets/gallery/, merges with the
   curated entries in tools/gallery-extra.json, and writes gallery-data.js.

   Run from the build folder:  node tools/build-gallery.mjs            */

import { readdirSync, existsSync, mkdirSync, statSync, writeFileSync, readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, extname, basename } from "node:path";

const SRC = "photos/gallery";
const OUT = "assets/gallery";
const LATEST_COUNT = 6;
const MAX_W = 1400;
const EXT = new Set([".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"]);

/* ---- locate a full ffmpeg (the one on PATH is often stripped) ---- */
function findFfmpeg() {
  if (process.env.SCROLLCRAFT_FFMPEG) return process.env.SCROLLCRAFT_FFMPEG;
  const home = process.env.USERPROFILE || process.env.HOME || "";
  const base = join(home, "AppData/Local/Microsoft/WinGet/Packages");
  try {
    for (const d of readdirSync(base)) {
      if (!d.startsWith("Gyan.FFmpeg")) continue;
      for (const b of readdirSync(join(base, d))) {
        const p = join(base, d, b, "bin/ffmpeg.exe");
        if (existsSync(p)) return p;
      }
    }
  } catch {}
  return "ffmpeg";
}
const FF = findFfmpeg();

const slug = (s) =>
  s.toLowerCase()
    .replace(/[äàáâ]/g, "a").replace(/[öòóô]/g, "o").replace(/[üùúû]/g, "u")
    .replace(/[éèêë]/g, "e").replace(/[îí]/g, "i").replace(/ß/g, "ss")
    .replace(/[șş]/g, "s").replace(/[țţ]/g, "t")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");

/* "02 Bianco im Schnee__Hunderunde.jpg" -> caption + credit */
function parseName(file) {
  let name = basename(file, extname(file));
  let credit = null;
  const cut = name.split("__");
  if (cut.length > 1) { name = cut[0]; credit = cut.slice(1).join(" ").trim(); }
  const sortKey = name;
  name = name.replace(/^\d+[\s._-]+/, "");           // drop leading order number
  const cap = name.replace(/[-_]+/g, " ").trim();
  return { cap: cap || "Europe4strays", credit, sortKey };
}

function convert(from, to, maxW = MAX_W) {
  mkdirSync(join(to, ".."), { recursive: true });
  execFileSync(FF, ["-y", "-loglevel", "error", "-i", from,
    "-vf", `scale='min(${maxW},iw)':-2`, "-c:v", "libwebp", "-quality", "82", to]);
}

/* ---------- 1. year folders ---------- */
const photos = [];
let converted = 0;
const years = existsSync(SRC)
  ? readdirSync(SRC).filter((d) => /^\d{4}$/.test(d) && statSync(join(SRC, d)).isDirectory())
      .sort().reverse()
  : [];

for (const year of years) {
  const files = readdirSync(join(SRC, year)).filter((f) => EXT.has(extname(f)));
  files.sort().reverse();                              // newest first inside a year
  for (const f of files) {
    const { cap, credit } = parseName(f);
    const target = `${OUT}/${year}/${slug(basename(f, extname(f)))}.webp`;
    if (!existsSync(target)) { convert(join(SRC, year, f), target); converted++; }
    photos.push({ src: target, year, cap, ...(credit ? { credit } : {}) });
  }
}

/* ---------- 2. curated entries from elsewhere in assets/ ---------- */
const extra = JSON.parse(readFileSync("tools/gallery-extra.json", "utf8"));
photos.push(...extra.photos);

/* newest year first, folder photos before curated ones inside a year */
photos.sort((a, b) => Number(b.year) - Number(a.year));

/* ---------- 3. before / after pairs ---------- */
const pairs = [];
const baDir = join(SRC, "vorher-nachher");
if (existsSync(baDir)) {
  const files = readdirSync(baDir).filter((f) => EXT.has(extname(f)));
  const stems = new Map();
  for (const f of files) {
    const n = basename(f, extname(f));
    const m = n.match(/^(.*?)[-_ ]+(vorher|before|nachher|after|collage)$/i);
    if (!m) continue;
    const stem = m[1], kind = m[2].toLowerCase();
    if (!stems.has(stem)) stems.set(stem, {});
    stems.get(stem)[kind] = f;
  }
  for (const [stem, k] of stems) {
    const capName = stem.replace(/[-_]+/g, " ").trim();
    const s = slug(stem);
    if (k.collage) {                                   // split a side-by-side image in half
      const src = join(baDir, k.collage);
      const before = `${OUT}/ba/${s}-before.webp`;
      const after = `${OUT}/ba/${s}-after.webp`;
      mkdirSync(`${OUT}/ba`, { recursive: true });
      if (!existsSync(before)) {
        execFileSync(FF, ["-y", "-loglevel", "error", "-i", src,
          "-vf", "crop=iw/2:ih:0:0,scale='min(1200,iw)':-2", "-c:v", "libwebp", "-quality", "82", before]);
        execFileSync(FF, ["-y", "-loglevel", "error", "-i", src,
          "-vf", "crop=iw/2:ih:iw/2:0,scale='min(1200,iw)':-2", "-c:v", "libwebp", "-quality", "82", after]);
        converted += 2;
      }
      pairs.push({ before, after, cap: capName });
    } else if ((k.vorher || k.before) && (k.nachher || k.after)) {
      const b = `${OUT}/ba/${s}-before.webp`;
      const a = `${OUT}/ba/${s}-after.webp`;
      if (!existsSync(b)) { convert(join(baDir, k.vorher || k.before), b, 1200); converted++; }
      if (!existsSync(a)) { convert(join(baDir, k.nachher || k.after), a, 1200); converted++; }
      pairs.push({ before: b, after: a, cap: capName });
    } else {
      console.warn(`  ! "${stem}" has only one half, skipped`);
    }
  }
}
pairs.push(...extra.pairs);

/* ---------- 4. write the manifest ---------- */
const out =
`/* GENERATED by tools/build-gallery.mjs - do not edit by hand.
   Add photos in photos/gallery/<year>/ and run the script again.
   ${photos.length} photos, ${pairs.length} before/after pair(s). */
window.E4S_GALLERY = {
  latestCount: ${LATEST_COUNT},
  photos: ${JSON.stringify(photos, null, 2).replace(/\n/g, "\n  ")},
  pairs: ${JSON.stringify(pairs, null, 2).replace(/\n/g, "\n  ")}
};
`;
writeFileSync("gallery-data.js", out);

const byYear = {};
for (const p of photos) byYear[p.year] = (byYear[p.year] || 0) + 1;
console.log(`gallery-data.js written: ${photos.length} photos, ${pairs.length} pair(s), ${converted} newly converted`);
console.log("per year:", Object.entries(byYear).sort((a, b) => b[0] - a[0]).map(([y, n]) => `${y}:${n}`).join("  "));
