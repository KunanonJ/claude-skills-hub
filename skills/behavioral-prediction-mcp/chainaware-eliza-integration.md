# Integrating ChainAware AI Agents into ElizaOS

This guide explains how to connect ChainAware's blockchain intelligence tools to your ElizaOS agents, and how to build specialized security agents using ChainAware's sub-agent character files.

**MCP Server URL:** `https://prediction.mcp.chainaware.ai/sse`  
**API keys & pricing:** [chainaware.ai/pricing](https://chainaware.ai/pricing)  
**GitHub:** [github.com/ChainAware/behavioral-prediction-mcp](https://github.com/ChainAware/behavioral-prediction-mcp)

---

## Available Tools

ChainAware exposes 5 MCP tools your Eliza agents can call:

| Tool ID | What it does |
|---|---|
| `predictive_fraud` | AML check + fraud probability score for any wallet (~98% accuracy) |
| `predictive_behaviour` | Predicts next on-chain action, risk profile, and wallet segmentation |
| `predictive_rug_pull` | Scores a liquidity pool or contract for rug pull risk |
| `token_rank_list` | Ranks a list of tokens by quality and risk |
| `token_rank_single` | Deep risk and quality score for a single token |

Supported networks: ETH, BNB, POLYGON, BASE, TON, TRON, HAQQ, SOLANA (varies by tool).

---

## Option A — Raw Tool Access (quickest)

Connect any existing Eliza agent to all 5 ChainAware tools in minutes. The agent's LLM decides which tool to call based on user input.

### Step 1 — Install the MCP plugin

```bash
npm install @fleek-platform/eliza-plugin-mcp
# or
pnpm add @fleek-platform/eliza-plugin-mcp
```

### Step 2 — Add ChainAware to your character file

```json
{
  "name": "YourAgent",
  "plugins": ["@fleek-platform/eliza-plugin-mcp"],
  "settings": {
    "mcp": {
      "servers": {
        "chainaware": {
          "type": "sse",
          "name": "ChainAware Prediction MCP",
          "url": "https://prediction.mcp.chainaware.ai/sse?apiKey=YOUR_API_KEY"
        }
      }
    }
  }
}
```

Replace `YOUR_API_KEY` with your key from [chainaware.ai/pricing](https://chainaware.ai/pricing).

That's it. Your agent can now respond to prompts like:

- *"Is 0x1234... safe to interact with on ETH?"*
- *"What's the rug pull risk on this BNB pool?"*
- *"What will this wallet do next on Solana?"*

---

## Option B — Specialized ChainAware Agents (recommended)

ChainAware provides ready-to-use character files — one per sub-agent — that embed domain-specific reasoning on top of the 5 MCP tools. Instead of a generic agent guessing how to interpret fraud scores, you get agents purpose-built for AML compliance, whale detection, token ranking, and more.

### How it works

Each character file sets a focused `system` prompt that instructs the agent on when and how to call ChainAware tools, how to interpret results, and how to respond. The MCP tools are the same as Option A — the character file adds the intelligence layer.

### Step 1 — Install the plugin

Same as Option A above.

### Step 2 — Pick a character file

Copy the character file for the sub-agent you want from the ChainAware repository into your `characters/` directory. Example for the AML scorer:

```json
{
  "name": "ChainAware-AML-Agent",
  "system": "You are an AML compliance specialist with access to ChainAware's fraud detection and behavioral prediction tools. When given a wallet address: always call predictive_fraud first to get the fraud probability score. If probabilityFraud > 0.7, flag the wallet as high risk and explain the forensic details in plain language. Cross-reference with predictive_behaviour to assess whether the wallet's intentions (trading, staking, bridging) are consistent with its risk profile. Always state the network being analyzed and remind users that scores are predictive, not definitive.",
  "bio": [
    "AML and fraud risk specialist for Web3",
    "Powered by ChainAware's on-chain behavioral prediction models"
  ],
  "plugins": ["@fleek-platform/eliza-plugin-mcp"],
  "settings": {
    "mcp": {
      "servers": {
        "chainaware": {
          "type": "sse",
          "name": "ChainAware Prediction MCP",
          "url": "https://prediction.mcp.chainaware.ai/sse?apiKey=YOUR_API_KEY"
        }
      }
    }
  }
}
```

### Step 3 — Run the agent

```bash
elizaos start --character characters/chainaware-aml-agent.json
```

---

## Ready-to-Use Character Files

29 production-ready character files are available in the `eliza/characters/` directory. Each implements a complete specialist agent with full scoring logic, decision thresholds, and output formats — ready to drop in without modification.

```bash
elizaos start --character eliza/characters/chainaware-fraud-detector.json
```

### Available Characters

| File | Agent | Use Case |
|---|---|---|
| `chainaware-wallet-auditor.json` | Wallet Auditor | Full due diligence — fraud + behaviour + rug pull in one report |
| `chainaware-fraud-detector.json` | Fraud Detector | Fast fraud screening, AML forensics, batch wallet checks |
| `chainaware-aml-scorer.json` | AML Scorer | AML compliance score 0–100; 0 if any forensic flag detected |
| `chainaware-trust-scorer.json` | Trust Scorer | Simple trust score 0.00–1.00 (`1 - fraud_probability`) |
| `chainaware-rug-pull-detector.json` | Rug Pull Detector | Smart contract and LP safety — probabilistic rug pull scoring |
| `chainaware-wallet-marketer.json` | Wallet Marketer | Personalized marketing message (≤20 words) per wallet |
| `chainaware-reputation-scorer.json` | Reputation Scorer | Reputation score 0–1000 using the ChainAware formula |
| `chainaware-wallet-ranker.json` | Wallet Ranker | Global wallet rank by experience, points, and behavioral tier |
| `chainaware-token-ranker.json` | Token Ranker | Discover and rank tokens by holder community strength |
| `chainaware-token-analyzer.json` | Token Analyzer | Single-token deep dive — community rank + top holder quality |
| `chainaware-onboarding-router.json` | Onboarding Router | Route wallets to Beginner / Intermediate / Skip onboarding |
| `chainaware-whale-detector.json` | Whale Detector | Classify wallets: Mega Whale / Whale / Emerging Whale / Not a Whale |
| `chainaware-defi-advisor.json` | DeFi Advisor | Personalized DeFi product recommendations by experience + risk tier |
| `chainaware-airdrop-screener.json` | Airdrop Screener | Batch screen for airdrop eligibility; filter bots; rank by reputation |
| `chainaware-lending-risk-assessor.json` | Lending Risk Assessor | Borrower risk grade A–F, collateral ratio, interest rate tier |
| `chainaware-token-launch-auditor.json` | Token Launch Auditor | Pre-listing audit — Launch Safety Score, APPROVED/CONDITIONAL/REJECTED |
| `chainaware-agent-screener.json` | Agent Screener | AI agent wallet + feeder wallet trust score 0–10 |
| `chainaware-cohort-analyzer.json` | Cohort Analyzer | Segment batches into behavioral cohorts with engagement strategies |
| `chainaware-counterparty-screener.json` | Counterparty Screener | Pre-transaction go/no-go — Safe / Caution / Block |
| `chainaware-governance-screener.json` | Governance Screener | DAO voter Sybil detection and voting weight multiplier |
| `chainaware-transaction-monitor.json` | Transaction Monitor | Real-time transaction risk — ALLOW / FLAG / HOLD / BLOCK |
| `chainaware-lead-scorer.json` | Lead Scorer | Sales lead score 0–100, tier Hot/Warm/Cold/Dead, outreach angle |
| `chainaware-upsell-advisor.json` | Upsell Advisor | Upgrade readiness, next product recommendation, trigger event |
| `chainaware-platform-greeter.json` | Platform Greeter | Contextual welcome message tailored to wallet + platform |
| `chainaware-marketing-director.json` | Marketing Director | Full campaign orchestrator — segmentation, leads, whales, message playbook |
| `chainaware-compliance-screener.json` | Compliance Screener | MiCA-aligned compliance report — PASS / EDD / REJECT (~70–75% coverage) |
| `chainaware-gamefi-screener.json` | GameFi Screener | Web3 game wallet screening — bot detection, P2E reward multiplier |
| `chainaware-portfolio-risk-advisor.json` | Portfolio Risk Advisor | Portfolio rug pull scan — weighted risk score, grade A–F, rebalancing plan |
| `chainaware-rwa-investor-screener.json` | RWA Investor Screener | RWA suitability — QUALIFIED / CONDITIONAL / REFER_TO_KYC / DISQUALIFIED |

---

## Combining ChainAware with Other Plugins

ChainAware tools work alongside any other ElizaOS plugin. For example, pairing with `@elizaos/plugin-twitter` creates an agent that monitors mentions of wallet addresses and automatically runs fraud checks:

```json
{
  "name": "ChainAware-Twitter-Monitor",
  "plugins": [
    "@fleek-platform/eliza-plugin-mcp",
    "@elizaos/plugin-twitter"
  ],
  "settings": {
    "mcp": {
      "servers": {
        "chainaware": {
          "type": "sse",
          "url": "https://prediction.mcp.chainaware.ai/sse?apiKey=YOUR_API_KEY"
        }
      }
    }
  }
}
```

---

## How the MCP Plugin Routes Tool Calls

When a user sends a message, the plugin:

1. Checks which MCP servers are available and lists their tools
2. Uses the LLM to select the most appropriate ChainAware tool
3. Calls the tool with the extracted parameters (wallet address, network)
4. Stores the result in the agent's memory
5. Uses the LLM again to generate a human-readable response

This means your agent handles the tool selection automatically — you don't need to write routing logic.

---

## Environment Variables (recommended approach)

Avoid hardcoding API keys in character files. Use environment variables instead:

```bash
# .env
CHAINAWARE_API_KEY=your_key_here
```

Then reference in your character file or agent bootstrap code:

```json
"url": "https://prediction.mcp.chainaware.ai/sse?apiKey=${CHAINAWARE_API_KEY}"
```

Or pass it via header authentication if your setup supports it:

```json
{
  "type": "sse",
  "url": "https://prediction.mcp.chainaware.ai/sse",
  "headers": {
    "X-API-Key": "${CHAINAWARE_API_KEY}"
  }
}
```

---

## Troubleshooting

**Agent doesn't call ChainAware tools**  
Verify the plugin is listed in `plugins` and the SSE URL includes a valid API key. Check logs for connection errors on startup.

**`403 Unauthorized`**  
Your API key is invalid or missing. Check [chainaware.ai/pricing](https://chainaware.ai/pricing) to confirm your subscription is active.

**`400 Bad Request`**  
The wallet address or network string is malformed. Supported network values: `ETH`, `BNB`, `POLYGON`, `BASE`, `TON`, `TRON`, `HAQQ`, `SOLANA` (not all tools support all networks — check the tool description).

**Tool selected but returns empty result**  
The address may be unrecognized or too new. The API returns `"New Address"` status for wallets with insufficient on-chain history.

---

## Get Access

API keys are available via subscription at [chainaware.ai/pricing](https://chainaware.ai/pricing).  
For enterprise integration or custom plans, contact the ChainAware team at [chainaware.ai](https://chainaware.ai).
