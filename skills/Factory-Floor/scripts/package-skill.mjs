#!/usr/bin/env node
// Package Factory Floor into a distributable .skill file.
// Matches the skill-creator packager format: a zip with the skill directory
// as the top-level entry (e.g. "Factory Floor/SKILL.md").

import { readFileSync, existsSync, rmSync, renameSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { basename, dirname, resolve, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const skillRoot = resolve(__dirname, '..')
const skillName = basename(skillRoot)
const parentDir = dirname(skillRoot)
const outputFile = join(skillRoot, `${skillName}.skill`)

// Validate SKILL.md frontmatter has name + description.
const skillMd = join(skillRoot, 'SKILL.md')
if (!existsSync(skillMd)) {
  console.error('SKILL.md not found')
  process.exit(1)
}

const content = readFileSync(skillMd, 'utf8')
const fmMatch = content.match(/^---\n([\s\S]*?)\n---/)
if (!fmMatch) {
  console.error('SKILL.md is missing YAML frontmatter')
  process.exit(1)
}
const frontmatter = fmMatch[1]
if (!/^name:\s*\S/m.test(frontmatter)) {
  console.error('SKILL.md frontmatter is missing `name`')
  process.exit(1)
}
if (!/^description:\s*\S/m.test(frontmatter)) {
  console.error('SKILL.md frontmatter is missing `description`')
  process.exit(1)
}

console.log(`Packaging skill: ${skillName}`)

// Remove any stale .skill at the output location so it's not swept into the zip.
if (existsSync(outputFile)) rmSync(outputFile)

// Exclude patterns match the skill-creator Python packager.
const excludes = [
  `${skillName}/.git/*`,
  `${skillName}/__pycache__/*`,
  `${skillName}/**/__pycache__/*`,
  `${skillName}/node_modules/*`,
  `${skillName}/**/node_modules/*`,
  `${skillName}/.venv/*`,
  `${skillName}/venv/*`,
  `${skillName}/.env/*`,
  `${skillName}/*.skill`,
  `${skillName}/**/*.pyc`,
  `${skillName}/**/*.pyo`,
]

// Write the zip to the parent dir so the archive file isn't part of its own input.
const stagedZip = join(parentDir, `${skillName}.skill`)
if (existsSync(stagedZip)) rmSync(stagedZip)

try {
  execFileSync(
    'zip',
    ['-r', '-q', `${skillName}.skill`, `${skillName}/`, '-x', ...excludes],
    { cwd: parentDir, stdio: 'inherit' },
  )
} catch (err) {
  console.error(`zip failed: ${err.message}`)
  process.exit(1)
}

renameSync(stagedZip, outputFile)
console.log(`Packaged to ${outputFile}`)
