# OpenAI Skill Registry — Submission Guide

This document covers how to submit the **ChainAware Behavioral Prediction MCP**
to the OpenAI skill registry (Codex / ChatGPT Connectors).

---

## Prerequisites

Before submitting, confirm you have:

- [ ] An OpenAI developer account with access to the skill registry
- [ ] The MCP server publicly reachable at `https://prediction.mcp.chainaware.ai/sse`
- [ ] A valid `CHAINAWARE_API_KEY`
- [ ] All files below present and up to date (see Pre-Submission Checklist)

---

## Pre-Submission Checklist

Run through these before uploading anything:

### Files
- [ ] `agents/openai.yaml` — skill definition (capabilities, subagents, dependencies, metadata)
- [ ] `assets/logo-small.png` — 64×64 px square PNG
- [ ] `assets/logo-large.png` — 512×512 px square PNG
- [ ] `SKILL.md` — full skill documentation (used by Claude / ClawHub; useful reference for registry description)
- [ ] `README.md` — public-facing repo documentation

### Content
- [ ] `openai.yaml` → `interface.display_name` is correct
- [ ] `openai.yaml` → `interface.short_description` is under 150 characters
- [ ] `openai.yaml` → `interface.icon_small` and `icon_large` paths match actual files
- [ ] `openai.yaml` → all 6 capabilities listed (`predictive_fraud`, `predictive_behaviour`, `predictive_rug_pull`, `credit_score`, `token_rank_list`, `token_rank_single`)
- [ ] `openai.yaml` → all 32 subagents listed
- [ ] `openai.yaml` → `dependencies.tools[].url` is the live MCP endpoint
- [ ] MCP endpoint responds — test with: `curl -I https://prediction.mcp.chainaware.ai/sse`

---

## Submission Steps

### Option A — OpenAI Developer Portal (recommended)

1. Go to [platform.openai.com](https://platform.openai.com) and sign in
2. Navigate to **Explore** → **Skills** (or **Connectors** depending on your account tier)
3. Click **Submit a Skill** / **Add Connector**
4. Fill in the form:
   - **Name:** `ChainAware Behavioral Prediction`
   - **Description:** paste `interface.short_description` from `openai.yaml`
   - **MCP URL:** `https://prediction.mcp.chainaware.ai/sse`
   - **Auth:** API Key — header `X-API-Key`
   - **Icon:** upload `assets/logo-large.png`
5. Upload or paste `agents/openai.yaml` when prompted for the skill definition
6. Submit for review

### Option B — Codex CLI (if available on your account)

```bash
# Authenticate
openai login

# Submit skill
openai skills submit \
  --file agents/openai.yaml \
  --name "chainaware-behavioral-prediction" \
  --version 1.2.0
```

### Option C — GitHub-linked registry

Some OpenAI registry tiers accept a public GitHub repository directly:

1. Push this repo to `https://github.com/ChainAware/behavioral-prediction-mcp`
2. In the portal, select **Import from GitHub**
3. Point to the repo root — the registry will auto-detect `agents/openai.yaml`

---

## Key Fields from `openai.yaml`

| Field | Value |
|-------|-------|
| `display_name` | ChainAware Behavioral Prediction |
| `short_description` | AI-powered fraud detection, wallet behavior analysis, rug pull prediction, and token ranking for Web3 — across 8 blockchains, 14M+ wallets. |
| `brand_color` | `#0066FF` |
| `MCP endpoint` | `https://prediction.mcp.chainaware.ai/sse` |
| `auth type` | API Key (`X-API-Key` header) |
| `capabilities` | 6 tools |
| `subagents` | 32 specialist agents |

---

## After Submission

- **Review time:** typically 1–5 business days
- **Test:** once approved, test from a fresh ChatGPT or Codex session:
  ```
  "Analyze wallet 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 for fraud on ETH"
  ```
- **Monitor:** check the registry dashboard for usage stats and error reports

---

## Updating the Skill

When tools or subagents are added:

1. Update `agents/openai.yaml` (capabilities, subagents)
2. Bump the version in `openai.yaml` metadata (if versioned)
3. Re-submit via the portal or CLI:
   ```bash
   openai skills update \
     --file agents/openai.yaml \
     --name "chainaware-behavioral-prediction" \
     --version 1.3.0
   ```

---

## Useful Links

- OpenAI Developer Portal: https://platform.openai.com
- MCP Specification: https://github.com/modelcontextprotocol/spec
- ChainAware GitHub: https://github.com/ChainAware/behavioral-prediction-mcp
- ChainAware Pricing / API Key: https://chainaware.ai/pricing
- ChainAware Privacy Policy: https://chainaware.ai/privacy
