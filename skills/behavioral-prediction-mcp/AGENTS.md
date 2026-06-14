# ChainAware Subagent Index

Machine-readable index of all 32 Claude Code subagents in `.claude/agents/`.
Each agent is a specialist that handles a specific Web3 intelligence task using the
ChainAware Behavioral Prediction MCP (`https://prediction.mcp.chainaware.ai/sse`).

**Quick setup:**
```bash
claude mcp add --transport sse chainaware-behavioral-prediction \
  https://prediction.mcp.chainaware.ai/sse --header "X-API-Key: YOUR_KEY"
export CHAINAWARE_API_KEY="your-key-here"
```

---

## Agent Directory

### chainaware-wallet-auditor
**File:** `.claude/agents/chainaware-wallet-auditor.md`
**Model:** claude-sonnet-4-6
**Tools:** `predictive_behaviour`
**Purpose:** Full due diligence. Deep behavioural analysis of a wallet including fraud signals, intent, experience, and recommendations.
**Triggers:** "full audit of 0x...", "due diligence on this wallet", "complete analysis", "deep dive on this address"
**Input:** wallet address + network
**Output:** Behaviour profile, fraud signals, experience score, intent, recommendations

---

### chainaware-fraud-detector
**File:** `.claude/agents/chainaware-fraud-detector.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`
**Purpose:** Fast wallet fraud screening. Returns fraud status, probability, and forensic AML flags.
**Triggers:** "is this wallet safe?", "fraud check on 0x...", "AML screen", "is this address suspicious?", "check before I transact"
**Input:** wallet address + network
**Output:** Status (Fraud / Not Fraud / New Address), probabilityFraud (0–1), forensic flags

---

### chainaware-rug-pull-detector
**File:** `.claude/agents/chainaware-rug-pull-detector.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_rug_pull`, `predictive_fraud`
**Purpose:** Smart contract and LP safety checks before depositing funds.
**Triggers:** "will this pool rug pull?", "is this contract safe?", "check this LP", "rug pull risk", "should I ape in?"
**Input:** smart contract or LP address + network (ETH, BNB, BASE, HAQQ)
**Output:** Rug pull probability, risk tier, deployer risk, forensic breakdown, recommendation

---

### chainaware-wallet-marketer
**File:** `.claude/agents/chainaware-wallet-marketer.md`
**Model:** claude-sonnet-4-6
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Generates a hyper-personalised marketing message (≤20 words) calibrated to the wallet's behaviour profile.
**Triggers:** "write a message for this wallet", "personalise outreach for 0x...", "convert this user", "marketing for this address"
**Input:** wallet address + network
**Output:** One personalised message (≤20 words) + rationale

---

### chainaware-reputation-scorer
**File:** `.claude/agents/chainaware-reputation-scorer.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`
**Purpose:** Calculates a numeric reputation score using the ChainAware formula.
**Formula:** `(1000 / 110) × (experience + 1) × (riskCapability + 1) × (1 - probabilityFraud)` — max score = 1000; `experience` (0–10) and `riskCapability` (0–9) are direct fields from `predictive_behaviour`
**Triggers:** "reputation score for 0x...", "score this wallet", "rank these wallets", "which wallet is better?"
**Input:** wallet address + network
**Output:** Reputation score (0–1000), band label, component breakdown

---

### chainaware-aml-scorer
**File:** `.claude/agents/chainaware-aml-scorer.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`
**Purpose:** AML compliance scoring for KYC, regulatory, and exchange onboarding workflows.
**Formula:** `(1 - probabilityFraud) × 100` — returns 0 if any forensic flag is present
**Triggers:** "AML score for 0x...", "is this wallet AML compliant?", "KYC screening", "compliance check", "run AML check"
**Input:** wallet address + network
**Output:** AML score (0–100), pass/fail verdict, forensic flag breakdown

---

### chainaware-trust-scorer
**File:** `.claude/agents/chainaware-trust-scorer.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`
**Purpose:** Returns a simple trust score as `1 - fraud_probability`.
**Triggers:** "trust score for 0x...", "how much do I trust this wallet?", "trustworthiness rating", "confidence score"
**Input:** wallet address + network
**Output:** Trust score (0.00–1.00)

---

### chainaware-wallet-ranker
**File:** `.claude/agents/chainaware-wallet-ranker.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`
**Purpose:** Returns a wallet's global experience rank and leaderboard position.
**Triggers:** "what is the rank of 0x...", "rank this wallet", "how good is this wallet?", "global rank", "wallet leaderboard"
**Input:** wallet address + network
**Output:** Experience score (0–10), global rank, experience tier, wallet age, transaction count

---

### chainaware-token-ranker
**File:** `.claude/agents/chainaware-token-ranker.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `token_rank_list`
**Purpose:** Discovers and ranks tokens by the strength of their holder community.
**Triggers:** "top AI tokens", "best DeFi tokens on ETH", "rank tokens by community", "strongest holder base", "token leaderboard"
**Input:** network + optional category (AI Token, RWA Token, DeFi Token, DeFAI Token, DePIN Token) + sort preference
**Output:** Ranked token list with community rank, normalised rank, holder count, chain, category

---

### chainaware-token-analyzer
**File:** `.claude/agents/chainaware-token-analyzer.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `token_rank_single`, `predictive_fraud`
**Purpose:** Deep-dive into a single token: community rank, top holders, global wallet rank, and holder fraud screening.
**Triggers:** "who holds this token?", "token rank for 0x...", "best holders of this contract", "holder analysis", "is this token held by whales?"
**Input:** contract address + network
**Output:** Token community rank, top holders with global rank, fraud screening on top holders

---

### chainaware-onboarding-router
**File:** `.claude/agents/chainaware-onboarding-router.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Routes wallets to the correct onboarding flow based on on-chain experience level.
**Triggers:** "which onboarding flow for 0x...", "is this user a beginner?", "skip onboarding for this wallet?", "route this wallet", "first-time user check"
**Input:** wallet address + network
**Output:** Onboarding route (Beginner / Intermediate / Power User / Skip), rationale, recommended first steps

---

### chainaware-whale-detector
**File:** `.claude/agents/chainaware-whale-detector.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Classifies wallets into whale tiers for VIP treatment, fee discounts, and governance weighting.
**Triggers:** "is this a whale?", "VIP wallet", "whale tier", "find whales", "classify this wallet", "high-value wallet check"
**Input:** wallet address + network (supports batch)
**Output:** Tier (Mega Whale / Whale / Emerging Whale / Not a Whale), domain (DeFi / NFT / Trading / Yield), status (Active / Dormant), recommended treatment

---

### chainaware-defi-advisor
**File:** `.claude/agents/chainaware-defi-advisor.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Returns personalised DeFi product recommendations calibrated to the wallet's experience and risk appetite.
**Triggers:** "what DeFi products suit this wallet?", "which yield strategy for 0x...", "best DeFi products for this wallet", "personalise DeFi recommendations"
**Input:** wallet address + network
**Output:** Recommended product tier, specific DeFi products, rationale based on experience + risk profile

---

### chainaware-airdrop-screener
**File:** `.claude/agents/chainaware-airdrop-screener.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`, `predictive_behaviour`
**Purpose:** Batch screens wallets for airdrop eligibility; filters bots and fraud; ranks eligible wallets by reputation score.
**Triggers:** "screen these wallets for our airdrop", "filter bots from this list", "sybil filter for airdrop", "fair airdrop allocation", "remove fake wallets"
**Input:** list of wallet addresses + network. Optional: fraud threshold, token budget
**Output:** Eligible ranked list, flagged list, disqualified list, token allocations, cohort breakdown

---

### chainaware-lending-risk-assessor
**File:** `.claude/agents/chainaware-lending-risk-assessor.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`, `predictive_behaviour`, `credit_score` (ETH only)
**Purpose:** Assesses borrower risk for DeFi lending protocols. Returns risk grade, collateral ratio, and interest rate tier.
**Triggers:** "what collateral should I require from 0x...", "lending risk for this address", "what LTV for this wallet?", "assess this borrower", "should I lend to this wallet?"
**Input:** wallet address + network. Optional: loan amount, asset type, platform risk policy
**Output:** Risk grade (A–F), recommended collateral ratio (%), interest rate tier, risk breakdown

---

### chainaware-token-launch-auditor
**File:** `.claude/agents/chainaware-token-launch-auditor.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_rug_pull`, `predictive_fraud`, `predictive_behaviour`
**Purpose:** Pre-listing launch safety audit combining contract rug pull risk and deployer wallet screening.
**Triggers:** "should we list this token?", "audit this launch", "is this deployer trustworthy?", "vet this IDO", "launch safety check", "pre-listing safety check"
**Input:** token contract address + deployer wallet address + network
**Output:** Launch Safety Score, verdict (APPROVED / CONDITIONAL / REJECTED), safety badge, listing conditions

---

### chainaware-agent-screener
**File:** `.claude/agents/chainaware-agent-screener.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`, `predictive_behaviour`
**Purpose:** Screens an AI agent's operational wallet and feeder wallet for trustworthiness.
**Formula:** Agent Trust Score 0–10 (0=fraud, 1=new/insufficient data, 2–10=normalised reputation)
**Triggers:** "is this agent wallet safe?", "screen this agent", "check the feeder wallet for this agent", "can I trust this agent?", "agent trust score for 0x..."
**Input:** agent wallet address + feeder wallet address + network
**Output:** Agent Trust Score (0–10), per-wallet fraud verdict, overall recommendation

---

### chainaware-cohort-analyzer
**File:** `.claude/agents/chainaware-cohort-analyzer.md`
**Model:** claude-sonnet-4-6
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Segments a batch of wallets into behavioural cohorts with per-cohort engagement strategies.
**Cohorts:** Power DeFi User, NFT Collector, Yield Farmer, Multi-Chain Explorer, Active Trader, Casual User, Dormant/Inactive, New/Fresh, Unclassified, Excluded (fraud/bot)
**Triggers:** "segment these wallets", "who are my power users?", "cohort analysis for these addresses", "what types of users do I have?", "behavioral mix of my community"
**Input:** list of wallet addresses + network. Optional: engagement goal, custom cohort labels
**Output:** Cohort distribution table, wallet-level detail, per-cohort engagement playbook, audience quality score

---

### chainaware-counterparty-screener
**File:** `.claude/agents/chainaware-counterparty-screener.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`, `predictive_behaviour`
**Purpose:** Real-time pre-transaction safety check. Returns a go/no-go verdict before a trade, transfer, or contract interaction.
**Verdicts:** 🟢 Safe / 🟡 Caution / 🔴 Block
**Triggers:** "is it safe to send to this address?", "check this counterparty", "pre-transaction check", "quick safety check on 0x...", "should I trade with this wallet?"
**Input:** counterparty wallet address + network. Optional: transaction type (transfer / trade / contract / LP deposit)
**Output:** Verdict (Safe / Caution / Block), one-line reason, key signals, recommended action

---

### chainaware-platform-greeter
**File:** `.claude/agents/chainaware-platform-greeter.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Generates a personalised welcome message for a specific wallet when it connects to a specific platform. The same wallet gets a different message on Aave vs 1inch vs OpenSea — platform context + wallet behaviour = hyper-relevant in-app copy.
**Platform types supported:** DEX/Swap, Lending/Borrowing, Yield/Staking, Bridge, NFT, Derivatives/Perps, Portfolio/Analytics, Launchpad, Governance/DAO, Unknown/Custom
**Triggers:** "what should we show 0x... when they connect to Aave?", "welcome message for this wallet on 1inch", "personalised greeting on our dapp", "in-app message when this user lands", "contextual welcome for 0x... on [platform]", "personalise the landing experience for this wallet"
**Input:** wallet address + network + platform name. Optional: platform type, feature to highlight, tone (friendly / professional / bold)
**Output:** Personalised welcome message (max 2 sentences, max 35 words) + rationale + alternate versions. Batch mode produces a message per wallet for platform launches or feature rollouts.

---

### chainaware-upsell-advisor
**File:** `.claude/agents/chainaware-upsell-advisor.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Identifies the best upsell opportunity for an existing user. Scores upgrade readiness (0–100), recommends the specific next product, calculates conversion probability, identifies the optimal trigger event, and generates a ready-to-use upsell message.
**Triggers:** "what should I upsell to 0x...", "next product for this user", "is this wallet ready to upgrade?", "upgrade path for this wallet", "when should I offer the next tier?", "best upsell for this wallet", "next-best-product for 0x...", "upgrade readiness check"
**Input:** wallet address + network + current product/tier. Optional: product catalogue, upsell goal (revenue / engagement / retention)
**Output:** Upgrade readiness score (0–100), conversion probability, recommended next product, trigger event, ready-to-use upsell message, "what NOT to do" warning. Batch mode ranks full user lists by upsell readiness.

---

### chainaware-lead-scorer
**File:** `.claude/agents/chainaware-lead-scorer.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Sales lead qualification engine. Scores a wallet 0–100 as a conversion prospect, assigns a lead tier, estimates conversion probability, and recommends a specific outreach angle.
**Tiers:** 🔥 Hot (75–100) / 🟡 Warm (50–74) / 🔵 Cold (25–49) / ⚫ Dead (0–24 or disqualified)
**Triggers:** "is this a good lead?", "score this wallet as a prospect", "lead quality for this address", "which wallets are worth pursuing?", "hot leads in this list", "sales qualification for this address", "conversion potential for 0x...", "rank these wallets by sales potential"
**Input:** wallet address + network. Optional: product context, outreach goal (acquisition / upsell / reactivation), batch list
**Output:** Lead score (0–100), tier, conversion probability, outreach angle, channel fit, timing signal, batch ranked list

---

### chainaware-transaction-monitor
**File:** `.claude/agents/chainaware-transaction-monitor.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`, `predictive_rug_pull`, `predictive_behaviour`
**Purpose:** Real-time transaction risk scoring for autonomous AI agents and automated pipelines. Screens sender, receiver, and contract; returns a composite risk score (0–100) and a machine-actionable pipeline action.
**Actions:** ✅ ALLOW / ⚠️ FLAG / 🔶 HOLD / 🛑 BLOCK
**Triggers:** "should my agent execute this transaction?", "risk score for this tx", "monitor this transaction", "flag or allow this transfer?", "pipeline risk signal for this event", "autonomous transaction screening", "compliance check for this transaction"
**Input:** sender address + receiver address + network. Optional: contract address, transaction value, action type (transfer / swap / stake / bridge / mint / approve / liquidity)
**Output:** Composite risk score (0–100), per-address risk levels, pipeline action, operator note. Compact mode available for programmatic consumption.

---

### chainaware-governance-screener
**File:** `.claude/agents/chainaware-governance-screener.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** DAO voter screening — Sybil detection, governance tier classification, and voting weight multiplier calculation.
**Tiers:** Core Contributor (2×) / Active Member (1.5×) / Participant (1×) / Observer (0.5×) / Disqualified (0×)
**Governance models supported:** Token-weighted, reputation-weighted, quadratic
**Triggers:** "should this wallet be allowed to vote?", "voting weight for 0x...", "screen our DAO members", "Sybil check for governance", "filter fake voters", "governance health check"
**Input:** wallet address (or list) + network. Optional: governance model, voting power pool, participation threshold
**Output:** Governance tier, voting weight multiplier, Sybil risk verdict, batch leaderboard, governance health score

---

### chainaware-sybil-detector
**File:** `.claude/agents/chainaware-sybil-detector.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Bulk Sybil attack detection for DAO governance votes — screens a voter list for coordinated fraud, wallet farms, and low-quality participation. Classifies each wallet as ELIGIBLE / REVIEW / EXCLUDE, detects cross-wallet Sybil patterns (cluster, fraud concentration, new-wallet surge, uniform risk profile), and produces reputation-weighted vote multipliers.
**Triggers:** "screen these wallets for governance", "are these voters legitimate?", "detect Sybil attackers in this vote", "rank these voters by quality", "which wallets should be excluded from this proposal?", "run Sybil detection on this voter list"
**Input:** list of wallet addresses + network. Optional: minimum reputation threshold, custom fraud/experience thresholds, proposal context
**Output:** ELIGIBLE / REVIEW / EXCLUDE classification per wallet, Sybil pattern flags, overall risk rating (LOW / MEDIUM / HIGH / CRITICAL), recommendation (PROCEED / PROCEED WITH CAUTION / HALT AND INVESTIGATE), reputation-weighted vote multipliers

---

### chainaware-marketing-director
**File:** `.claude/agents/chainaware-marketing-director.md`
**Model:** claude-sonnet-4-6
**Tools:** `Agent` (orchestrator), `predictive_fraud`
**Purpose:** Full-cycle campaign orchestrator. Takes wallet list + platform description + campaign goal and delegates to specialist subagents to produce a complete Marketing Campaign Brief: segmented audience, prioritised leads, whale roster, per-cohort message playbook, upsell opportunities, and onboarding routes.
**Triggers:** "plan a campaign for these wallets", "marketing brief for our platform", "how do we engage these users?", "full marketing strategy for this address list", "who should we target and what should we say?", "build me a campaign"
**Input:** wallet address(es) + network + platform description. Optional: campaign goal (acquisition / retention / monetization / re-engagement), current product/tier
**Output:** Marketing Campaign Brief — cohort breakdown, lead tier list, whale roster, per-cohort message playbook, upsell targets, onboarding routes

---

### chainaware-compliance-screener
**File:** `.claude/agents/chainaware-compliance-screener.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `Agent` (orchestrator), `predictive_fraud`
**Purpose:** First-layer MiCA-aligned compliance screening. Orchestrates fraud-detector, aml-scorer, transaction-monitor, and counterparty-screener into a structured Compliance Report with verdict (PASS / ENHANCED DUE DILIGENCE / REJECT) and explicit scope disclaimer (~70–75% MiCA coverage for pure DeFi).
**Triggers:** "is this wallet compliant?", "compliance check for 0x...", "should we onboard this wallet?", "AML screening for this address", "MiCA screening for these wallets", "flag this wallet for EDD", "onboarding compliance batch"
**Input:** wallet address(es) + network. Optional: counterparty address, transaction value, transaction type (onboarding / transaction / batch)
**Output:** Compliance Report — verdict (PASS / EDD / REJECT), risk rating, per-check results, scope disclaimer

---

### chainaware-gamefi-screener
**File:** `.claude/agents/chainaware-gamefi-screener.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`, `predictive_behaviour`
**Purpose:** Web3 game and P2E wallet screening. Detects bot farms, multi-account cheaters, and reward abusers; classifies legitimate players into experience tiers for matchmaking; calculates P2E reward eligibility.
**Triggers:** "is this wallet a real player or a bot?", "P2E eligibility for 0x...", "bot detection for my game", "what matchmaking tier for this wallet?", "is this a farm wallet?", "detect cheaters in my P2E platform", "reward eligibility for this address"
**Input:** wallet address + network. Optional: game name/type, P2E reward cap per tier, minimum legitimacy score threshold
**Output:** Player verdict (ALLOW / FLAG / BLOCK), legitimacy score, experience tier, P2E reward eligibility and multiplier, matchmaking bracket

---

### chainaware-portfolio-risk-advisor
**File:** `.claude/agents/chainaware-portfolio-risk-advisor.md`
**Model:** claude-sonnet-4-6
**Tools:** `predictive_rug_pull`, `token_rank_single`
**Purpose:** Portfolio-level rug pull and community health assessment. Scans every token via `predictive_rug_pull`, enriches with `token_rank_single` where available, produces a weighted Portfolio Risk Score, grade (A–F), concentration flags, and prioritised rebalancing plan.
**Triggers:** "how risky is my portfolio?", "check these tokens for rug pulls", "which of my positions are dangerous?", "portfolio rug pull scan", "which tokens should I exit?", "rebalancing recommendations based on risk", "are any of my tokens about to rug?"
**Input:** list of token contract addresses + networks. Optional: position sizes or USD values (for weighted scoring), risk tolerance (conservative / standard / aggressive)
**Output:** Portfolio Risk Score, grade (A–F), per-token risk table, concentration flags, prioritised rebalancing plan

---

### chainaware-rwa-investor-screener
**File:** `.claude/agents/chainaware-rwa-investor-screener.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_fraud`, `predictive_behaviour`
**Purpose:** RWA investor suitability screening. Assesses AML compliance, fraud risk, on-chain experience (proxy for investor sophistication), and risk profile alignment against the RWA's declared risk tier. Distinct from `compliance-screener` (MiCA/AML) — this is about investor suitability and experience matching.
**Triggers:** "is this wallet suitable for our RWA?", "RWA suitability check for 0x...", "can this wallet invest in tokenized real estate?", "investor qualification for our tokenized fund", "whitelist these wallets for our RWA pre-sale", "is this wallet accredited enough?", "batch screen investors for our token round"
**Input:** wallet address + network. Optional: RWA risk tier (conservative / moderate / aggressive), investment cap policy
**Output:** Suitability Tier (QUALIFIED / CONDITIONAL / REFER_TO_KYC / DISQUALIFIED), Suitability Score (0–100), recommended investment cap, investor profile, risk flags

---

### chainaware-credit-scorer
**File:** `.claude/agents/chainaware-credit-scorer.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `credit_score`
**Purpose:** Returns a crypto credit score (1–9) for any wallet combining fraud probability and social graph analysis. Fast, single-number creditworthiness signal for lending and trust decisions.
**Triggers:** "what is the credit score for 0x...", "credit score for this wallet", "is this wallet a good borrower?", "creditworthiness of this address", "rate this wallet for credit", "calculate credit score"
**Input:** wallet address + network (ETH only)
**Output:** Credit score (1–9), tier label (Prime / Reliable / Moderate / High Risk / Very High Risk)

---

### chainaware-ltv-estimator
**File:** `.claude/agents/chainaware-ltv-estimator.md`
**Model:** claude-haiku-4-5-20251001
**Tools:** `predictive_behaviour`, `predictive_fraud`
**Purpose:** Estimates 12-month lifetime value (LTV) as a USD revenue range. Models projected transaction count, average transaction value on the platform, and the platform's fee rate — scaled by category breadth, risk profile, and fraud-based retention. Hard rejects fraudulent wallets ($0).
**Formula:** `(annual_tx × Intent_Multiplier) × (balance × platform_share) × fee_rate × Category_Multiplier × Risk_Multiplier × Retention_Factor` ±25%
**Triggers:** "what is the LTV of 0x...", "revenue potential for this wallet", "12-month revenue estimate", "estimate lifetime value for this address", "rank these wallets by revenue potential", "prioritize wallets by LTV"
**Input:** wallet address + network. Optional: platform_share (default 0.15), fee_rate (default 0.001)
**Output:** USD revenue range (Low–High), LTV tier (Dormant / Low / Medium / High / Very High), full calculation breakdown

---

## Network Support Matrix

| Tool | ETH | BNB | POLYGON | TON | BASE | TRON | HAQQ | SOLANA |
|------|-----|-----|---------|-----|------|------|------|--------|
| `predictive_fraud` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| `predictive_behaviour` | ✅ | ✅ | — | — | ✅ | — | ✅ | ✅ |
| `predictive_rug_pull` | ✅ | ✅ | — | — | ✅ | — | ✅ | — |
| `credit_score` | ✅ | — | — | — | — | — | — | — |
| `token_rank_list` | ✅ | ✅ | — | — | ✅ | — | — | ✅ |
| `token_rank_single` | ✅ | ✅ | — | — | ✅ | — | — | ✅ |

## Composability Map

```
Autonomous transaction pipeline  → chainaware-transaction-monitor
Transaction safety check         → chainaware-counterparty-screener
  └─ needs more detail       → chainaware-wallet-auditor
  └─ is a contract address   → chainaware-rug-pull-detector

User onboarding              → chainaware-onboarding-router
  └─ personalise DeFi offer  → chainaware-defi-advisor
  └─ personalise message     → chainaware-wallet-marketer

Airdrop campaign             → chainaware-airdrop-screener
  └─ whale tier bonuses      → chainaware-whale-detector
  └─ message each recipient  → chainaware-wallet-marketer

DAO governance vote          → chainaware-governance-screener
  └─ full member audit       → chainaware-wallet-auditor
  └─ AML on flagged wallets  → chainaware-aml-scorer

DeFi lending                 → chainaware-lending-risk-assessor
  └─ full borrower profile   → chainaware-wallet-auditor

Token / launchpad vetting    → chainaware-token-launch-auditor
  └─ token holder quality    → chainaware-token-analyzer
  └─ deployer deep dive      → chainaware-wallet-auditor

User analytics               → chainaware-cohort-analyzer
  └─ per-cohort messaging    → chainaware-wallet-marketer
  └─ onboard new cohort      → chainaware-onboarding-router

AI agent verification        → chainaware-agent-screener
  └─ full agent audit        → chainaware-wallet-auditor
```

## Further Reading

- Full documentation: https://github.com/ChainAware/behavioral-prediction-mcp
- Wallet Auditor Guide: https://chainaware.ai/blog/chainaware-wallet-auditor-how-to-use/
- MCP integration guide: https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/
- 12 agent capabilities: https://chainaware.ai/blog/12-blockchain-capabilities-any-ai-agent-can-use-mcp-integration-guide/
- Complete product guide: https://chainaware.ai/blog/chainaware-ai-products-complete-guide/
- API access: https://chainaware.ai/pricing
