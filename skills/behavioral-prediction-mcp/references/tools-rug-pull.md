# Predictive Rug Pull Detection — Reference

**Tool ID:** `predictive_rug_pull`
**MCP Endpoint:** `https://prediction.mcp.chainaware.ai/sse`

Forecasts whether a smart contract or liquidity pool is likely to execute a rug pull —
*before* investors deposit capital. Analyzes the contract itself, its deployer's on-chain
history, and the behavior of associated liquidity providers.

Core insight: **bad actors cannot create good contracts**. A deployer's behavioral history
across 8 chains reveals who they are, regardless of how polished their website or whitepaper looks.

---

## Supported Networks

`ETH` · `BNB` · `BASE` · `HAQQ`

---

## Input Schema

| Field           | Type   | Required | Description                                              |
|----------------|--------|----------|----------------------------------------------------------|
| `apiKey`        | string | ✅        | ChainAware API key                                       |
| `network`       | string | ✅        | One of: `ETH`, `BNB`, `BASE`, `HAQQ`                    |
| `walletAddress` | string | ✅        | Smart contract address or liquidity pool address to check |

---

## Output Schema

```json
{
  "message": "Success",
  "contractAddress": "0x1234...",
  "status": "Fraud | Not Fraud",
  "probabilityFraud": 0.87,
  "lastChecked": "2025-10-25T12:45:00Z",
  "forensic_details": {
    "...": "on-chain metrics used in scoring"
  },
  "createdAt": "2025-10-25T12:45:00Z",
  "updatedAt": "2025-10-25T12:45:00Z"
}
```

### Status Values

| Value       | Meaning                                               |
|------------|-------------------------------------------------------|
| `Fraud`     | High rug pull probability — avoid depositing          |
| `Not Fraud` | Low rug pull probability — contract appears legitimate |

### probabilityFraud Interpretation

| Range       | Risk Level | Recommended Action                                   |
|------------|------------|------------------------------------------------------|
| 0.00–0.20   | Low        | Contract appears safe                                |
| 0.21–0.50   | Medium     | Proceed with caution; monitor deployer activity      |
| 0.51–0.80   | High       | Warn users prominently before they deposit           |
| 0.81–1.00   | Critical   | Block listing or deposit entirely                    |

---

## Example Agent Prompts

```
"Will this new DeFi pool rug pull if I stake my assets?"
"Is this smart contract on BNB safe? Address: 0x456..."
"Check the rug pull risk of this ETH liquidity pool."
"Monitor my LP position for potential future exploits."
"Should I invest in this new launchpad project? Contract: 0x789..."
"Scan these 10 contracts before we list them on our DEX."
"Flag any pools on BASE with a rug pull probability above 0.5."
```

---

## Example API Call (Node.js)

```javascript
const result = await client.call("predictive_rug_pull", {
  apiKey: process.env.CHAINAWARE_API_KEY,
  network: "BNB",
  walletAddress: "0xContractAddressHere"
});

if (result.probabilityFraud > 0.5) {
  console.warn("⚠️ High rug pull risk:", result.probabilityFraud);
  blockDeposit();
} else {
  console.log("✅ Contract appears safe:", result.status);
}
```

---

## Example API Call (Python)

```python
result = client.call("predictive_rug_pull", {
    "apiKey": os.environ["CHAINAWARE_API_KEY"],
    "network": "ETH",
    "walletAddress": "0xContractAddressHere"
})

print(result["status"])           # "Not Fraud"
print(result["probabilityFraud"]) # 0.05
```

---

## How the Scoring Works

The model evaluates three layers:

1. **Contract layer** — bytecode patterns, proxy structures, admin key permissions,
   honeypot indicators, mint functions, ownership concentration

2. **Deployer layer** — the wallet that deployed the contract is scored for its full
   cross-chain behavioral history; serial rug pullers are flagged even with fresh contracts

3. **Liquidity layer** — LP wallet behaviors, lock status, withdrawal velocity patterns,
   and concentration of liquidity in suspicious addresses

All three layers feed a single `probabilityFraud` score, updated continuously as on-chain
activity evolves.

---

## Use Cases

- **Launchpads** — vet every project before listing; block high-risk contracts automatically
- **DEXes** — scan new liquidity pools before they appear in your UI
- **Investors** — check any token contract before buying or providing liquidity
- **Wallets & portfolio trackers** — warn users in real time when they're about to interact
  with a flagged contract
- **Insurance protocols** — price smart contract cover based on rug pull probability scores
- **DeFi aggregators** — filter out high-risk pools from yield routing

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
- Pump & Dump vs Rug Pull — How to Spot Both: https://chainaware.ai/blog/pump-and-dump-vs-rug-pull/
