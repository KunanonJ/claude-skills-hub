---
name: github-workflow-artifacts
description: "Upload, download, and reuse artifacts across GitHub Actions jobs and workflows — coverage reports, test results, build outputs, Playwright HTML reports. Trigger when the user mentions workflow artifacts, `actions/upload-artifact`, `actions/download-artifact`, sharing files between jobs, persisting CI build outputs, or environment-gated deployments. Sourced from github.com/skills/workflow-artifacts."
---

# GitHub Actions Workflow Artifacts

Use artifacts to pass files between jobs in a workflow, between workflows, or to persist them for downstream debugging. Think: "test report from one job that the next job uploads to S3" or "build once, deploy three times."

## When to Use Artifacts

- **Test reports** — Playwright HTML, jest-junit XML, coverage reports.
- **Build outputs** — compiled binaries, frontend bundles, Docker tar archives.
- **Reuse across jobs** — build job produces `dist/`, deploy job consumes it.
- **Reuse across workflows** — CI workflow stores build, Deploy workflow downloads it.
- **Debug evidence** — screenshots from failed E2E runs, log dumps.

Artifacts default to **90-day retention**. Configurable per-upload.

## Basic Upload + Download Within a Workflow

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 7

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - run: aws s3 sync dist/ s3://my-bucket/
```

The `needs: build` is critical — without it, the `deploy` job can start before `build` finishes and the artifact won't exist.

## Single-File Artifacts (Direct Preview)

For HTML reports, upload as a single file and it gets a "Preview" link in the GitHub UI:

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: playwright-report
    path: playwright-report/index.html
    if-no-files-found: error
```

Anyone with read access to the run can click the artifact and open the HTML directly in the browser — no download required.

## Always Upload, Even on Failure

Test reports are most useful when tests fail. Use `if: always()`:

```yaml
- name: Run tests
  run: npm test

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: |
      coverage/
      junit.xml
      screenshots/
```

Without `if: always()`, the upload skips when tests fail and you lose the evidence.

## Cross-Workflow Artifact Download

Use case: CI workflow builds and uploads, separate Deploy workflow downloads.

`ci.yml`:
```yaml
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ github.sha }}
          path: dist/
```

`deploy.yml`:
```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

permissions:
  contents: read
  actions: read       # required to read artifacts from another workflow run

jobs:
  deploy:
    if: github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-${{ github.event.workflow_run.head_sha }}
          run-id: ${{ github.event.workflow_run.id }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
      - run: ./deploy.sh
```

Required: `permissions.actions: read` plus the `run-id` and `github-token` inputs on download-artifact v4 when crossing workflow boundaries.

## Environment Gates — Approval Before Deploy

Combine artifacts with deployment environments to gate production:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
        with: { name: dist, path: dist/ }
      - run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production    # configure required reviewers in repo settings
    steps:
      - uses: actions/download-artifact@v4
        with: { name: dist, path: dist/ }
      - run: ./deploy.sh production
```

Configure the `production` environment under **Settings → Environments** with required reviewers. The deploy job pauses until a human approves, then runs with the original build artifact (no rebuild, no drift).

## Glob Patterns

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: logs
    path: |
      logs/**/*.log
      !logs/temp/**
      coverage/lcov.info
```

Supports include patterns (lines) and exclude patterns (lines starting with `!`).

## Merging Multiple Uploads

When matrix jobs each upload their own artifact, merge them:

```yaml
jobs:
  test:
    strategy:
      matrix: { shard: [1, 2, 3, 4] }
    runs-on: ubuntu-latest
    steps:
      - run: npx playwright test --shard=${{ matrix.shard }}/4
      - uses: actions/upload-artifact@v4
        with:
          name: report-${{ matrix.shard }}
          path: playwright-report/

  merge:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          pattern: report-*
          merge-multiple: true
          path: all-reports/
      - uses: actions/upload-artifact@v4
        with:
          name: combined-report
          path: all-reports/
```

`merge-multiple: true` flattens the downloaded directories.

## Size and Retention

- **Free tier**: 500 MB total storage per repo.
- **Pro/Team**: 2 GB. **Enterprise**: 50 GB. Overage billed.
- **Max single upload**: 10 GB.
- **Retention**: 1–90 days (default 90). Set lower to save quota.

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: big-build
    path: build/
    retention-days: 3
    compression-level: 9   # max compression, slower upload
```

## Anti-Patterns

- ❌ Uploading `node_modules/` — huge, deterministic from `package-lock.json`. Use caching, not artifacts.
- ❌ Forgetting `if: always()` on test report uploads — you only get reports when CI passes.
- ❌ Hardcoding `retention-days: 90` (default) for ephemeral build artifacts — fills your quota.
- ❌ Using `download-artifact@v3` syntax with `@v4` — v4 is not backward-compatible (different storage backend, no cross-version compat).
- ❌ Downloading artifacts from another workflow without `permissions.actions: read` — silent failure.
- ❌ Skipping `needs:` and assuming jobs run in declaration order.

## v3 → v4 Migration Notes

`actions/upload-artifact@v4` and `download-artifact@v4` changed substantially:
- Artifacts are now immutable — re-uploading with the same name **fails**, doesn't overwrite.
- v3 and v4 are NOT interoperable. A v3 upload cannot be downloaded by v4.
- v4 is significantly faster (98% reduction in end-to-end time for large artifacts).
- Cross-workflow downloads require new `run-id` + `github-token` inputs.

Migration: bump both upload and download in lockstep across the org. Don't mix.

## Quick Checklist

- [ ] Upload step has a stable `name`
- [ ] Test/report uploads use `if: always()`
- [ ] Job-to-job downloads have `needs:` set
- [ ] Cross-workflow downloads include `permissions.actions: read` + `run-id`
- [ ] `retention-days` set to something reasonable (3–14 for build artifacts)
- [ ] Using v4 of both upload and download actions

## References

- Source course: https://github.com/skills/workflow-artifacts
- Docs: https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
- v4 announcement: https://github.blog/changelog/2024-02-12-deprecation-notice-v1-and-v2-of-the-artifact-actions/
