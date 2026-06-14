# Token Rank Single — Reference

**Tool ID:** `token_rank_single`
**MCP Endpoint:** `https://prediction.mcp.chainaware.ai/sse`

Returns the community rank and top holders for a specific token, identified by contract address
and network. Unlike `token_rank_list` which returns ranked lists for discovery, this tool
deep-dives into a single token — surfacing its strongest holders with full wallet-level
intelligence (balance, age, transaction count, global rank).

Use this when a user wants to understand *who* holds a token and *how strong* those holders are.

---

## Supported Networks

`ETH` · `BNB` · `BASE` · `SOLANA`

---

## Input Schema

| Field              | Type   | Required | Description                                              |
|-------------------|--------|----------|----------------------------------------------------------|
| `contract_address` | string | ✅        | Token contract or mint address (chain-specific format)   |
| `network`          | string | ✅        | One of: `ETH`, `BNB`, `BASE`, `SOLANA`                  |

---

## Output Schema

```json
{
  "message": "string",
  "data": {
    "contract": {
      "contractAddress": "string",
      "contractName": "string",
      "ticker": "string",
      "chain": "string",
      "category": "string",
      "type": "string",
      "communityRank": 0,
      "normalizedRank": 0,
      "totalHolders": 0,
      "lastProcessedAt": "ISO-8601",
      "createdAt": "ISO-8601",
      "updatedAt": "ISO-8601"
    },
    "topHolders": [
      {
        "contractAddress": "string",
        "Holder": {
          "walletAddress": "string",
          "chain": "string",
          "balance": "string",
          "walletAgeInDays": 0,
          "transactionsNumber": 0,
          "totalPoints": 0.0,
          "globalRank": 0
        }
      }
    ]
  }
}
```

---

## Key Output Fields Explained

### `data.contract` — Token Details

| Field            | Description                                                     |
|------------------|-----------------------------------------------------------------|
| `communityRank`  | Raw ranking based on aggregate holder behavioral quality        |
| `normalizedRank` | Normalized score for cross-chain/cross-category comparison      |
| `totalHolders`   | Total unique wallet addresses holding this token                |
| `category`       | Token category (e.g. `AI Token`, `DeFi Token`)                 |

### `data.topHolders[]` — Strongest Holders

Each entry in `topHolders` includes a `Holder` object with wallet-level intelligence:

| Field               | Description                                                  |
|---------------------|--------------------------------------------------------------|
| `walletAddress`     | The holder's wallet address                                  |
| `balance`           | Token balance held (string to preserve precision)            |
| `walletAgeInDays`   | Age of the wallet in days                                    |
| `transactionsNumber`| Total transaction count across the wallet's history          |
| `totalPoints`       | Computed wallet scoring metric (float)                       |
| `globalRank`        | Wallet rank across the entire ChainAware 14M+ wallet network |

### Global Rank Interpretation

| globalRank Range | Tier       | Meaning                                    |
|-----------------|------------|--------------------------------------------|
| Top 1%          | Elite      | Highest-quality wallets in the network     |
| Top 10%         | Strong     | Well-established, active wallets           |
| Top 25%         | Above Avg  | Solid on-chain history                     |
| Bottom 50%      | Developing | Newer or less active wallets               |

---

## Example Agent Prompts

```
"What is the token rank for USDT on Ethereum?"
"Who are the top holders of 0xdAC17F958D2ee523a2206206994597C13D831ec7 on ETH?"
"Show me the best holders of this Solana token."
"How strong is the holder base of this contract on BNB?"
"What's the global rank of wallets holding this BASE token?"
"Deep-dive into the community quality of this token."
"Are the top holders of this token experienced or new wallets?"
"Compare holder quality: is this token held by whales or retail?"
```

---

## Example API Call (Node.js)

```javascript
const result = await client.call("token_rank_single", {
  contract_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  network: "ETH"
});

const { contract, topHolders } = result.data;
console.log(`${contract.contractName} (${contract.ticker})`);
console.log(`Community Rank: ${contract.communityRank}`);
console.log(`Total Holders: ${contract.totalHolders}`);
console.log(`\nTop Holders:`);
topHolders.forEach((entry, i) => {
  const h = entry.Holder;
  console.log(`  ${i + 1}. ${h.walletAddress} — Balance: ${h.balance}, Global Rank: ${h.globalRank}, Age: ${h.walletAgeInDays}d`);
});
```

---

## Example API Call (Python)

```python
result = client.call("token_rank_single", {
    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "network": "ETH"
})

contract = result["data"]["contract"]
print(f"{contract['contractName']} ({contract['ticker']})")
print(f"Community Rank: {contract['communityRank']}")
print(f"Total Holders: {contract['totalHolders']}")

print("\nTop Holders:")
for i, entry in enumerate(result["data"]["topHolders"]):
    h = entry["Holder"]
    print(f"  {i+1}. {h['walletAddress']} — Balance: {h['balance']}, Global Rank: {h['globalRank']}, Age: {h['walletAgeInDays']}d")
```

---

## Use Cases

- **Token due diligence** — before investing, check if a token is held by experienced, high-rank wallets or fresh/suspicious ones
- **Whale analysis** — identify the top holders and assess whether they are long-term participants or short-term flippers
- **Community health monitoring** — track whether a token's top holders are strengthening or weakening over time
- **Governance intelligence** — understand who the most influential holders are for DAO voting and proposals
- **Exchange listing decisions** — evaluate holder quality as a factor in token listing approvals
- **Investor relations** — surface wallet-level data on top token holders for reporting and outreach

---

## Composability

Token rank data pairs naturally with other ChainAware tools:

- Use `predictive_behaviour` on a top holder's `walletAddress` to get their full behavioral profile
- Use `predictive_fraud` on a top holder to check if any major holders are flagged
- Use `token_rank_list` first to discover tokens, then `token_rank_single` to deep-dive

---

## Error Codes

| Code  | Meaning                                                  |
|-------|----------------------------------------------------------|
| `403` | Invalid or missing API key                               |
| `400` | Malformed `contract_address` or `network`                |
| `500` | Temporary backend failure — retry after a short delay    |

---

## Further Reading

- Complete Product Guide: https://chainaware.ai/blog/chainaware-ai-products-complete-guide/
- Prediction MCP Developer Guide: https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/
