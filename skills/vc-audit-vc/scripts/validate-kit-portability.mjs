#!/usr/bin/env node
// Standing portability audit for the agent-harness kit.
//
// Mirrors the two checks the widened vc-publish Step 8 gate runs, but walks the
// shipped text surface DIRECTLY (the dev repo lacks resolve-manifest.mjs -- it is
// kitOnly), so this validator can run in CI where the resolver is absent.
//
//   Check (a) -- product-name leak: flowser|CloakBrowser|OpenClaw|Supabase
//   Check (b) -- dangling context-path leak: a concrete backticked
//                process/context/<file> ref that is NOT a shipped/seeded survivor.
//
// CRITICAL DESIGN POINT: check (b) is validated against the shipped-SURVIVOR
// allowlist (what ships/seeds), NOT against local disk existence. In the publish
// source repo the leaked refs (uxui/uiux.md, tests/browser-automation.md,
// generated-skills-catalog.json under process/context) exist on disk, so a naive
// disk-existence check would never catch the leak in the publish source.
//
// Brand scan is product-names ONLY. It intentionally does NOT scan for
// `tRPC` / `Prisma` / `ck` / `ckignore`. The legacy `.ck.json` / `.ckignore`
// fallback literals (Phase 2 back-compat read path) are intentional and must NOT
// be flagged.

import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const failures = [];
const warnings = [];

function fail(message) {
  failures.push(message);
}

function warn(message) {
  warnings.push(message);
}

const SKIP_DIR = "node_" + "modules";

function walk(dir, predicate, out = []) {
  const abs = path.join(root, dir);
  if (!fs.existsSync(abs)) return out;
  for (const entry of fs.readdirSync(abs, { withFileTypes: true })) {
    const rel = path.join(dir, entry.name);
    if (rel.includes(SKIP_DIR)) continue;
    if (entry.isDirectory()) walk(rel, predicate, out);
    else if (!predicate || predicate(rel)) out.push(rel);
  }
  return out;
}

// Enumerated shipped TEXT surfaces (mirror of the vc-publish Step 8 resolved set,
// minus the resolver). Excludes binaries and node_modules (via SKIP_DIR).
const textFiles = [
  "CLAUDE.md",
  "AGENTS.md",
  ...walk(".claude/skills", (rel) => /\.(md|cjs|mjs|py|js|json)$/.test(rel)),
  ...walk(".claude/agents", (rel) => rel.endsWith(".md")),
  ...walk(".codex", (rel) => /\.(md|toml|cjs|mjs|py|js|json)$/.test(rel)),
  ...walk("process/development-protocols", (rel) => rel.endsWith(".md")),
].filter((rel) => fs.existsSync(path.join(root, rel)));

// ---------------------------------------------------------------------------
// Check (a) -- product-name leak scan (brand list is product-names ONLY).
// ---------------------------------------------------------------------------
const BRAND_RE = /flowser|CloakBrowser|OpenClaw|Supabase/i;

// Bucket-4 line-content allowlist: lines that MUST keep a brand literal to
// function. A brand hit on one of these lines is legitimate, not a leak.
//   - `author: flowser`          -- maintainer frontmatter tag, not a project leak
//   - isFlowserActivePlanPath    -- internal code identifier (vc-watzup scan)
//   - this validator's + vc-publish's OWN brand-pattern lines (grep / regex strings)
//     -- otherwise the gate flags itself. Matched via the BRAND_LITERAL_MARKER and
//     the grep-invocation markers below.
//   - the internal hook comment about plan-generation validation workflows in
//     session-init.cjs -- Bucket-4 do-not-touch internal context. Exempted by its
//     exact phrase (specific enough that no real leak would coincide with it).
const BRAND_ALLOWLIST_MARKERS = [
  "author: flowser",
  "isFlowserActivePlanPath",
  "grep -ri",
  "grep -rIin",
  "BRAND_RE",
  "BRAND_ALLOWLIST_MARKERS",
  "BRAND_LITERAL_MARKER",
  "Flowser plan generation",
];

// A literal marker that lives ONLY on this validator's own pattern/doc lines so
// the validator never flags itself. Any line containing it is skipped by check (a).
const BRAND_LITERAL_MARKER = "flowser|CloakBrowser|OpenClaw|Supabase";

function isBrandAllowlisted(line) {
  if (line.includes(BRAND_LITERAL_MARKER)) return true;
  return BRAND_ALLOWLIST_MARKERS.some((marker) => line.includes(marker));
}

for (const file of textFiles) {
  const lines = fs.readFileSync(path.join(root, file), "utf8").split("\n");
  lines.forEach((line, index) => {
    if (!BRAND_RE.test(line)) return;
    if (isBrandAllowlisted(line)) return;
    fail(`${file}:${index + 1} product-name leak: ${line.trim().slice(0, 160)}`);
  });
}

// ---------------------------------------------------------------------------
// Check (b) -- dangling concrete context-path leak.
//
// Mirror validate-context-discovery.mjs ref extraction:
//   - match backticked `process/context/<ref>` tokens
//   - strip trailing punctuation
//   - skip glob/placeholder refs ( { } [ * ] )
// Then, instead of a disk check, classify CONCRETE FILE refs (a real filename
// with extension, not a directory or an ellipsis placeholder) and FAIL any that
// are not in the shipped-SURVIVOR allowlist.
// ---------------------------------------------------------------------------
const CONTEXT_SURVIVORS = new Set([
  "process/context/all-context.md",
  "process/context/tests/all-tests.md",
]);

function isConcreteContextFileRef(ref) {
  if (/[{}[*\]]/.test(ref)) return false; // glob / placeholder
  if (ref.includes("..")) return false; // ellipsis placeholder (process/context/...)
  if (ref.endsWith("/")) return false; // directory reference
  // last path segment must look like a real filename with an extension
  if (!/\/[^/]*\.[A-Za-z0-9]+$/.test(ref)) return false;
  return true;
}

for (const file of textFiles) {
  const lines = fs.readFileSync(path.join(root, file), "utf8").split("\n");
  lines.forEach((line, index) => {
    for (const match of line.matchAll(/`(process\/context\/[^`\s]+)`/g)) {
      const ref = match[1].replace(/[.,;:]+$/, "");
      if (!isConcreteContextFileRef(ref)) continue; // portable dir/glob/ellipsis ref
      if (CONTEXT_SURVIVORS.has(ref)) continue; // shipped/seeded survivor
      fail(
        `${file}:${index + 1} non-portable context path leak: \`${ref}\` is not a shipped/seeded survivor`,
      );
    }
  });
}

const result = {
  checkedFiles: textFiles.length,
  warnings,
  failures,
};

console.log(JSON.stringify(result, null, 2));

if (failures.length > 0) {
  process.exitCode = 1;
}
