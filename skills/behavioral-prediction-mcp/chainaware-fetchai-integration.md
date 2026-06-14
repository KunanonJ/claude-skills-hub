# Integrating ChainAware AI Agents into Fetch.ai / Agentverse

This guide explains how to connect ChainAware's blockchain intelligence tools to the Fetch.ai ecosystem — both as a simple outbound call from any existing uAgent, and as a fully registered Agentverse agent discoverable via DeltaV.

**MCP Server URL:** `https://prediction.mcp.chainaware.ai/sse`
**API keys & pricing:** [chainaware.ai/pricing](https://chainaware.ai/pricing)
**GitHub:** [github.com/ChainAware/behavioral-prediction-mcp](https://github.com/ChainAware/behavioral-prediction-mcp)

---

## Available Tools

ChainAware exposes 5 tools your uAgents can call:

| Tool | What it does | Networks |
|---|---|---|
| `predictive_fraud` | AML check + fraud probability score for any wallet (~98% accuracy) | ETH, BNB, POLYGON, TON, BASE, TRON, HAQQ |
| `predictive_behaviour` | Predicts next on-chain action, risk profile, and wallet segmentation | ETH, BNB, BASE, HAQQ, SOLANA |
| `predictive_rug_pull` | Scores a smart contract or liquidity pool for rug pull risk | ETH, BNB, BASE, HAQQ |
| `token_rank_list` | Ranks tokens by holder community strength | ETH, BNB, BASE, SOLANA |
| `token_rank_single` | Deep community rank + top holders for a single token contract | ETH, BNB, BASE, SOLANA |

---

## Option A — Call ChainAware from Any Existing uAgent (quickest)

Add ChainAware as an outbound HTTP dependency to an agent you already have. No Agentverse registration required — the agent calls ChainAware whenever it handles a relevant user message.

### Step 1 — Install dependencies

```bash
pip install uagents mcp httpx
```

### Step 2 — Add ChainAware calls to your agent

```python
import os
import asyncio
from uagents import Agent, Context, Model
from mcp import ClientSession
from mcp.client.sse import sse_client

CHAINAWARE_URL = (
    f"https://prediction.mcp.chainaware.ai/sse"
    f"?apiKey={os.environ['CHAINAWARE_API_KEY']}"
)

class FraudCheckRequest(Model):
    wallet_address: str
    network: str

class FraudCheckResponse(Model):
    status: str
    probability_fraud: float
    forensic_flags: list[str]

agent = Agent(name="my-web3-agent", seed=os.environ["AGENT_SEED"])

async def call_chainaware(tool: str, params: dict) -> dict:
    async with sse_client(CHAINAWARE_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, params)
            return result.content[0].text if result.content else {}

@agent.on_message(model=FraudCheckRequest)
async def handle_fraud_check(ctx: Context, sender: str, msg: FraudCheckRequest):
    ctx.logger.info(f"Fraud check: {msg.wallet_address} on {msg.network}")
    data = await call_chainaware("predictive_fraud", {
        "apiKey": os.environ["CHAINAWARE_API_KEY"],
        "network": msg.network,
        "walletAddress": msg.wallet_address,
    })
    flags = [k for k, v in data.get("forensic_details", {}).items() if v]
    await ctx.send(sender, FraudCheckResponse(
        status=data.get("status", "Unknown"),
        probability_fraud=data.get("probabilityFraud", 0.0),
        forensic_flags=flags,
    ))

if __name__ == "__main__":
    agent.run()
```

Set your environment variables:

```bash
export CHAINAWARE_API_KEY=your-key-here
export AGENT_SEED=your-random-seed-phrase
python agent.py
```

---

## Option B — Standalone ChainAware Agent on Agentverse (DeltaV-discoverable)

Register a dedicated ChainAware agent on Agentverse so that DeltaV can automatically route user requests like *"check this wallet for fraud"* or *"is this contract a rug pull?"* to your agent.

### Step 1 — Install dependencies

```bash
pip install uagents mcp httpx
```

### Step 2 — Define your message protocols

Create `protocols.py` with Pydantic models for each capability you want to expose:

```python
from uagents import Model
from typing import Optional

# --- Fraud Detection ---
class FraudRequest(Model):
    wallet_address: str
    network: str  # ETH, BNB, POLYGON, TON, BASE, TRON, HAQQ

class FraudResponse(Model):
    status: str           # "Fraud" | "Not Fraud" | "New Address"
    probability_fraud: float
    risk_level: str       # Low | Medium | High | Critical
    forensic_flags: list[str]
    recommendation: str

# --- Behavioral Analysis ---
class BehaviourRequest(Model):
    wallet_address: str
    network: str  # ETH, BNB, BASE, HAQQ, SOLANA

class BehaviourResponse(Model):
    experience: int
    categories: list[str]
    risk_profile: str
    intent_trade: str
    intent_stake: str
    intent_bridge: str
    intent_nft: str
    recommendation: str

# --- Rug Pull Detection ---
class RugPullRequest(Model):
    contract_address: str
    network: str  # ETH, BNB, BASE, HAQQ

class RugPullResponse(Model):
    status: str
    probability_fraud: float
    risk_level: str
    forensic_flags: list[str]
    verdict: str

# --- Token Ranking ---
class TokenRankRequest(Model):
    network: str
    category: Optional[str] = ""  # AI Token, RWA Token, DeFi Token, DeFAI Token, DePIN Token
    limit: int = 10

class TokenRankResponse(Model):
    tokens: list[dict]
    total: int
```

### Step 3 — Build the agent

Create `chainaware_agent.py`:

```python
import os
import asyncio
from uagents import Agent, Context, Bureau
from mcp import ClientSession
from mcp.client.sse import sse_client
from protocols import (
    FraudRequest, FraudResponse,
    BehaviourRequest, BehaviourResponse,
    RugPullRequest, RugPullResponse,
    TokenRankRequest, TokenRankResponse,
)

CHAINAWARE_URL = (
    f"https://prediction.mcp.chainaware.ai/sse"
    f"?apiKey={os.environ['CHAINAWARE_API_KEY']}"
)

RISK_LABELS = {
    (0.00, 0.20): ("Low", "Safe to proceed"),
    (0.20, 0.50): ("Medium", "Proceed with caution"),
    (0.50, 0.80): ("High", "Block or require additional verification"),
    (0.80, 1.01): ("Critical", "Reject immediately"),
}

def risk_label(prob: float) -> tuple[str, str]:
    for (lo, hi), label in RISK_LABELS.items():
        if lo <= prob < hi:
            return label
    return ("Unknown", "")

async def mcp_call(tool: str, params: dict) -> dict:
    async with sse_client(CHAINAWARE_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, params)
            return result.content[0].text if result.content else {}

agent = Agent(
    name="chainaware-blockchain-intelligence",
    seed=os.environ["AGENT_SEED"],
    # Hosted on Agentverse — use their endpoint for DeltaV routing
    # port and endpoint set automatically when deployed to Agentverse
)

@agent.on_message(model=FraudRequest)
async def handle_fraud(ctx: Context, sender: str, msg: FraudRequest):
    ctx.logger.info(f"[fraud] {msg.wallet_address} / {msg.network}")
    data = await mcp_call("predictive_fraud", {
        "apiKey": os.environ["CHAINAWARE_API_KEY"],
        "network": msg.network,
        "walletAddress": msg.wallet_address,
    })
    prob = data.get("probabilityFraud", 0.0)
    level, rec = risk_label(prob)
    flags = [k for k, v in data.get("forensic_details", {}).items() if v]
    await ctx.send(sender, FraudResponse(
        status=data.get("status", "Unknown"),
        probability_fraud=prob,
        risk_level=level,
        forensic_flags=flags,
        recommendation=rec,
    ))

@agent.on_message(model=BehaviourRequest)
async def handle_behaviour(ctx: Context, sender: str, msg: BehaviourRequest):
    ctx.logger.info(f"[behaviour] {msg.wallet_address} / {msg.network}")
    data = await mcp_call("predictive_behaviour", {
        "apiKey": os.environ["CHAINAWARE_API_KEY"],
        "network": msg.network,
        "walletAddress": msg.wallet_address,
    })
    intention = data.get("intention", {})
    await ctx.send(sender, BehaviourResponse(
        experience=data.get("experience", {}).get("Value", 0),
        categories=data.get("categories", []),
        risk_profile=data.get("riskProfile", {}).get("Value", "Unknown"),
        intent_trade=intention.get("Prob_Trade", "Low"),
        intent_stake=intention.get("Prob_Stake", "Low"),
        intent_bridge=intention.get("Prob_Bridge", "Low"),
        intent_nft=intention.get("Prob_NFT_Buy", "Low"),
        recommendation=data.get("recommendation", ""),
    ))

@agent.on_message(model=RugPullRequest)
async def handle_rug_pull(ctx: Context, sender: str, msg: RugPullRequest):
    ctx.logger.info(f"[rug_pull] {msg.contract_address} / {msg.network}")
    data = await mcp_call("predictive_rug_pull", {
        "apiKey": os.environ["CHAINAWARE_API_KEY"],
        "network": msg.network,
        "walletAddress": msg.contract_address,
    })
    prob = data.get("probabilityFraud", 0.0)
    level, _ = risk_label(prob)
    flags = [k for k, v in data.get("forensic_details", {}).items() if v]
    verdict = "AVOID" if prob > 0.50 else "CAUTION" if prob > 0.20 else "SAFE"
    await ctx.send(sender, RugPullResponse(
        status=data.get("status", "Unknown"),
        probability_fraud=prob,
        risk_level=level,
        forensic_flags=flags,
        verdict=verdict,
    ))

@agent.on_message(model=TokenRankRequest)
async def handle_token_rank(ctx: Context, sender: str, msg: TokenRankRequest):
    ctx.logger.info(f"[token_rank] {msg.network} / {msg.category}")
    data = await mcp_call("token_rank_list", {
        "limit": str(msg.limit),
        "offset": "0",
        "network": msg.network,
        "sort_by": "communityRank",
        "sort_order": "DESC",
        "category": msg.category or "",
        "contract_name": "",
    })
    contracts = data.get("contracts", [])
    await ctx.send(sender, TokenRankResponse(
        tokens=contracts[:msg.limit],
        total=data.get("total", len(contracts)),
    ))

if __name__ == "__main__":
    agent.run()
```

### Step 4 — Register on Agentverse

1. Go to [agentverse.ai](https://agentverse.ai) and sign in
2. Create a new **Hosted Agent**
3. Upload `chainaware_agent.py` and `protocols.py`
4. Set environment variables in the Agentverse dashboard:
   - `CHAINAWARE_API_KEY` — your ChainAware API key
   - `AGENT_SEED` — a random seed phrase (keep this secret)
5. Add a **service description** so DeltaV can route requests to your agent:

```
This agent checks blockchain wallet addresses for fraud risk, behavioral profiles,
and rug pull risk using ChainAware's on-chain intelligence API. It covers wallets
on Ethereum, BNB, Base, Polygon, TON, TRON, HAQQ, and Solana.
```

6. Add **tags** in Agentverse: `web3`, `fraud-detection`, `blockchain`, `aml`, `rug-pull`, `wallet-analytics`, `defi`

Once live, DeltaV will route requests like *"is this wallet safe?"* or *"check this contract for rug pull risk"* to your registered agent automatically.

---

## Multi-Agent Pipelines

Because each ChainAware capability maps cleanly to a separate uAgent, you can build pipelines where a coordinator agent routes to specialist sub-agents — mirroring ChainAware's own 29-subagent architecture.

### Example: Coordinator → Fraud + Behaviour pipeline

```python
from uagents import Agent, Context, Model
import os

FRAUD_AGENT_ADDRESS  = "agent1q..."   # address of your fraud uAgent
BEHAVIOUR_AGENT_ADDRESS = "agent1q..." # address of your behaviour uAgent

class WalletAuditRequest(Model):
    wallet_address: str
    network: str

class WalletAuditResponse(Model):
    fraud_status: str
    fraud_probability: float
    experience: int
    categories: list[str]
    recommendation: str

coordinator = Agent(name="chainaware-coordinator", seed=os.environ["COORDINATOR_SEED"])

# Store partial results keyed by wallet address
_pending: dict[str, dict] = {}

@coordinator.on_message(model=WalletAuditRequest)
async def start_audit(ctx: Context, sender: str, msg: WalletAuditRequest):
    _pending[msg.wallet_address] = {"sender": sender, "fraud": None, "behaviour": None}
    await ctx.send(FRAUD_AGENT_ADDRESS, FraudRequest(
        wallet_address=msg.wallet_address, network=msg.network
    ))
    await ctx.send(BEHAVIOUR_AGENT_ADDRESS, BehaviourRequest(
        wallet_address=msg.wallet_address, network=msg.network
    ))

@coordinator.on_message(model=FraudResponse)
async def got_fraud(ctx: Context, sender: str, msg: FraudResponse):
    # match back to pending by inspecting context — simplified here
    for wallet, state in _pending.items():
        if state["fraud"] is None:
            state["fraud"] = msg
            _try_complete(ctx, wallet, state)
            break

@coordinator.on_message(model=BehaviourResponse)
async def got_behaviour(ctx: Context, sender: str, msg: BehaviourResponse):
    for wallet, state in _pending.items():
        if state["behaviour"] is None:
            state["behaviour"] = msg
            _try_complete(ctx, wallet, state)
            break

def _try_complete(ctx: Context, wallet: str, state: dict):
    if state["fraud"] and state["behaviour"]:
        f, b = state["fraud"], state["behaviour"]
        asyncio.create_task(ctx.send(state["sender"], WalletAuditResponse(
            fraud_status=f.status,
            fraud_probability=f.probability_fraud,
            experience=b.experience,
            categories=b.categories,
            recommendation=b.recommendation,
        )))
        del _pending[wallet]
```

---

## Mapping ChainAware Subagents to uAgent Patterns

Each of the 29 ChainAware specialist subagents has a direct uAgent equivalent. Build whichever you need:

| ChainAware Subagent | uAgent pattern | MCP tools called |
|---|---|---|
| `chainaware-fraud-detector` | Single handler, `FraudRequest` → `FraudResponse` | `predictive_fraud` |
| `chainaware-aml-scorer` | Single handler, returns AML score 0–100 | `predictive_fraud` |
| `chainaware-trust-scorer` | Single handler, returns `1 - probabilityFraud` | `predictive_fraud` |
| `chainaware-wallet-auditor` | Coordinator → fraud + behaviour + rug pull | All 3 prediction tools |
| `chainaware-rug-pull-detector` | Single handler, `RugPullRequest` → `RugPullResponse` | `predictive_rug_pull` |
| `chainaware-wallet-marketer` | Single handler, returns personalized message ≤20 words | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-reputation-scorer` | Single handler, returns score `1000×(exp+1)×(risk+1)×(1-fraud)` | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-wallet-ranker` | Single handler, returns experience rank + totalPoints | `predictive_behaviour` |
| `chainaware-onboarding-router` | Single handler, returns Beginner / Intermediate / Skip | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-whale-detector` | Single handler, returns Mega Whale / Whale / Emerging / Not | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-defi-advisor` | Single handler, returns recommended DeFi product tier | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-token-ranker` | Single handler, `TokenRankRequest` → ranked list | `token_rank_list` |
| `chainaware-token-analyzer` | Single handler, `TokenRankSingleRequest` → community rank + top holders | `token_rank_single` + `predictive_fraud` |
| `chainaware-airdrop-screener` | Batch handler, filters and ranks wallets | `predictive_fraud` + `predictive_behaviour` |
| `chainaware-lending-risk-assessor` | Single handler, returns grade A–F + collateral ratio | `predictive_fraud` + `predictive_behaviour` |
| `chainaware-token-launch-auditor` | Single handler, takes contract + deployer, returns APPROVED / CONDITIONAL / REJECTED | `predictive_rug_pull` + `predictive_fraud` + `predictive_behaviour` |
| `chainaware-agent-screener` | Single handler, takes agent + feeder wallet, returns trust score 0–10 | `predictive_fraud` + `predictive_behaviour` |
| `chainaware-cohort-analyzer` | Batch handler, returns cohort segments + engagement strategies | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-counterparty-screener` | Single handler, returns Safe / Caution / Block | `predictive_fraud` + `predictive_behaviour` |
| `chainaware-governance-screener` | Single or batch handler, returns Sybil flag + voting weight | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-transaction-monitor` | Single handler, returns ALLOW / FLAG / HOLD / BLOCK | `predictive_fraud` + `predictive_rug_pull` + `predictive_behaviour` |
| `chainaware-lead-scorer` | Single handler, returns score 0–100 + tier Hot/Warm/Cold/Dead | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-upsell-advisor` | Single handler, returns next product + upgrade readiness score | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-platform-greeter` | Single handler, returns contextual welcome message | `predictive_behaviour` + `predictive_fraud` |
| `chainaware-marketing-director` | Coordinator → cohort + lead + whale + greeter pipeline | `predictive_fraud` + `predictive_behaviour` |
| `chainaware-compliance-screener` | Coordinator → fraud + AML + counterparty pipeline, returns PASS / EDD / REJECT | `predictive_fraud` |
| `chainaware-gamefi-screener` | Single handler, returns player tier + P2E multiplier | `predictive_fraud` + `predictive_behaviour` |
| `chainaware-portfolio-risk-advisor` | Batch handler, returns portfolio grade A–F + rebalancing plan | `predictive_rug_pull` + `token_rank_single` |
| `chainaware-rwa-investor-screener` | Single handler, returns QUALIFIED / CONDITIONAL / REFER_TO_KYC / DISQUALIFIED | `predictive_fraud` + `predictive_behaviour` |

Full system prompt logic for each subagent is in `.claude/agents/` and the equivalent Eliza character files are in `eliza/characters/`. Use them as the specification for what each uAgent handler should implement.

---

## API Key Handling

In uAgents, **never put your API key in the agent source file.** Use environment variables:

```python
import os
API_KEY = os.environ["CHAINAWARE_API_KEY"]
```

On Agentverse hosted agents, set `CHAINAWARE_API_KEY` in the environment variables panel in the dashboard — it is injected at runtime and never stored in your code.

For local development:

```bash
export CHAINAWARE_API_KEY=your-key-here
python chainaware_agent.py
```

---

## Getting an API Key

Subscribe at [chainaware.ai/pricing](https://chainaware.ai/pricing). Once you have a key, the MCP endpoint is immediately available — no additional registration or whitelisting required.

**Privacy:** wallet addresses sent to ChainAware are pseudonymous blockchain identifiers. See [chainaware.ai/privacy](https://chainaware.ai/privacy) for the full data policy.

---

## Further Reading

| Resource | Link |
|---|---|
| Fetch.ai uAgents docs | https://fetch.ai/docs/guides/agents/quickstart |
| Agentverse hosted agents | https://fetch.ai/docs/guides/agentverse/agentverse-hosted-agents |
| DeltaV service descriptions | https://fetch.ai/docs/guides/agents/intermediate/agent-functions |
| ChainAware MCP developer guide | https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/ |
| ChainAware complete product guide | https://chainaware.ai/blog/chainaware-ai-products-complete-guide/ |
| 12 blockchain capabilities for AI agents | https://chainaware.ai/blog/12-blockchain-capabilities-any-ai-agent-can-use-mcp-integration-guide/ |
