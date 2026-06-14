# Predictive Fraud Detection — Reference

**Tool ID:** `predictive_fraud`
**MCP Endpoint:** `https://prediction.mcp.chainaware.ai/sse`

Forecasts the probability that a wallet address will engage in fraudulent activity *before*
any transaction takes place. Also performs AML (Anti-Money Laundering) checks.

- ~98% accuracy on Ethereum
- ~96% accuracy on BNB Smart Chain
- Not rules-based blocklisting — AI trained on 1.3B+ behavioral data points

---

## Supported Networks

`ETH` · `BNB` · `POLYGON` · `TON` · `BASE` · `TRON` · `HAQQ`

---

## Input Schema

| Field           | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| `apiKey`        | string | ✅        | ChainAware API key (obtain at chainaware.ai/pricing) |
| `network`       | string | ✅        | One of: `ETH`, `BNB`, `POLYGON`, `TON`, `BASE`, `TRON`, `HAQQ` |
| `walletAddress` | string | ✅        | The wallet address to evaluate (hex or ENS) |

---

## Output Schema

```json
{
  "message": "string",
  "walletAddress": "string",
  "status": "Fraud | Not Fraud | New Address",
  "probabilityFraud": "0.00–1.00",
  "token": "string",
  "lastChecked": "ISO-8601 timestamp",
  "forensic_details": {
    "...": "deep on-chain behavioral metrics"
  },
  "createdAt": "ISO-8601 timestamp",
  "updatedAt": "ISO-8601 timestamp"
}
```

### Status Values

| Value          | Meaning                                                        |
|---------------|----------------------------------------------------------------|
| `Fraud`        | High probability of fraudulent activity                        |
| `Not Fraud`    | Low probability — wallet appears safe                          |
| `New Address`  | Insufficient on-chain history to score; treat with caution     |

### probabilityFraud Interpretation

| Range       | Risk Level | Recommended Action                          |
|------------|------------|---------------------------------------------|
| 0.00–0.20   | Low        | Safe to proceed                             |
| 0.21–0.50   | Medium     | Proceed with caution, consider extra checks |
| 0.51–0.80   | High       | Flag for manual review                      |
| 0.81–1.00   | Critical   | Block or reject immediately                 |

---

## Example Agent Prompts

```
"Is it safe to interact with vitalik.eth on Ethereum?"
"What is the fraud risk of 0xABC123... on BNB?"
"Run an AML check on this wallet: 0x456... (BASE network)"
"Is my new wallet flagged for any suspicious behavior?"
"Check if this address on TRON has a history of fraud."
"Screen all wallets connecting to my Dapp today."
```

---

## Example API Call (Node.js)

```javascript
const result = await client.call("predictive_fraud", {
  apiKey: process.env.CHAINAWARE_API_KEY,
  network: "ETH",
  walletAddress: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" // vitalik.eth
});

// result.status        → "Not Fraud"
// result.probabilityFraud → 0.02
```

---

## Example API Call (Python)

```python
result = client.call("predictive_fraud", {
    "apiKey": os.environ["CHAINAWARE_API_KEY"],
    "network": "ETH",
    "walletAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
})

print(result["status"])           # "Not Fraud"
print(result["probabilityFraud"]) # 0.02
```

---

## Use Cases

- **DeFi onboarding** — screen wallets before allowing deposits, borrowing, or staking
- **NFT launchpads** — block fraudulent minters from participating in drops
- **Crypto exchanges** — AML compliance checks at account creation
- **Lending protocols** — reject high-risk borrowers before loan origination
- **Continuous monitoring** — re-check wallets periodically to catch behavioral changes

---

## Error Codes

| Code  | Meaning                                                  |
|-------|----------------------------------------------------------|
| `403` | Invalid or missing `apiKey`                              |
| `400` | Malformed `network` or `walletAddress`                   |
| `500` | Temporary backend failure — retry after a short delay    |

---

## Further Reading

- Complete Product Guide: https://chainaware.ai/blog/chainaware-ai-products-complete-guide/
- AI-Based Predictive Fraud Detection in Web3: https://chainaware.ai/blog/ai-based-predictive-fraud-detection-in-web3/
