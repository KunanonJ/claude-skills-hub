# Tool Reference: `credit_score`

## Overview

AI-driven crypto credit/trust scoring for blockchain wallets. Combines fraud probability, on-chain inflow/outflow analytics, and social graph analysis to produce a single **riskRating** (1–9) that reflects a wallet's borrower reliability and trustworthiness.

Primary use case: DeFi lending protocols that need a fast, single-number creditworthiness signal per wallet — without building their own scoring model.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `apiKey` | string | ✅ | API key for authentication (`CHAINAWARE_API_KEY` env var) |
| `network` | string | ✅ | Blockchain network: `ETH` |
| `walletAddress` | string | ✅ | The wallet address to score |

---

## Output

```json
{
  "message": "Success",
  "creditData": {
    "riskRating": 7,
    "walletAddress": "0x..."
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | `"Success"` or error text |
| `creditData.riskRating` | integer | Credit/trust score from 1 (highest risk) to 9 (highest trust) |
| `creditData.walletAddress` | string | Echoed wallet address |

---

## Rating Scale

| riskRating | Risk Level | Lending Interpretation |
|-----------|------------|------------------------|
| 9 | Very Low Risk | Prime borrower — best terms |
| 7–8 | Low Risk | Reliable borrower — standard terms |
| 5–6 | Moderate Risk | Elevated caution — higher collateral |
| 3–4 | High Risk | Restricted terms or decline |
| 1–2 | Very High Risk | Decline — do not lend |

**Tip:** Convert to a 0–100 component for composite scoring:
```
credit_component = ((riskRating - 1) / 8) × 100
```

---

## Supported Networks

`ETH`

Note: Only Ethereum is currently supported. For all other networks, fall back to `predictive_fraud` alone.

---

## Error Cases

| Code | Cause |
|------|-------|
| `401 Unauthorized` | Invalid `apiKey` |
| `400 Bad Request` | Malformed `network` or `walletAddress` |
| `500 Internal Server Error` | Temporary downstream failure |

---

## Key Differences from `predictive_fraud`

| Aspect | `predictive_fraud` | `credit_score` |
|--------|-------------------|----------------|
| Output | Continuous 0.00–1.00 probability + forensic details | Integer 1–9 rating |
| Signal sources | On-chain behavior, AML flags | Fraud score + social graph |
| AML forensics | ✅ Full forensic breakdown | ❌ Rating only |
| Networks | ETH, BNB, POLYGON, TON, BASE, TRON, HAQQ | ETH only |
| Best for | Fraud detection, compliance screening | Lending/credit decisions |

---

## Usage in Agents

The `credit_score` tool is used by:
- **`chainaware-lending-risk-assessor`** — as a third signal alongside `predictive_fraud` and `predictive_behaviour`

It can be used standalone for any use case requiring a quick creditworthiness signal without the full forensic detail of `predictive_fraud`.

---

## Example Use Cases

- "What is the credit score for this wallet?"
- "What's the calculated trust score for 0x...?"
- "Calculate credit score for this borrower before approving a loan."
- "Screen these wallets by credit rating before adding to our lending whitelist."

---

## Further Reading

- [Credit Score Guide](https://chainaware.ai/blog/chainaware-credit-score-the-complete-guide-to-web3-credit-scoring-in-2026/) — Full methodology, use cases, and DeFi lending integration patterns
- [Credit Scoring Agent Guide](https://chainaware.ai/blog/chainaware-credit-scoring-agent-guide/) — How to build and use the ChainAware credit scoring agent
- [Top 5 Ways Prediction MCP Will Turbocharge Your DeFi Platform](https://chainaware.ai/blog/top-5-ways-prediction-mcp-will-turbocharge-your-defi-platform/) — Lending use case deep-dive
