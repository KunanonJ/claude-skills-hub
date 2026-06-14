# 🧠 ChainAware Behavioural Prediction MCP Server

**MCP Server Name:** ChainAware Behavioural Prediction MCP

**Category:** Web3 / Security / DeFi Analytics

**Status:** Public tools – Private backend

**Access:** By request (API key)

**Server URL:** [https://prediction.mcp.chainaware.ai/sse]

**Repository:** [https://github.com/ChainAware/behavioral-prediction-mcp]

**Website:** [https://chainaware.ai/]

**Twitter:** [https://x.com/ChainAware/]

<!-- MCP -->
mcp-name: io.github.ChainAware/chainaware-behavioral-prediction-mcp

---

## 📖 Description

The **Behavioural Prediction MCP Server** provides AI-powered tools to analyze wallet behaviour prediction,fraud detection and rug pull prediction.

Developers and platforms can integrate these tools through the MCP protocol to safeguard DeFi users, monitor liquidity risks, and score wallet or contract trustworthiness.

All tools follow the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/spec) and can be consumed via MCP-compatible clients.

---

## ⚙️ Available Tools

### 1. Predictive Fraud Detection Tool

**ID:** `predictive_fraud`

**Description:**
This AI‑powered algorithm forecasts the likelihood of fraudulent activity on a given wallet address *before* it happens (≈98% accuracy), and performs AML/Anti‑Money‑Laundering checks. 
Use this when your user wants a risk assessment or early‑warning on a blockchain address.

➡️ Example Use Cases:

    • Is it safe to intercant with vitalik.eth ?
    • What is the fraudulent status of this address ?
    • Is my new wallet at risk of being used for fraud?  

**Inputs:**

| Name            | Type   | Required | Description                                                               |
| --------------- | ------ | -------- | ------------------------------------------------------------------------- |
| `apiKey`        | string | ✅        | API key for authentication                                               |
| `network`       | string | ✅        | Blockchain network (`ETH`, `BNB`,`POLYGON`,`TON`,`BASE`, `TRON`, `HAQQ`) |
| `walletAddress` | string | ✅        | The wallet address to evaluate                                           |



**Outputs (JSON):**

  ```json
  {
    "message": "string",                         // e.g. “Success” or error description
    "walletAddress": "string",                   // blockchain wallet address that was analyzed
    "chain": "string",                           // blockchain network identifier (e.g. ETH, BNB,POLYGON,TON,BASE, TRON, HAQQ)
    "status": "string",                          // classification result (e.g. “Fraud” | “Not Fraud” | “New Address”)
    "probabilityFraud": "0.00–1.00",             // decimal fraud probability score (string to preserve precision)
    
    "token": "string | null",                    // optional token associated with the check (may be null)
    "lastChecked": "ISO-8601 timestamp",         // last time the wallet risk analysis was executed
    
    "forensic_details": {
      "cybercrime": "string",                    // indicator score for cybercrime activity
      "money_laundering": "string",              // indicator score for money laundering activity
      "number_of_malicious_contracts_created": "string",  // number of malicious contracts deployed by this wallet
      "gas_abuse": "string",                     // gas abuse indicator
      "financial_crime": "string",               // financial crime indicator
      "darkweb_transactions": "string",          // interaction with darkweb-linked wallets
      "reinit": "string",                        // reinitialization exploit indicator
      "phishing_activities": "string",           // phishing activity indicator
      "fake_kyc": "string",                      // fake KYC related activity
      "blacklist_doubt": "string",               // suspected blacklist association
      "fake_standard_interface": "string",       // fake ERC interface indicator
      "data_source": "string",                   // source of forensic intelligence (may be empty)
      "stealing_attack": "string",               // stealing attack indicator
      "blackmail_activities": "string",          // blackmail activity indicator
      "sanctioned": "string",                    // sanction exposure indicator
      "malicious_mining_activities": "string",   // malicious mining indicator
      "mixer": "string",                         // interaction with mixing services
      "fake_token": "string",                    // fake token creation or usage indicator
      "honeypot_related_address": "string"       // interaction with honeypot-related addresses
    },
    "checked_times": 0,                          // integer — number of times this wallet has been analyzed
    
    "createdAt": "ISO-8601 timestamp",           // record creation timestamp
    "updatedAt": "ISO-8601 timestamp",           // record last update timestamp

    "sanctionData": [
      {
        "category": "string | null",              // sanction category (may be null)
        "name": "string | null",                  // sanction list name
        "description": "string | null",           // sanction description
        "url": "string | null",                   // source URL for sanction information
        "isSanctioned": false,                    // boolean — whether the wallet is officially sanctioned
        "createdAt": "ISO-8601 timestamp",        // sanction record creation timestamp
        "updatedAt": "ISO-8601 timestamp"         // sanction record last update timestamp
      }
    ]
  }
```

Error cases:

    • `403 Unauthorized` → invalid `apiKey`  
    • `400 Bad Request` → malformed `network` or `walletAddress`  
    • `500 Internal Server Error` → temporary downstream failure  
---

### 2. Predictive Behaviour Analysis Tool

**ID:** `predictive_behaviour`

**Description:**
    This AI‑driven engine projects what a wallet address intentions or what address is likely to do next,
    profiles its past on‑chain history, and recommends personalized actions.

    Use this when you need:

      • Next‑best‑action predictions and intentions(“Will this address deposit, trade, or stake?”)  
      • A risk‑tolerance and experience profile  
      • Category segmentation (e.g. NFT, DeFi, Bridge usage)  
      • Custom recommendations based on historical patterns


➡️ Example Use Cases:

    • “What will this address do next?”  
    • “Is the user high‑risk or experienced?”  
    • “Recommend the best DeFi strategies for 0x1234... on ETH network.”

**Inputs:**

| Name            | Type   | Required           | Description                                                               |
| --------------- | ------ | ------------------ | ------------------------------------------------------------------------- |
| `apiKey`        | string | ✅                 | API key for authentication                                                |
| `network`       | string | ✅                 | Blockchain network (`ETH`, `BNB`,`BASE`,`HAQQ`,`SOLANA`)                  |
| `walletAddress` | string | ✅                 | The wallet address to evaluate                                            |



**Outputs (JSON):**

```json
{
      "message": "string",                           // e.g. “Success” or error description
      "walletAddress": "string",                     // blockchain wallet address analyzed
      "status": "string",                            // fraud classification result (e.g. “Fraud” | “Not Fraud” | “New Address”)

      "probabilityFraud": "0.00–1.00",               // decimal probability score indicating fraud risk
      "token": "string | null",                      // optional token context for the analysis
      "chain": "string",                             // blockchain network identifier (e.g. ETH, BNB,BASE,HAQQ,SOLANA)

      "lastChecked": "ISO-8601 timestamp",           // last time the wallet was analyzed

      "forensic_details": {
        "cybercrime": "string",                      // indicator of cybercrime association
        "money_laundering": "string",                // money laundering activity indicator
        "number_of_malicious_contracts_created": "string", // malicious contracts deployed by wallet
        "gas_abuse": "string",                       // abnormal gas usage indicator
        "financial_crime": "string",                 // financial crime activity indicator
        "darkweb_transactions": "string",            // interaction with darkweb-linked wallets
        "reinit": "string",                          // contract reinitialization exploit indicator
        "phishing_activities": "string",             // phishing activity indicator
        "fake_kyc": "string",                        // fake KYC interaction indicator
        "blacklist_doubt": "string",                 // suspected blacklist association
        "fake_standard_interface": "string",         // fake token interface indicator
        "data_source": "string",                     // source of forensic intelligence
        "stealing_attack": "string",                 // stealing attack indicator
        "blackmail_activities": "string",            // blackmail activity indicator
        "sanctioned": "string",                      // sanction exposure indicator
        "malicious_mining_activities": "string",     // malicious mining activity indicator
        "mixer": "string",                           // interaction with mixing services
        "fake_token": "string",                      // fake token creation/use indicator
        "honeypot_related_address": "string"         // honeypot contract interaction indicator
      },

      "categories": [
        {
          "Category": "string",                      // wallet interaction category (e.g. DeFi, NFT, Bridge)
          "Count": 0                                 // number of transactions/interactions in this category
        }
      ],

      "riskProfile": [
        {
          "Category": "Risk_Profile",                 // willingnes to take risk object
          "Balance_age": 0.0                         // 1-10 willingnes to take risk value
        }
      ],

      "segmentInfo": "string (JSON encoded)",        // serialized JSON containing protocol engagement flags (e.g "{\"Maker\":0,\"Aave_borrow\":0,\"Aave_lend\":1,\"Lido\":0,\"Uniswap\":1,\"Compound_lend\":0,\"Compound_borrow\":0}")

      "experience": {
        "Type": "string",                            // descriptor label (e.g. “Experience”)
        "Value": 0                                   // numeric experience score level
      },

      "intention": {
        "Type": "string",                            // descriptor label (e.g. “Intentions”)
        "Value": {
          "Prob_Lend": "Low | Medium | High",
          "Prob_Trade": "Low | Medium | High",
          "Prob_Game": "Low | Medium | High",
          "Prob_NFT": "Low | Medium | High",
          "Prob_Stake_ETH": "Low | Medium | High",
          "Prob_Borrow": "Low | Medium | High",
          "Prob_Gamble": "Low | Medium | High",
          "Prob_Stake": "Low | Medium | High",
          "Prob_Yield_Farm": "Low | Medium | High",
          "Prob_Leveraged_Stake": "Low | Medium | High",
          "Prob_Leveraged_Stake_ETH": "Low | Medium | High",
          "Prob_Leveraged_Lend": "Low | Medium | High",
          "Prob_Leverage_Long_ETH": "Low | Medium | High",
          "Prob_Leverage_Long": "Low | Medium | High"
        }
      },

      "protocols": [
        {
          "Protocol": "string",                      // protocol name (e.g. Uniswap, Curve, MakerDAO)
          "Count": 0                                 // number of interactions with this protocol
        }
      ],

      "userDetails": {
        "wallet_age_days": 0,                        // age of wallet in days
        "total_balance_usd": 0.0,                    // current wallet balance in USD
        "transaction_count": 0,                      // total number of transactions executed
        "wallet_rank": 0                             // ranking of wallet in the scoring system
      },

      "riskCapability": 0,                           // numeric risk capability score

      "recommendation": {
        "Type": "string",                            // descriptor label (e.g. “Recommendation”)
        "Value": [
          "string"                                   // recommended strategies or actions
        ]
      },

      "checked_times": 0,                            // number of times the wallet analysis was executed
      "createdAt": "ISO-8601 timestamp",             // record creation timestamp
      "updatedAt": "ISO-8601 timestamp",             // record last update timestamp

      "sanctionData": [
        {
          "category": "string | null",               // sanction category
          "name": "string | null",                   // sanction list name
          "description": "string | null",            // sanction description
          "url": "string | null",                    // reference source URL
          "isSanctioned": false,                     // whether the wallet is officially sanctioned
          "createdAt": "ISO-8601 timestamp",
          "updatedAt": "ISO-8601 timestamp"
        }
      ]
    }
    
```

Error cases:

    • `403 Unauthorized` → invalid `apiKey`  
    • `400 Bad Request` → malformed `network` or `walletAddress`  
    • `500 Internal Server Error` → temporary downstream failure  
---


### 3. Predictive Rug‑Pull Detection Tool

**ID:** `predictive_rug_pull`

**Description:**
This AI‑powered engine forecasts which liquidity pools or contracts are likely to perform a “rug pull” in the future. Use this when you need to warn users before they deposit into risky pools or to monitor smart‑contract security on-chain.

➡️ Example Use Cases:

    • “Will this new DeFi pool rug‑pull if I stake my assets?”  
    • “Monitor my LP position for potential future exploits.”  

**Inputs:**

| Name            | Type   | Required | Description                                              |
| --------------- | ------ | -------- | -------------------------------------------------------  |
| `apiKey`        | string | ✅        | API key for authentication                              |
| `network`       | string | ✅        | Blockchain network (`ETH`, `BNB`, `BASE`, `HAQQ`)       |
| `walletAddress` | string | ✅        | Smart contract or liquidity pool address                |

**Outputs (JSON):**

```json
{
      "message": "string",                         // e.g. “Success” or error description

      "contractAddress": "string",                 // smart contract address analyzed
      "pairAddress": "string",                     // liquidity pair address on DEX
      "contractCreatorAddress": "string | null",   // creator address of the contract if known

      "risk_score": 0,                             // numeric internal risk score
      "risk_status": "string",                     // qualitative risk level (e.g. “Low Risk”, “Medium Risk”, “High Risk”)

      "risk_indicators": {
        "is_honeypot": 0,                          // honeypot detection flag
        "honeypot_with_same_creator": 0,           // creator deployed previous honeypots
        "can_take_back_ownership": 0,              // contract allows reclaiming ownership
        "is_mintable": 0,                          // token supply can be minted
        "hidden_owner": 0,                         // hidden ownership mechanism detected

        "buy_tax": 0,                              // buy transaction tax percentage
        "sell_tax": 0,                             // sell transaction tax percentage

        "cannot_buy": 0,                           // trading restriction preventing buys
        "cannot_sell_all": 0,                      // restriction preventing full sell

        "is_blacklisted": 0,                       // blacklist functionality detected
        "is_whitelisted": 0,                       // whitelist-only functionality detected

        "creator_percent": 0,                      // percentage of supply owned by creator
        "lp_holders_locked": false,                // liquidity lock status

        "liquidity": 0.0,                          // liquidity amount in base token
        "market_cap": 0,                           // estimated market capitalization

        "is_in_dex": 0,                            // token listed on DEX

        "slippage_modifiable": 0,                  // contract can modify slippage parameters
        "transfer_pausable": 0,                    // transfers can be paused
        "is_anti_whale": 0,                        // anti-whale protection mechanism
        "anti_whale_modifiable": 0,                // anti-whale parameters modifiable

        "trading_cooldown": 0,                     // cooldown period between trades
        "personal_slippage_modifiable": 0,         // per-wallet slippage modification

        "is_open_source": 0,                       // contract source verified
        "is_proxy": 0,                             // proxy contract indicator

        "owner_address": "string",                 // owner address of contract
        "owner_change_balance": 0,                 // owner ability to modify balances

        "selfdestruct": 0,                         // self-destruct capability
        "external_call": 0,                        // external calls present
        "gas_abuse": 0                             // abnormal gas manipulation behavior
      },

      "liquidityEvent": [
        {
          "eventType": "string",                   // liquidity event type (e.g. add/remove)
          "amount": 0.0,                           // liquidity amount affected
          "token": "string",                       // token symbol involved in liquidity

          "tx_hash": "string",                     // transaction hash

          "from_address": "string",                // address initiating liquidity action
          "from_fraud_probability": "0.00–1.00",   // fraud probability score for sender
          "from_fraud_status": "string",           // fraud classification of sender

          "createdAt": "ISO-8601 timestamp"        // timestamp of liquidity event
        }
      ],

      "status": "string",                          // overall fraud classification of contract
      "probabilityFraud": "0.00–1.00",             // probability of contract being fraudulent

      "chain": "string",                           // blockchain network identifier (e.g. BNB, ETH, BASE, HAQQ)
      "lastChecked": "ISO-8601 timestamp",         // last time contract analysis was performed

      "contractCreationTime": "ISO-8601 timestamp | null", // contract deployment timestamp

      "forensic_details": {
        "owner": "object",                         // owner metadata
        "privilege_withdraw": 0,                   // privileged withdraw capability
        "withdraw_missing": 0,                     // missing withdraw function
        "is_open_source": 0,                       // contract source verification status
        "blacklist": 0,                            // blacklist functionality
        "contract_name": "string",                 // contract/token name
        "selfdestruct": 0,                         // self-destruct capability
        "is_proxy": 0,                             // proxy contract indicator
        "approval_abuse": 0                        // abnormal token approval behavior
      },

      "checked_times": 0,                          // number of times contract has been analyzed

      "createdAt": "ISO-8601 timestamp",           // record creation time
      "updatedAt": "ISO-8601 timestamp"            // last update time
    }
```

Error cases:

    • `403 Unauthorized` → invalid `apiKey`  
    • `400 Bad Request` → malformed `network` or `walletAddress`  
    • `500 Internal Server Error` → temporary downstream failure  

---


### 4. Credit Score Tool

**ID:** `credit_score`

**Description:**
AI-driven crypto credit/trust scoring for blockchain wallets. Combines fraud probability, on-chain inflow/outflow analytics, and social graph analysis to produce a **riskRating** from 1 (highest risk) to 9 (highest trust). Designed for DeFi lending protocols that need a fast, single-number creditworthiness signal per wallet.

➡️ Example Use Cases:

    • "What is the credit score for this wallet?"
    • "What's the calculated trust score for this borrower?"
    • "Calculate credit score before approving this loan."

**Inputs:**

| Name            | Type   | Required | Description                                                               |
| --------------- | ------ | -------- | ------------------------------------------------------------------------- |
| `apiKey`        | string | ✅        | API key for authentication                                               |
| `network`       | string | ✅        | Blockchain network (`ETH`)                                               |
| `walletAddress` | string | ✅        | The wallet address to score                                              |

**Outputs (JSON):**

```json
{
  "message": "Success",
  "creditData": {
    "riskRating": 7,
    "walletAddress": "0x..."
  }
}
```

| riskRating | Risk Level | Lending Interpretation |
|-----------|------------|------------------------|
| 9 | Very Low Risk | Prime borrower |
| 7–8 | Low Risk | Reliable borrower |
| 5–6 | Moderate Risk | Elevated caution |
| 3–4 | High Risk | Restricted terms |
| 1–2 | Very High Risk | Decline |

Error cases:

    • `401 Unauthorized` → invalid `apiKey`
    • `400 Bad Request` → malformed `network` or `walletAddress`
    • `500 Internal Server Error` → temporary downstream failure

---

### 5. Token Rank List Tool


**ID:** `token_rank_list`

**Description:**
TokenRank analyzes the community of token holders and ranks every token by the strength of its holders. The stronger the token holders, the stronger the token! 
Use this when you need to know token rank of a token or tokens or compare between different categories and chains.
You can use search,filter and sort and pagination which returns a list of tokens.

➡️ Example Use Cases:
  – “Which is the best token on AI Token category?”  
  – “Compare x token in ETH chain and BNB chain?”  

**Inputs:**

| Name            | Type   | Required | Description                                                                                                     |
| --------------- | ------ | -------- | --------------------------------------------------------------------------------------------------------------  |
| `limit`         | string | ✅       | Number of items ot fetch during pagination                                                                      |
| `offset`        | string | ✅       | Page number(offset) during pagination                                                                           |
| `network`       | string |          | Blockchain network to filter (`ETH`, `BNB`, `BASE`, `SOLANA`)                                                   |
| `sort_by`       | string |          | Sort the returnet tokens based on (e.g.: 'communityRank')                                                       |
| `sort_order`    | string |          | 'ASC' or 'DESC' sorting the value of sort_by                                                                    |
| `category`      | string |          | Filter based on category of the token (e.g. 'AI Token','RWA Token','DeFi Token','DeFAI Token','DePIN Token')    |
| `contract_name` | string |          | Search based on contract name                                                                                   |


**Outputs (JSON):**

```json
  {
    "message": "string",                    // e.g. “Successfully fetched records” or error description
    "data": {
      "total": 0,                           // integer — total number of matching contracts
      "contracts": [
        {
          "contractAddress": "string",       // unique contract or mint address (chain-specific format)
          "contractName": "string",          // human-readable token name
          "ticker": "string",                // token symbol (usually uppercase, but not guaranteed)
          "chain": "string",                 // blockchain network (e.g. SOLANA | ETH | BNB | BASE)
          "category": "string",              // primary category label (e.g. 'AI Token','RWA Token','DeFi Token','DeFAI Token','DePIN Token') 
          "type": "string",                  // asset classification (e.g. “token” | “nft”)
          "communityRank": 0,                // integer — raw ranking based on community metrics
          "normalizedRank": 0,               // integer — normalized or scaled ranking score
          "totalHolders": 0,                 // integer — total unique wallet holders
          "lastProcessedAt": "ISO-8601",     // timestamp when analytics were last computed
          "createdAt": "ISO-8601",           // record creation timestamp
          "updatedAt": "ISO-8601"            // record last update timestamp
        }
      ]
    }
  }
```

Error cases:

    • `400 Bad Request` → malformed `network` or `walletAddress`  
    • `500 Internal Server Error` → temporary downstream failure  

---

### 6. Token Rank Single Tool

**ID:** `token_rank_single`

**Description:**
  Similar to TokenRank List,Token Rank analyzes the community of token holders and ranks every token by the strength of its holders.
  Except the token rank and token details the token rank single tool fetches the best holders their details and its globalRank alongside others in same network.
  Use this when you need to know token rank of a single token based on contract address and exeact chain or network or when you need best holders of specific token in specifc network or chain

➡️ Example Use Cases:
  – “What is the token rank for token in ETH network?”  
  – "Which are the best holders of this contract token address?”
  – “What is the token rank and its best holders?”

**Inputs:**

| Name              | Type   | Required  | Description                                                    |
| ------------------| ------ | --------- | -------------------------------------------------------------  |
| `contract_address`| string | ✅        | The contract address of the token to evaluate                  |
| `network`         | string | ✅        | Blockchain network to filter (`ETH`, `BNB`, `BASE`, `SOLANA`)  |


**Outputs (JSON):**

```json
 {
      "message": "string",                      // e.g. “Successfully fetched records” or error description
      "data": {
        "contract": {
            "contractAddress": "string",       // unique contract or mint address (chain-specific format)
            "contractName": "string",          // human-readable token name
            "ticker": "string",                // token symbol (usually uppercase, but not guaranteed)
            "chain": "string",                 // blockchain network (e.g. SOLANA | ETH | BNB | BASE)
            "category": "string",              // primary category label (e.g. 'AI Token','RWA Token','DeFi Token','DeFAI Token','DePIN Token') 
            "type": "string",                  // asset classification (e.g. “token” | “nft”)
            "communityRank": 0,                // integer — raw ranking based on community metrics
            "normalizedRank": 0,               // integer — normalized or scaled ranking score
            "totalHolders": 0,                 // integer — total unique wallet holders
            "lastProcessedAt": "ISO-8601",     // timestamp when analytics were last computed
            "createdAt": "ISO-8601",           // record creation timestamp
            "updatedAt": "ISO-8601"            // record last update timestamp
        },
        "topHolders": [
          {
            "contractAddress": "string",        // associated contract address
            "Holder": {
              "walletAddress": "string",        // holder wallet address
              "chain": "string",                // blockchain network of the wallet
              "balance": "string",              // token balance (string to preserve precision)
              "walletAgeInDays": 0,             // integer — age of wallet in days
              "transactionsNumber": 0,          // integer — total transaction count
              "totalPoints": 0.0,               // float — computed wallet scoring metric
              "globalRank": 0                   // integer — wallet rank across entire system
            }
          }
        ]
      }
    }
```

Error cases:

    • `400 Bad Request` → malformed `network` or `walletAddress`  
    • `500 Internal Server Error` → temporary downstream failure  

---

## 🧠 Example Client Usage

### Node.js Example

```js
import { MCPClient } from "mcp-client";

const client = new MCPClient("https://prediction.mcp.chainaware.ai/");

const result = await client.call("predictive_rug_pull", {
  apiKey: "your_api_key",
  network: "BNB",
  walletAddress: "0x1234..."
});

console.log(result);
```

### Python Example

```python
from mcp_client import MCPClient

client = MCPClient("https://prediction.mcp.chainaware.ai/")

res = client.call("chat", {"query": "What is the rug pull risk of 0x1234?"})
print(res)
```

---

Service Configuration:
```{
  "type": "sse",
  "config": {
    "mcpServers": {
      "chainaware-behavioural_prediction_mcp": {
        "type": "sse",
        "url": "https://prediction.mcp.chainaware.ai/sse",
        "description": "The Behavioural Prediction MCP Server provides AI-powered tools to analyze wallet behaviour prediction,fraud detection and rug pull prediction.",
        "headers":{
          "x-api-key":""
        },
        "params":{
          "walletAddress":"",
          "network":""
        },
        "auth": {
          "type": "api_key",
          "header": "X-API-Key"
        }
      }
    }
  }
}
```
---

## 🔌 Integration Notes

* ✅ Compatible with MCP clients across **Node.js**, **Python**, and **browser-based** environments
* 🔁 Uses **Server-Sent Events (SSE)** for streaming / real-time responses
* 📐 JSON schemas conform to the **MCP specification**
* 🚦 Rate limits may apply depending on usage tier
* 🔑 **API key required** for production endpoints

---

## Claude Code (CLI) Configuration

Use the Claude CLI to register the MCP server via SSE transport:

```bash
claude mcp add --transport sse chainaware-behavioural-prediction-mcp-server https://prediction.mcp.chainaware.ai/sse \
  --header "X-API-Key: your-key-here"
```

📚 Documentation:
[https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)

---

## ChatGPT Connector Configuration

> Available in ChatGPT environments that support **Connectors / MCP** (Developer Mode).

### Steps

1. Open **ChatGPT Settings**
2. Navigate to **Apps / Connectors**
3. Click **Add Connector**
4. Enter the integration name and URL below
5. Save the configuration

### Integration Details

**Name**

```
ChainAware Behavioural Prediction MCP Server
```

**Integration URL**

```
https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here
```

---

## Claude Web & Claude Desktop Configuration

### Steps

1. Open **Claude Web** or **Claude Desktop**
2. Go to **Settings → Integrations**
3. Click **Add integration**
4. Enter the name and URL below
5. Click **Add** to complete setup

### Integration Details

**Name**

```
ChainAware Behavioural Prediction MCP Server
```

**Integration URL**

```
https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here
```

📚 Documentation:
[https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers](https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers)

---

## Cursor Configuration

Add the MCP server to your Cursor configuration file (e.g. `mcp.json`):

```json
{
  "mcpServers": {
    "chainaware-behavioural-prediction-mcp-server": {
      "url": "https://prediction.mcpbeta.chainaware.ai/sse",
      "transport": "sse",
      "headers": {
        "X-API-Key": "your-key-here"
      }
    }
  }
}
```

📚 Documentation:
[https://cursor.com/docs/context/mcp](https://cursor.com/docs/context/mcp)

---

## 🤖 Claude Code Subagents

This repository includes **32 ready-to-use Claude Code subagents** in `.claude/agents/` — specialist agents that handle common Web3 intelligence tasks out of the box.

| Agent | Purpose |
|-------|---------|
| `chainaware-wallet-auditor` | Full due diligence — deep behavioural profiling including fraud signals |
| `chainaware-fraud-detector` | Fast wallet fraud screening |
| `chainaware-rug-pull-detector` | Smart contract / LP safety checks |
| `chainaware-trust-scorer` | Trust score (0.00–1.00) |
| `chainaware-credit-scorer` | Crypto credit score (1–9) for lending and creditworthiness decisions |
| `chainaware-ltv-estimator` | 12-month revenue potential (LTV) as a USD range based on behavioral signals |
| `chainaware-reputation-scorer` | Reputation score (0–1000) |
| `chainaware-aml-scorer` | AML compliance scoring (0–100) |
| `chainaware-wallet-ranker` | Wallet experience rank + leaderboard |
| `chainaware-wallet-marketer` | Personalized marketing messages |
| `chainaware-token-ranker` | Discover/rank tokens by holder community strength |
| `chainaware-token-analyzer` | Single token deep-dive + top holders |
| `chainaware-onboarding-router` | Route wallets to beginner/intermediate/skip onboarding |
| `chainaware-whale-detector` | Classify wallets into whale tiers (Mega/Whale/Emerging) |
| `chainaware-defi-advisor` | Personalized DeFi product recommendations by experience + risk tier |
| `chainaware-airdrop-screener` | Batch screen wallets for airdrop eligibility, filter bots/fraud |
| `chainaware-lending-risk-assessor` | Borrower risk grade (A–F), collateral ratio, interest rate tier |
| `chainaware-token-launch-auditor` | Pre-listing launch safety audit — APPROVED/CONDITIONAL/REJECTED |
| `chainaware-agent-screener` | AI agent trust score 0–10 via agent + feeder wallet checks |
| `chainaware-cohort-analyzer` | Segment a batch of wallets into behavioral cohorts with per-cohort engagement strategies |
| `chainaware-counterparty-screener` | Real-time pre-transaction go/no-go verdict (Safe / Caution / Block) before a trade, transfer, or contract interaction |
| `chainaware-governance-screener` | DAO voter screening — Sybil detection, governance tier, and voting weight multiplier (supports token-weighted, reputation-weighted, and quadratic models) |
| `chainaware-sybil-detector` | Bulk Sybil attack detection for DAO votes — classifies voters as ELIGIBLE / REVIEW / EXCLUDE, detects coordinated fraud patterns (wallet farms, new-wallet surges), and produces reputation-weighted vote multipliers |
| `chainaware-transaction-monitor` | Real-time transaction risk scoring for autonomous agents — composite score (0–100) and pipeline action (ALLOW / FLAG / HOLD / BLOCK) |
| `chainaware-lead-scorer` | Sales lead qualification — lead score (0–100), tier (Hot/Warm/Cold/Dead), conversion probability, and recommended outreach angle |
| `chainaware-upsell-advisor` | Upsell path for existing users — upgrade readiness score, next product recommendation, trigger event, and ready-to-use upsell message |
| `chainaware-platform-greeter` | Contextual welcome message for a specific wallet on a specific platform — same wallet gets a different message on Aave vs 1inch vs OpenSea |
| `chainaware-marketing-director` | Full-cycle campaign orchestrator — segments audience, scores leads, detects whales, builds per-cohort message playbook, surfaces upsell opportunities, and routes new wallets |
| `chainaware-compliance-screener` | First-layer MiCA-aligned compliance screening — orchestrates fraud-detector, aml-scorer, transaction-monitor, and counterparty-screener into a Compliance Report with verdict (PASS / EDD / REJECT) |
| `chainaware-gamefi-screener` | Web3 game and P2E wallet screening — detects bot farms, cheaters, and farm wallets; classifies legitimate players into experience tiers for matchmaking; outputs P2E reward eligibility |
| `chainaware-portfolio-risk-advisor` | Portfolio-level rug pull and community health assessment — scans every token, produces weighted Portfolio Risk Score, grade (A–F), concentration flags, and prioritized rebalancing plan |
| `chainaware-rwa-investor-screener` | RWA investor suitability screening — assesses fraud risk, experience, and risk profile alignment against the RWA tier; returns QUALIFIED / CONDITIONAL / REFER_TO_KYC / DISQUALIFIED with investment cap |

### Setup

**Step 1 — Connect the MCP server**

The agents call ChainAware tools via MCP. Register the server first:

```bash
claude mcp add --transport sse chainaware-behavioral-prediction \
  https://prediction.mcp.chainaware.ai/sse \
  --header "X-API-Key: YOUR_KEY"
```

For Cursor / Windsurf, add to `mcp.json`:

```json
{
  "mcpServers": {
    "chainaware-behavioral-prediction": {
      "url": "https://prediction.mcp.chainaware.ai/sse",
      "transport": "sse",
      "headers": { "X-API-Key": "YOUR_KEY" }
    }
  }
}
```

**Step 2 — Copy the agent files**

Clone this repo and copy the agents into your project:

```bash
git clone https://github.com/ChainAware/behavioral-prediction-mcp.git
cp -r behavioral-prediction-mcp/.claude/agents/ your-project/.claude/agents/
```

Or cherry-pick only the agents you need:

```bash
mkdir -p your-project/.claude/agents
cp behavioral-prediction-mcp/.claude/agents/chainaware-fraud-detector.md \
   your-project/.claude/agents/
```

**Step 3 — Set the API key**

```bash
export CHAINAWARE_API_KEY="your-key-here"
```

Get a key at [https://chainaware.ai/pricing](https://chainaware.ai/pricing)

### Important Notes

* The `tools:` line in each agent's frontmatter references the MCP server by its registered name. If you register the server under a different name, update the `tools:` lines to match.
* Agents specify a `model:` in their frontmatter (`claude-haiku-4-5-20251001` or `claude-sonnet-4-6`). You need access to those models.
* The `references/` folder contains detailed tool documentation that gives agents richer context. Copying it alongside the agents is recommended but optional.

---

## 🔐 Security Notes

* Do **not** hard-code API keys in public repositories
* Prefer environment variables or secret managers when supported
* Rotate keys regularly in production environments

---

## 🔒 Access Policy

The MCP server requires an API key for production usage.
To request access:

* You can subscribe to listed available plans via: https://chainaware.ai/pricing

---

## 📖 Further Reading

### Product Overviews
- [ChainAware Complete Product Guide](https://chainaware.ai/blog/chainaware-ai-products-complete-guide/) — Overview of all tools, networks, and coverage
- [Web3 Business Potential](https://chainaware.ai/blog/web3-business-potential/) — Business case and market opportunity for Web3 intelligence
- [Use ChainAware as a Business](https://chainaware.ai/blog/use-chainaware-as-business/) — How to build commercial products and services on top of ChainAware

### Tool-Specific Guides
- [Fraud Detector Guide](https://chainaware.ai/blog/chainaware-fraud-detector-guide/) — How to use `predictive_fraud`: inputs, outputs, thresholds, use cases
- [Rug Pull Detector Guide](https://chainaware.ai/blog/chainaware-rugpull-detector-guide/) — How to use `predictive_rug_pull`: contract scoring, deployer risk, LP analysis
- [Token Rank Guide](https://chainaware.ai/blog/chainaware-token-rank-guide/) — How to use `token_rank_list` and `token_rank_single`: community strength scoring
- [Wallet Rank Guide](https://chainaware.ai/blog/chainaware-wallet-rank-guide/) — Wallet ranking system: experience tiers, global rank, points
- [Wallet Auditor Guide](https://chainaware.ai/blog/chainaware-wallet-auditor-how-to-use/) — Full wallet audit workflow combining multiple tools
- [Transaction Monitoring Guide](https://chainaware.ai/blog/chainaware-transaction-monitoring-guide/) — Real-time transaction risk monitoring patterns
- [Web3 Behavioral User Analytics Guide](https://chainaware.ai/blog/chainaware-web3-behavioral-user-analytics-guide/) — Using `predictive_behaviour` for user analytics and segmentation
- [Credit Score Guide](https://chainaware.ai/blog/chainaware-credit-score-the-complete-guide-to-web3-credit-scoring-in-2026/) — Web3 credit scoring methodology and use in DeFi lending
- [Credit Scoring Agent Guide](https://chainaware.ai/blog/chainaware-credit-scoring-agent-guide/) — How to build and use the ChainAware credit scoring agent

### Analytics & Strategy
- [Web3 User Segmentation & Behavioral Analytics for DApp Growth](https://chainaware.ai/blog/web3-user-segmentation-behavioral-analytics-for-dapp-growth-2026/) — Segmentation strategies for DApp retention and growth
- [AI-Powered Blockchain Analysis: Machine Learning for Crypto Security](https://chainaware.ai/blog/ai-powered-blockchain-analysis-machine-learning-for-crypto-security-2026/) — ML approaches to on-chain security and fraud detection
- [Forensic Crypto Analytics vs AI-Based Crypto Analytics](https://chainaware.ai/blog/forensic-crypto-analytics-versus-ai-based-crypto-analytics/) — Comparison of traditional forensic tools vs ChainAware's predictive AI approach
- [MiCA Compliance DeFi Screener](https://chainaware.ai/blog/mica-compliance-defi-screener-chainaware/) — How ChainAware covers ~70–75% of DeFi MiCA obligations; positions compliance-screener vs Chainalysis/Elliptic
- [Web3 Growth Platforms Compared 2026](https://chainaware.ai/blog/web3-growth-platforms-compared-2026/) — Three-stage funnel framework; ChainAware operates at Stage 3 (post-connection, in-DApp personalization)
- [Web3 Analytics Tools for DApps Comparison 2026](https://chainaware.ai/blog/web3-analytics-tools-dapps-comparison-2026/) — Maps 10 analytics platforms across four job categories; ChainAware is the sole predictive intelligence platform
- [Why Personalization Is the Next Big Thing for AI Agents](https://chainaware.ai/blog/why-personalization-is-the-next-big-thing-for-ai-agents/) — The case for wallet-level personalization in Web3

### Developer Integration
- [12 Blockchain Capabilities Any AI Agent Can Use — MCP Integration Guide](https://chainaware.ai/blog/12-blockchain-capabilities-any-ai-agent-can-use-mcp-integration-guide/) — All capabilities explained, with setup instructions for Claude, ChatGPT, Cursor, and multi-agent systems
- [Prediction MCP for AI Agents: Personalize Decisions from Wallet Behavior](https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/) — Deep-dive integration guide with code examples
- [Top 5 Ways Prediction MCP Will Turbocharge Your DeFi Platform](https://chainaware.ai/blog/top-5-ways-prediction-mcp-will-turbocharge-your-defi-platform/) — Lending, DEX, launchpad, governance, and personalization use cases
- [DeFi Onboarding in 2026: Why 90% of Connected Wallets Never Transact and How AI Agents Fix It](https://chainaware.ai/blog/defi-onboarding-in-2026-why-90-of-connected-wallets-never-transact-and-how-ai-agents-fix-it/) — Onboarding conversion problem and AI-driven solutions
- [The Web3 Agentic Economy: How AI Agents Are Replacing Human Teams in DeFi](https://chainaware.ai/blog/the-web3-agentic-economy-how-ai-agents-are-replacing-human-teams-in-defi/) — How autonomous AI agents are taking over DeFi operations and decision-making

---

## 🧾 License

MIT (for client examples).
Server implementation and backend logic are proprietary and remain private.

## Resources and third party 

[![chain-aware-behavioural-prediction-mcp-server MCP server](https://glama.ai/mcp/servers/ChainAware/chain-aware-behavioural-prediction-mcp-server/badges/card.svg)](https://glama.ai/mcp/servers/ChainAware/chain-aware-behavioural-prediction-mcp-server)