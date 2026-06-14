# Token Rank List — Reference

**Tool ID:** `token_rank_list`
**MCP Endpoint:** `https://prediction.mcp.chainaware.ai/sse`

Ranks tokens by the quality and strength of their holder community. TokenRank analyzes every
holder of a token, scores them using ChainAware's 14M+ wallet behavioral profiles, and ranks
the token based on the aggregate strength of its community — not market cap, not price, not hype.

The stronger the holders, the stronger the token.

---

## Supported Networks

`ETH` · `BNB` · `BASE` · `SOLANA`

---

## Input Schema

| Field            | Type   | Required | Description                                                                 |
|-----------------|--------|----------|-----------------------------------------------------------------------------|
| `limit`          | string | ✅        | Number of items to return per page (e.g. `"10"`, `"25"`)                   |
| `offset`         | string | ✅        | Page number for pagination (e.g. `"0"` for first page)                     |
| `network`        | string | ✅        | One of: `ETH`, `BNB`, `BASE`, `SOLANA`                                    |
| `sort_by`        | string | ✅        | Field to sort by (e.g. `communityRank`)                                    |
| `sort_order`     | string | ✅        | `ASC` or `DESC`                                                            |
| `category`       | string | ✅        | Token category filter (see categories below). Use empty string for all     |
| `contract_name`  | string | ✅        | Search by token/contract name. Use empty string for no filter              |

### Token Categories

| Category      | Description                                |
|---------------|--------------------------------------------|
| `AI Token`    | Tokens in the AI / artificial intelligence sector |
| `RWA Token`   | Real-World Asset tokens                    |
| `DeFi Token`  | Decentralized finance tokens               |
| `DeFAI Token` | DeFi + AI hybrid tokens                   |
| `DePIN Token` | Decentralized Physical Infrastructure tokens |

---

## Output Schema

```json
{
  "message": "string",
  "data": {
    "total": 0,
    "contracts": [
      {
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
      }
    ]
  }
}
```

---

## Key Output Fields Explained

### `communityRank` — Raw Community Ranking

Integer ranking based on the aggregate behavioral quality of the token's holders.
Lower values = stronger community. Derived from holder experience scores, transaction
history, protocol diversity, and wallet age across the ChainAware network.

### `normalizedRank` — Normalized Ranking Score

Scaled ranking score for easier cross-chain and cross-category comparison.

### `totalHolders` — Holder Count

Total unique wallet addresses holding this token. Combined with community rank,
this distinguishes tokens with many weak holders from tokens with fewer but
stronger holders.

### `category` — Token Classification

Primary category label assigned to the token. Useful for filtering and comparing
tokens within the same sector (e.g. all AI tokens, all DeFi tokens).

---

## Example Agent Prompts

```
"What are the top AI tokens on Ethereum?"
"Rank DeFi tokens on BNB by community strength."
"Which RWA tokens have the strongest holder base?"
"Show me the top 10 DePIN tokens on Solana."
"Compare AI tokens across ETH and BASE by community rank."
"Find the best DeFAI tokens right now."
"Search for tokens named 'Render' on Ethereum."
"Which tokens have the most holders on BNB?"
```

---

## Example API Call (Node.js)

```javascript
const result = await client.call("token_rank_list", {
  limit: "10",
  offset: "0",
  network: "ETH",
  sort_by: "communityRank",
  sort_order: "DESC",
  category: "AI Token",
  contract_name: ""
});

console.log(`Total AI tokens on ETH: ${result.data.total}`);
result.data.contracts.forEach((token, i) => {
  console.log(`${i + 1}. ${token.contractName} (${token.ticker}) — Rank: ${token.communityRank}, Holders: ${token.totalHolders}`);
});
```

---

## Example API Call (Python)

```python
result = client.call("token_rank_list", {
    "limit": "10",
    "offset": "0",
    "network": "ETH",
    "sort_by": "communityRank",
    "sort_order": "DESC",
    "category": "AI Token",
    "contract_name": ""
})

print(f"Total AI tokens on ETH: {result['data']['total']}")
for i, token in enumerate(result["data"]["contracts"]):
    print(f"{i+1}. {token['contractName']} ({token['ticker']}) — Rank: {token['communityRank']}, Holders: {token['totalHolders']}")
```

---

## Use Cases

- **Token discovery** — find the strongest tokens in any category based on holder quality, not hype
- **Due diligence** — compare community strength before investing; weak holder bases signal fragility
- **Portfolio construction** — weight portfolios toward tokens with high-quality, committed holders
- **DEX/aggregator curation** — surface top-ranked tokens in category pages and search results
- **Research & analytics** — track how token community quality evolves over time across chains
- **Marketing intelligence** — identify which token communities attract the strongest wallets

---

## Error Codes

| Code  | Meaning                                                  |
|-------|----------------------------------------------------------|
| `403` | Invalid or missing API key                               |
| `400` | Malformed `network`, `category`, or pagination params    |
| `500` | Temporary backend failure — retry after a short delay    |

---

## Further Reading

- Complete Product Guide: https://chainaware.ai/blog/chainaware-ai-products-complete-guide/
- Prediction MCP Developer Guide: https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/
