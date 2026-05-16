---
name: github-reusable-workflows
description: "Author reusable GitHub Actions workflows callable via `workflow_call` — inputs, secrets, outputs, and permission propagation between caller and callee. Trigger when the user mentions reusable workflows, workflow_call, calling workflows from other workflows, DRY GHA, shared CI workflows, or wants to reduce duplication across repos. Sourced from github.com/skills/reusable-workflows."
---

# Reusable GitHub Actions Workflows

Stop copy-pasting `test.yml`, `lint.yml`, and `deploy.yml` across repos and branches. Define them once with `workflow_call`, then invoke from anywhere.

## When to Use

- Same CI steps repeated across multiple repos or workflows.
- Org-wide CI policy (security scans, dependency review) you want enforced from one place.
- Composable pipelines — caller decides which checks to run.
- Centralized fixes — patch a bug once, all callers benefit on next run.

## The Two Pieces

### The reusable workflow (callee)

`.github/workflows/reusable-tests.yml`:
```yaml
name: Reusable Tests

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: "20"
      run-coverage:
        type: boolean
        default: false
    secrets:
      CODECOV_TOKEN:
        required: false
    outputs:
      coverage-pct:
        description: "Line coverage percentage"
        value: ${{ jobs.test.outputs.pct }}

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      pct: ${{ steps.cov.outputs.pct }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
      - run: npm ci
      - run: npm test
      - if: ${{ inputs.run-coverage }}
        id: cov
        run: |
          PCT=$(npm run coverage --silent | grep -oP '\d+(?=%)' | head -1)
          echo "pct=$PCT" >> "$GITHUB_OUTPUT"
      - if: ${{ inputs.run-coverage && env.CODECOV_TOKEN != '' }}
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
        uses: codecov/codecov-action@v4
```

### The caller workflow

`.github/workflows/ci.yml`:
```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    uses: ./.github/workflows/reusable-tests.yml
    with:
      node-version: "20"
      run-coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  report:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo "Coverage was ${{ needs.test.outputs.coverage-pct }}%"
```

## Calling Across Repos

Reference by full path including ref:

```yaml
jobs:
  test:
    uses: my-org/shared-workflows/.github/workflows/test.yml@v1.2.0
```

Rules:
- Caller and callee repos must be **in the same org** or callee must be **public**.
- Pin to a **tag or commit SHA**, never a branch — branch refs let the callee mutate behavior under you.
- For private callees: enable at **Org Settings → Actions → General → Access** for the consuming repos.

## Permissions: The #1 Gotcha

Permissions **don't inherit from caller to callee**. Each side sets its own.

The effective permission is the **intersection** of caller and callee. If the caller has `contents: read` and the callee declares `contents: write`, the job runs with `contents: read`.

```yaml
# Caller
permissions:
  contents: read
  pull-requests: write

jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    # Callee inherits NOTHING. It must declare its own permissions.
```

```yaml
# Callee — explicit
permissions:
  contents: read
  pull-requests: write
  id-token: write   # for OIDC
```

Without explicit permissions on the callee, you get the default token, which may be too permissive or too restrictive depending on the org default. **Always declare permissions explicitly in reusable workflows.**

## Secrets Patterns

### Pass individual secrets

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy.yml
    secrets:
      AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
```

### Pass all secrets (use sparingly)

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy.yml
    secrets: inherit
```

`secrets: inherit` means every secret in the caller's scope flows to the callee. Convenient but blast-radius wide — prefer enumerating.

## Outputs Across Jobs

Job-level outputs from the called workflow are available via `needs.<job>.outputs.<name>` in the caller:

```yaml
jobs:
  build:
    uses: ./.github/workflows/build.yml

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Built ${{ needs.build.outputs.image-tag }}"
```

Callee must declare outputs at the top level under `workflow_call.outputs`, mapping from job outputs.

## Matrix in the Caller

You can fan out a reusable workflow via matrix:

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: ["18", "20", "22"]
    uses: ./.github/workflows/reusable-tests.yml
    with:
      node-version: ${{ matrix.node }}
```

Each matrix value triggers a separate run of the reusable workflow.

## Reusable vs Composite Actions

| | Reusable workflow | Composite action |
|---|---|---|
| Runs as | A separate job (own runner) | Steps in caller's job |
| Has its own `runs-on` | Yes | No (inherits) |
| Can call other workflows | Yes (with limits) | No |
| Can use `if:`, matrix at the call site | Yes | Limited |
| Use when | Encapsulating a whole pipeline stage | Encapsulating a sequence of steps |

## Limits

- A workflow_call chain can be at most **4 levels deep** (caller → reusable → reusable → reusable).
- Max **20 unique reusable workflows** called per workflow.
- `env` from caller does NOT propagate. Re-declare or pass as input.

## Anti-Patterns

- ❌ Calling `@main` — silent breakage when the callee evolves.
- ❌ Reusable workflow with no `permissions:` block — relies on org default, unpredictable.
- ❌ `secrets: inherit` for callees that only need one secret.
- ❌ Copying the same 50-line job into 8 repos instead of extracting.
- ❌ Reusable workflow that does five unrelated things — split it; let caller compose.
- ❌ Trying to use `env:` to pass values to a callee — use `inputs:`.

## Quick Setup Checklist

- [ ] Reusable workflow has `on: workflow_call:` with explicit `inputs` and `secrets`
- [ ] Callee declares its own `permissions:` block — no implicit inheritance
- [ ] Caller pins callee by tag or SHA (never branch)
- [ ] If cross-org, callee is public OR org policy allows the cross-repo access
- [ ] Outputs declared at `workflow_call.outputs` if caller needs them
- [ ] Documentation comment at the top of the reusable file listing inputs and example caller

## References

- Source course: https://github.com/skills/reusable-workflows
- Docs: https://docs.github.com/en/actions/using-workflows/reusing-workflows
- Permissions: https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs
