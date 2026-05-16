---
name: github-models-in-actions
description: "Run LLM inference inside GitHub Actions workflows using GitHub Models — automate issue triage, PR summaries, release notes, and AI-powered code review. Covers the `actions/ai-inference` action, structured outputs with Zod, and building custom AI-powered actions. Trigger when the user wants AI in their workflow, automated issue analysis, GitHub Models, free LLM access in GHA, or `models: read` permission. Sourced from github.com/skills/ai-in-actions + create-ai-powered-actions."
---

# GitHub Models in GitHub Actions

GitHub Models gives every repo free, rate-limited LLM inference (GPT-4o, Claude, Llama, Phi, more). It works inside GHA workflows with a single permission — no API keys, no billing setup.

## When to Use

- Auto-classify and label new issues by content
- Summarize long PR diffs into release-note bullets
- Tag duplicates against an existing issue corpus
- Translate user-facing strings
- Generate test data based on schemas
- Reply to common questions in issue threads

When **not** to use: heavy production traffic (rate limits apply), latency-sensitive paths (inference is seconds, not ms), high-stakes decisions where a hallucination would hurt.

## Permissions

```yaml
permissions:
  models: read         # required for GitHub Models inference
  contents: read
  issues: write        # if posting back to issues
  pull-requests: write # if posting back to PRs
```

`models: read` is opt-in per-workflow; without it the API returns 403.

## Approach 1: actions/ai-inference (Drop-in)

Easiest path. No code to write.

```yaml
name: Triage new issue

on:
  issues:
    types: [opened]

permissions:
  models: read
  issues: write

jobs:
  classify:
    runs-on: ubuntu-latest
    steps:
      - id: ai
        uses: actions/ai-inference@v1
        with:
          model: openai/gpt-4o-mini
          prompt: |
            Classify this issue into exactly one of:
            bug, feature, question, docs, duplicate, invalid.
            Return only the label, no punctuation.

            Title: ${{ github.event.issue.title }}
            Body: ${{ github.event.issue.body }}

      - run: gh issue edit ${{ github.event.issue.number }} --add-label "${{ steps.ai.outputs.response }}"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Models you can use (in `openai/<name>` namespace): `gpt-4o`, `gpt-4o-mini`, `o1-preview`. Also: `anthropic/claude-3-5-sonnet`, `meta/llama-3-70b-instruct`, `microsoft/phi-3-medium-128k-instruct`. Full list: https://github.com/marketplace?type=models

## Approach 2: Structured Outputs with Zod (Custom Action)

When you need machine-parseable JSON, not free text. Use the OpenAI SDK against the GitHub Models endpoint.

```js
// src/index.js
const core = require("@actions/core");
const github = require("@actions/github");
const OpenAI = require("openai");
const { z } = require("zod");
const { zodResponseFormat } = require("openai/helpers/zod");

const Analysis = z.object({
  label: z.enum(["bug", "feature", "question", "docs", "duplicate", "invalid"]),
  severity: z.enum(["low", "medium", "high", "critical"]),
  reasoning: z.string().max(280)
});

async function run() {
  const issue = github.context.payload.issue;
  const client = new OpenAI({
    baseURL: "https://models.inference.ai.azure.com",
    apiKey: process.env.GITHUB_TOKEN
  });

  const completion = await client.beta.chat.completions.parse({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "You triage GitHub issues precisely." },
      { role: "user", content: `Title: ${issue.title}\n\nBody: ${issue.body}` }
    ],
    response_format: zodResponseFormat(Analysis, "analysis")
  });

  const result = completion.choices[0].message.parsed;
  core.setOutput("label", result.label);
  core.setOutput("severity", result.severity);
  core.setOutput("reasoning", result.reasoning);
}

run().catch(err => core.setFailed(err.message));
```

`action.yml`:
```yaml
name: AI Issue Triage
runs: { using: "node20", main: "dist/index.js" }
outputs:
  label: { description: "Classification label" }
  severity: { description: "Estimated severity" }
  reasoning: { description: "Why this label/severity" }
```

The endpoint `https://models.inference.ai.azure.com` is the GitHub Models gateway. The OpenAI SDK works against it because the API is OpenAI-compatible. Auth is via the `GITHUB_TOKEN` from the workflow.

## Combining With Other Actions

Triage → label → comment → assign:

```yaml
jobs:
  smart-triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - id: analyze
        uses: ./.github/actions/ai-triage
      - run: gh issue edit ${{ github.event.issue.number }} --add-label "${{ steps.analyze.outputs.label }}"
      - if: steps.analyze.outputs.severity == 'critical'
        run: gh issue edit ${{ github.event.issue.number }} --add-assignee on-call-rotation
      - uses: peter-evans/create-or-update-comment@v4
        with:
          issue-number: ${{ github.event.issue.number }}
          body: |
            🤖 Auto-triage: **${{ steps.analyze.outputs.label }}** (severity: ${{ steps.analyze.outputs.severity }})
            ${{ steps.analyze.outputs.reasoning }}
```

## Patterns

### PR diff summary
```yaml
- run: git diff origin/main...HEAD > /tmp/diff.patch
- uses: actions/ai-inference@v1
  id: summary
  with:
    model: openai/gpt-4o
    prompt-file: /tmp/diff.patch
    system-prompt: "Summarize this diff in 3 bullets. Focus on user-visible behavior changes."
```

### Duplicate detection
1. Fetch all open issues with `gh issue list --json title,body,number`
2. Pass the new issue + the list to the model
3. Ask: "is this a duplicate of any of these? Reply with the issue number or NONE"

### Release notes from commits
```yaml
- run: git log --pretty="%h %s" $LAST_TAG..HEAD > /tmp/commits.txt
- uses: actions/ai-inference@v1
  id: notes
  with:
    model: openai/gpt-4o
    prompt-file: /tmp/commits.txt
    system-prompt: "Group these commits into Features / Fixes / Internal sections. Use markdown."
```

## Limits

- Rate limited per-repo (free tier is generous; specifics on GitHub's billing page).
- Max context: model-dependent. `gpt-4o-mini` is 128k tokens.
- No persistent memory — each call is stateless.
- Cannot fine-tune via this endpoint. For production, move to the actual provider API with billing.

## Anti-Patterns

- ❌ Using AI inference for a hard rule that regex would solve. ("Is this a bug?" → no; "Does the title contain 'crash'?" → yes.)
- ❌ Trusting unstructured output to drive destructive actions (closing issues, force-pushing). Use structured outputs + sanity checks.
- ❌ Putting secrets in the prompt body — they show in logs.
- ❌ Skipping `permissions.models: read` and wondering why every call 403s.
- ❌ Running on every commit when issue/PR events would be cheaper.

## References

- Source courses: https://github.com/skills/ai-in-actions, https://github.com/skills/create-ai-powered-actions
- actions/ai-inference: https://github.com/actions/ai-inference
- GitHub Models marketplace: https://github.com/marketplace?type=models
- OpenAI SDK structured outputs: https://platform.openai.com/docs/guides/structured-outputs
