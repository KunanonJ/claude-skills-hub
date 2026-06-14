# Predictive Behaviour Analysis — Reference

**Tool ID:** `predictive_behaviour`
**MCP Endpoint:** `https://prediction.mcp.chainaware.ai/sse`

Profiles a wallet's complete on-chain history and predicts what it is *likely to do next*.
Powers AI agent personalization, user segmentation, next-best-action recommendations,
and experience-level scoring.

This is the core tool for **personalizing DeFi agents** — giving them real behavioral context
about each wallet they interact with, instead of serving generic responses.

---

## Supported Networks

`ETH` · `BNB` · `BASE` · `HAQQ` · `SOLANA`

---

## Input Schema

| Field           | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| `apiKey`        | string | ✅        | ChainAware API key                       |
| `network`       | string | ✅        | One of: `ETH`, `BNB`, `BASE`, `HAQQ`, `SOLANA` |
| `walletAddress` | string | ✅        | The wallet address to profile            |

---

## Output Schema

```json
{
  "message": "string",
  "walletAddress": "string",
  "status": "Fraud | Not Fraud | New Address",
  "probabilityFraud": "0.00–1.00",
  "balance": 12450.75,
  "lastChecked": "ISO-8601 timestamp",
  "forensic_details": { },
  "categories": [
    { "Category": "DeFi Lender", "Count": 142 },
    { "Category": "Bridge User", "Count": 38 }
  ],
  "riskProfile": [
    { "Category": "Conservative", "Balance_age": 1.8 }
  ],
  "segmentInfo": "JSON-string of segment counts",
  "experience": { "Type": "Experience", "Value": 8 },
  "intention": {
    "Type": "Intentions",
    "Value": {
      "Prob_Trade": "High",
      "Prob_Stake": "Medium",
      "Prob_Bridge": "Low",
      "Prob_NFT_Buy": "Low"
    }
  },
  "protocols": [
    { "Protocol": "Aave", "Count": 54 },
    { "Protocol": "Uniswap", "Count": 31 }
  ],
  "recommendation": {
    "Type": "Recommendation",
    "Value": [
      "Consider showcasing high-yield staking opportunities",
      "This wallet has strong DeFi experience — skip onboarding prompts"
    ]
  },
  "createdAt": "ISO-8601 timestamp",
  "updatedAt": "ISO-8601 timestamp"
}
```

---

## Key Output Fields Explained

### `categories` — Behavioral Segments

Classifies the wallet's primary on-chain activity patterns:

| Category            | Description                                      |
|--------------------|--------------------------------------------------|
| `DeFi Lender`       | Regularly deposits into lending protocols        |
| `Active Trader`     | High swap/trade frequency                        |
| `NFT Collector`     | Significant NFT purchase history                 |
| `Governance Participant` | Votes in DAO governance                   |
| `Bridge User`       | Frequently moves assets cross-chain              |
| `New Wallet`        | Limited on-chain history                         |
| `Yield Farmer`      | Actively seeks and rotates yield opportunities   |

### `intention` — Predicted Next Actions

Probability of the wallet's next on-chain action within the near term:

| Field          | Values              |
|---------------|---------------------|
| `Prob_Trade`   | `High / Medium / Low` |
| `Prob_Stake`   | `High / Medium / Low` |
| `Prob_Bridge`  | `High / Medium / Low` |
| `Prob_NFT_Buy` | `High / Medium / Low` |

### `experience` — Expertise Score

Integer 0–10 representing on-chain maturity:

| Range  | Interpretation             |
|--------|----------------------------|
| 0–2    | Beginner — new to DeFi     |
| 3–5    | Intermediate               |
| 6–7    | Experienced                |
| 8–10   | Expert / Power User        |

### `recommendation` — Personalized Action Suggestions

Array of strings the AI agent can use directly to shape its response or UI — e.g. skip
onboarding for expert wallets, surface staking CTAs for high-stake-intent users.

---

## Example Agent Prompts

```
"What will 0xABC123... on ETH do next?"
"Is this user a DeFi lender or an NFT trader?"
"What's the experience level of this Solana wallet?"
"Recommend the best yield strategy for 0x123... on BASE."
"Personalize my DeFi agent's response for this wallet."
"Segment this wallet for my marketing campaign."
"Which protocols does this wallet use most on BNB?"
"Should I show the beginner onboarding flow to 0x789...?"
```

---

## Personalization Pattern (Agent Pseudocode)

```javascript
// 1. Get wallet behavioral profile
const profile = await client.call("predictive_behaviour", {
  apiKey: process.env.CHAINAWARE_API_KEY,
  network: "ETH",
  walletAddress: userWallet
});

// 2. Use intent + experience to shape agent response
const { intention, experience, recommendation, categories } = profile;

if (intention.Value.Prob_Stake === "High") {
  agent.suggest("staking opportunities");
}

if (experience.Value > 7) {
  agent.skipOnboarding();
} else {
  agent.showBeginnersGuide();
}

// 3. Use recommendations directly
agent.setContext(recommendation.Value.join("\n"));
```

---

## Use Cases

- **DeFi personalization** — route users to products that match their behavioral profile
- **Dynamic UI** — show advanced features to expert wallets, onboarding to new ones
- **Targeted campaigns** — segment wallets by category (NFT, DeFi, Bridge) for precision marketing
- **Yield farming automation** — detect high-yield-intent wallets and pre-position incentives
- **Lending** — assess borrower experience and risk tolerance before setting loan terms
- **GameFi** — personalize in-game economies based on a player wallet's on-chain spending patterns

---

## Error Codes

| Code  | Meaning                                                  |
|-------|----------------------------------------------------------|
| `403` | Invalid or missing `apiKey`                              |
| `400` | Malformed `network` or `walletAddress`                   |
| `500` | Temporary backend failure — retry after a short delay    |

---

## Further Reading

- Complete Developer Guide: https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/
- Why Personalization Is the Next Big Thing for AI Agents: https://chainaware.ai/blog/why-personalization-is-the-next-big-thing-for-ai-agents/
- Top 5 Ways Prediction MCP Will Turbocharge Your DeFi Platform: https://chainaware.ai/blog/top-5-ways-prediction-mcp-will-turbocharge-your-defi-platform/
