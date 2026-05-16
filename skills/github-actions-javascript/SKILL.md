---
name: github-actions-javascript
description: "Author a custom JavaScript GitHub Action — `action.yml` metadata, `@actions/core` toolkit, bundling with ncc/esbuild, inputs/outputs, testing locally with act. Trigger when the user wants to write a custom GitHub Action, build a marketplace action, package JS into a distributable action, or extend GHA with custom logic. Sourced from github.com/skills/write-javascript-actions."
---

# Writing JavaScript GitHub Actions

Build custom GitHub Actions in JavaScript when off-the-shelf actions don't fit. Faster startup than Docker actions, less ceremony than composite actions for non-trivial logic.

## When to Build One

- Reusing the same shell scripting across many workflows → wrap as an action.
- Need access to the GitHub API with proper auth (`@actions/github`).
- Want to publish to the Marketplace.
- Output is consumed by downstream steps.

**Don't** write a JS action when:
- A composite action (just steps) does the job — less complexity.
- A simple `run: |` block with `gh` CLI does it — no packaging overhead.

## Project Structure

```
my-action/
├── action.yml          # metadata — required at repo root
├── src/
│   └── index.js        # entrypoint
├── dist/
│   └── index.js        # bundled, committed
├── package.json
└── README.md
```

## action.yml — The Contract

```yaml
name: "Dad Joke Fetcher"
description: "Returns a random dad joke as output"
author: "you"

branding:
  icon: "smile"
  color: "yellow"

inputs:
  category:
    description: "Joke category (e.g. 'food', 'animals')"
    required: false
    default: "general"
  max-length:
    description: "Maximum joke length in characters"
    required: false
    default: "200"

outputs:
  joke:
    description: "The joke text"
  source:
    description: "Source API URL"

runs:
  using: "node20"
  main: "dist/index.js"
  post: "dist/cleanup.js"   # optional, runs after job
```

`runs.using: node20` is current. Avoid `node12` and `node16` (deprecated/removed).

## The Source File

`src/index.js`:
```js
const core = require("@actions/core");
const github = require("@actions/github");

async function run() {
  try {
    const category = core.getInput("category");
    const maxLength = parseInt(core.getInput("max-length"), 10);

    core.debug(`Fetching joke for category: ${category}`);

    const res = await fetch("https://icanhazdadjoke.com/", {
      headers: { Accept: "application/json" }
    });
    if (!res.ok) {
      throw new Error(`API returned ${res.status}`);
    }
    const data = await res.json();
    const joke = data.joke.slice(0, maxLength);

    core.setOutput("joke", joke);
    core.setOutput("source", "https://icanhazdadjoke.com");

    // Summary that shows up in the Actions UI
    await core.summary
      .addHeading("Today's Joke")
      .addQuote(joke)
      .write();

    // For triggers like issue_comment, post a reply
    if (github.context.eventName === "issue_comment") {
      const token = core.getInput("github-token", { required: true });
      const octokit = github.getOctokit(token);
      const { owner, repo } = github.context.repo;
      const issue_number = github.context.payload.issue.number;
      await octokit.rest.issues.createComment({ owner, repo, issue_number, body: joke });
    }
  } catch (err) {
    core.setFailed(err.message);
  }
}

run();
```

## @actions/core Toolkit Cheatsheet

| Call | What it does |
|---|---|
| `core.getInput("name")` | Read input from workflow |
| `core.getBooleanInput("flag")` | Read `true`/`false` input |
| `core.setOutput("name", val)` | Set output for downstream steps |
| `core.exportVariable("X", "v")` | Set env var for subsequent steps |
| `core.setSecret("v")` | Mask `v` in logs |
| `core.debug("msg")` | Visible only with `ACTIONS_STEP_DEBUG=true` |
| `core.warning("msg")` | Yellow warning in summary |
| `core.error("msg")` | Red error in summary, doesn't fail |
| `core.setFailed("msg")` | Sets exit code 1 and fails the step |
| `core.summary.addHeading(...).write()` | Rich markdown step summary |
| `core.startGroup("x")` / `core.endGroup()` | Collapsible log groups |
| `core.saveState(k, v)` / `core.getState(k)` | Pass data between `main` and `post` |

## Bundling — Why You Commit dist/

GitHub Actions runners don't run `npm install` for you. You ship the entire `node_modules` graph in one file. Use `@vercel/ncc`:

```bash
npm install --save-dev @vercel/ncc
npx ncc build src/index.js -o dist
```

`package.json` scripts:
```json
{
  "scripts": {
    "build": "ncc build src/index.js -o dist --source-map --license licenses.txt",
    "test": "jest",
    "prepare": "npm run build"
  }
}
```

**Commit `dist/`** — even though it feels wrong. The marketplace and `uses: my-org/my-action@v1` syntax point to a ref; without `dist/`, the runner can't execute.

## Versioning

Tag releases AND maintain a major-version ref:

```bash
git tag v1.0.0
git tag -f v1
git push --tags --force-with-lease
```

Consumers reference:
```yaml
- uses: my-org/dad-jokes-action@v1            # gets latest v1.x
- uses: my-org/dad-jokes-action@v1.0.0        # pinned
- uses: my-org/dad-jokes-action@abc1234       # SHA-pinned (most secure)
```

GitHub's `actions/*` and Marketplace conventions expect `v1`, `v2` floating tags.

## Testing Locally

Use [`act`](https://github.com/nektos/act):

```bash
brew install act
act -W .github/workflows/test.yml --container-architecture linux/amd64
```

For unit testing the action logic, mock `@actions/core` inputs via env vars:

```js
process.env["INPUT_CATEGORY"] = "food";
process.env["INPUT_MAX-LENGTH"] = "100";
require("./src/index.js");
```

(Inputs are exposed to the runtime as `INPUT_<UPPERCASE_NAME>`.)

## Triggering on issue_comment

`.github/workflows/joke.yml`:
```yaml
on:
  issue_comment:
    types: [created]

permissions:
  issues: write

jobs:
  reply:
    if: contains(github.event.comment.body, '/joke')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./           # uses the action defined in this same repo
        with:
          category: food
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

For the action to be usable from `uses: ./`, the workflow needs to first checkout — so the runner has the `action.yml` and `dist/` available.

## Security

- Validate every input — never inject into shell commands.
- Don't echo secrets. Use `core.setSecret()` if you compute one at runtime.
- Pin actions you depend on by SHA when targeting production-critical use.
- Set narrow `permissions:` in consumer workflows.
- For tokens, use `core.getInput("github-token", { required: true })` rather than reading from a hardcoded env var.

## Anti-Patterns

- ❌ Not bundling — `npm install` doesn't happen on the runner.
- ❌ Committing `node_modules/` instead of `dist/` — slow clones, lockfile drift.
- ❌ Using `console.log` for diagnostics — use `core.debug/info/warning`.
- ❌ `core.setFailed` followed by more code that assumes success — `setFailed` doesn't throw.
- ❌ `runs.using: node12` or `node16` — Node 12 and 16 are retired. Use `node20`.
- ❌ Tagging only `v1.0.0` and not `v1` — consumers can't pin to "latest v1".

## Quick Checklist

- [ ] `action.yml` at repo root with `runs.using: node20`
- [ ] `src/index.js` uses `@actions/core` for I/O
- [ ] `npm run build` produces `dist/index.js`
- [ ] `dist/` is committed
- [ ] Tagged `v1.0.0` AND moved `v1` to point to it
- [ ] README shows example usage with `uses:`
- [ ] Tested locally with `act` or via a workflow on a test branch

## References

- Source course: https://github.com/skills/write-javascript-actions
- @actions/toolkit: https://github.com/actions/toolkit
- ncc: https://github.com/vercel/ncc
- act: https://github.com/nektos/act
- Action metadata syntax: https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions
