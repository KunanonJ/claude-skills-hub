---
name: github-release-workflow
description: "Set up a release-based GitHub workflow with semver tags, release branches, release notes, and hotfix flow. Trigger when the user mentions GitHub releases, release branching, tag-based releases, semver, release notes generation, hotfix workflow, or wants a packaged versioned deliverable. Sourced from github.com/skills/release-based-workflow."
---

# Release-Based GitHub Workflow

GitHub flow (branch from main → PR → merge) is great for continuous deploy. Add **releases** on top when you need versioned, packaged software that consumers download — libraries, CLIs, mobile binaries, on-prem distributions.

## The Branching Pattern

```
main ────────●──●────●─────●─────●────────→ (always shippable)
                \                  \
                 release/1.0 ──●───●─── tag v1.0.0
                                       \
                                        release/1.0.1 ─●─ tag v1.0.1 (hotfix)
```

- `main` is always shippable.
- Cut a `release/X.Y` branch when feature-complete for that minor version.
- Polish (bug fixes, release notes) happens on the release branch.
- Tag `vX.Y.Z` at the finish line. Push back to main if anything important was fixed on the branch.
- For urgent fixes against a shipped version, branch from the tag, fix, tag `vX.Y.(Z+1)`.

## Semver Quick Rules

- `vMAJOR.MINOR.PATCH`
- **MAJOR**: breaking change (consumer must update their code)
- **MINOR**: backward-compatible feature
- **PATCH**: backward-compatible fix
- Prereleases: `v1.0.0-beta.1`, `v1.0.0-rc.2`. GitHub treats anything matching `-[a-z]` as "pre-release" by default.

## Beta Release Cycle

```bash
# Cut a release branch from main
git switch -c release/1.0 main
git push -u origin release/1.0

# Tag a beta on it
git tag v1.0.0-beta.1
git push --tags

# Create the GitHub Release marked "pre-release"
gh release create v1.0.0-beta.1 \
  --target release/1.0 \
  --title "1.0.0 Beta 1" \
  --prerelease \
  --generate-notes
```

`--generate-notes` builds release notes from PR titles since the last tag. Customize via `.github/release.yml`:

```yaml
changelog:
  categories:
    - title: Breaking Changes
      labels: ["breaking"]
    - title: New Features
      labels: ["enhancement", "feature"]
    - title: Bug Fixes
      labels: ["bug"]
    - title: Other Changes
      labels: ["*"]
  exclude:
    labels: ["chore", "docs", "test"]
```

PRs get categorized by label.

## Final Release

When the beta has soaked, cut the GA:

```bash
git tag v1.0.0
git push --tags

gh release create v1.0.0 \
  --target release/1.0 \
  --title "1.0.0" \
  --generate-notes \
  --latest
```

`--latest` updates the "Latest release" pointer (the one your README badge links to).

If important fixes happened on the release branch that aren't on main, merge the branch back:
```bash
git switch main
git merge --no-ff release/1.0
git push
```

## Hotfix Flow

A critical bug in v1.0.0. Don't bring main's WIP into the fix.

```bash
# Branch from the tag, not main
git switch -c hotfix/1.0.1 v1.0.0

# Fix
git commit -m "fix: handle null user id in /me endpoint"

# Tag and release
git tag v1.0.1
git push origin hotfix/1.0.1 --tags

gh release create v1.0.1 \
  --target hotfix/1.0.1 \
  --title "1.0.1 - Critical fix" \
  --generate-notes \
  --latest

# Merge fix back into main (and any active release branch)
git switch main
git cherry-pick <fix-commit>
git push
```

## Tag-Triggered Release Workflow

Automate the build-and-publish when a tag is pushed:

```yaml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write
  packages: write
  id-token: write
  attestations: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: npm ci && npm run build && npm test

      - name: Package
        run: npm pack
        # produces my-pkg-1.0.0.tgz

      - name: Publish to npm
        run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Create GitHub Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create ${{ github.ref_name }} \
            --title "${{ github.ref_name }}" \
            --generate-notes \
            ./my-pkg-*.tgz
```

For a prerelease tag, add `--prerelease` automatically:
```bash
[[ "${{ github.ref_name }}" =~ -[a-z] ]] && PRE="--prerelease" || PRE=""
gh release create ${{ github.ref_name }} $PRE ...
```

## Linking Issues + PRs to Releases

GitHub auto-links any issue closed by a PR merged between two tags. Show this on the release page:

In PR body: `Closes #123`. When tagged and released, #123 shows up under "What's Changed."

## When NOT to Use Release Branches

If you ship continuously to production (SaaS, every-merge-deploys), you don't need release branches. Tag every shipped commit if you want versioning, but don't pay the merge-back cost.

Use release branches when:
- Shipping a downloadable artifact (CLI binary, mobile app, on-prem package)
- Customers pin to specific versions
- You support multiple major versions concurrently
- You need a "freeze + polish" window between feature-complete and GA

## Anti-Patterns

- ❌ Tagging `latest` as a moving git tag — use `gh release edit --latest` to update the GitHub Release pointer instead. Git tags should be immutable.
- ❌ Breaking semver — adding a required parameter in a minor release. Customers expect minor = additive.
- ❌ Hotfixing from main and pretending it's a 1.0.x fix — accidentally includes WIP. Branch from the tag.
- ❌ No `.github/release.yml` — release notes become unfiltered PR titles, including `chore: bump deps`.
- ❌ Force-pushing a tag — breaks anyone who pinned to it. Cut a new tag instead.

## Quick Checklist

- [ ] `.github/release.yml` configures changelog categories
- [ ] PR labels (`feature`, `bug`, `breaking`, `chore`) used consistently
- [ ] Tag-triggered workflow handles build + publish + GitHub Release
- [ ] Hotfix runbook documented (branch from tag, not main)
- [ ] Beta releases marked `--prerelease`
- [ ] GA releases mark `--latest`
- [ ] Release branch merges back into main when it diverges

## References

- Source course: https://github.com/skills/release-based-workflow
- gh release docs: https://cli.github.com/manual/gh_release
- Auto-generated release notes config: https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes
- Semver spec: https://semver.org/
