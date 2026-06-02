# Metrics & Benchmarks Reference

## Unit Economics Calculations

### LTV (Lifetime Value)
```
LTV = (ARPU × Gross Margin) / Monthly Churn Rate
```
Or for cohort-based:
```
LTV = Sum of (Monthly Revenue × Retention Rate) over customer lifetime
```

### CAC (Customer Acquisition Cost)
```
CAC = (Sales + Marketing Spend) / New Customers Acquired
```
Include: salaries, commissions, advertising, tools, events, content production

### CAC Payback Period
```
CAC Payback (months) = CAC / (Monthly ARPU × Gross Margin)
```

### LTV:CAC Ratio
| Ratio | Interpretation |
|-------|----------------|
| <1:1 | Losing money on every customer |
| 1-2:1 | Unsustainable, need to improve |
| 3:1 | Healthy minimum threshold |
| 5:1+ | Excellent, may be underinvesting in growth |
| 7-8:1 | Best-in-class |

## SaaS Metrics Benchmarks

### Churn Rates by Segment
| Segment | Monthly Churn | Annual Churn |
|---------|---------------|--------------|
| SMB | 3-5% | 30-50% |
| Mid-Market | 1-2% | 10-20% |
| Enterprise | 0.5-1% | 5-10% |
| Best-in-class | <1% monthly | <10% annual |

### Net Revenue Retention (NRR)
```
NRR = (Starting MRR + Expansion - Churn - Contraction) / Starting MRR
```
| NRR | Interpretation |
|-----|----------------|
| <90% | Leaky bucket, growth unsustainable |
| 90-100% | Acceptable, but limited expansion |
| 100-110% | Good, expansion offsetting churn |
| 110-130% | Excellent |
| >130% | World-class (Snowflake, Twilio territory) |

### Gross Margin Targets
| Business Type | Target Gross Margin |
|---------------|---------------------|
| Pure SaaS | 75-85% |
| SaaS + Services | 60-70% |
| Marketplace | 40-60% |
| Hardware + Software | 30-50% |

## Cash Flow Metrics

### Runway Calculation
```
Runway (months) = Cash Balance / Monthly Burn Rate
```
Use trailing 3-month average burn for accuracy.

### Burn Multiple
```
Burn Multiple = Net Burn / Net New ARR
```
| Multiple | Rating |
|----------|--------|
| <1x | Excellent efficiency |
| 1-1.5x | Good |
| 1.5-2x | Concerning |
| >2x | Inefficient, requires correction |

### Cash Conversion Score
```
CCS = (Cash from Operations / Net Income) × 100
```
Target: >100% (generating more cash than accounting profit)

## Revenue Efficiency

### Magic Number (Sales Efficiency)
```
Magic Number = (QoQ ARR Growth) / (Prior Quarter S&M Spend)
```
| Score | Interpretation |
|-------|----------------|
| <0.5 | Inefficient, reduce spend or improve conversion |
| 0.5-0.75 | Acceptable |
| 0.75-1.0 | Good |
| >1.0 | Excellent, consider increasing investment |

### Revenue per Employee
| ARR Stage | Target RPE |
|-----------|------------|
| $1-5M | $110-150K |
| $5-10M | $150-200K |
| $10-50M | $200-250K |
| $50M+ | $300-400K+ |

Bootstrapped companies typically achieve 40-70% higher RPE than VC-backed at same stage.

## Working Capital Metrics

### Days Sales Outstanding (DSO)
```
DSO = (Accounts Receivable / Total Credit Sales) × Days in Period
```
| DSO | Rating |
|-----|--------|
| <30 days | Excellent |
| 30-45 days | Good |
| 45-60 days | Needs attention |
| >60 days | Problem requiring immediate action |

### Days Payable Outstanding (DPO)
```
DPO = (Accounts Payable / COGS) × Days in Period
```
Target: Negotiate highest DPO possible while maintaining vendor relationships

### Cash Conversion Cycle
```
CCC = DIO + DSO - DPO
```
(DIO = Days Inventory Outstanding, typically 0 for SaaS)

SaaS with annual prepay can achieve CCC of -30 to -90 days.

## Spending Benchmarks by ARR

### $1-3M ARR (Early Stage)
| Category | % of ARR |
|----------|----------|
| Sales | 15-20% |
| Marketing | 10-15% |
| R&D | 30-40% |
| Customer Success | 10-15% |
| G&A | 15-20% |

### $3-10M ARR (Growth Stage)
| Category | % of ARR |
|----------|----------|
| Sales | 10-15% |
| Marketing | 8-12% |
| R&D | 25-30% |
| Customer Success | 8-12% |
| G&A | 12-15% |

### $10M+ ARR (Scale Stage)
| Category | % of ARR |
|----------|----------|
| Sales | 8-12% |
| Marketing | 6-10% |
| R&D | 20-25% |
| Customer Success | 6-10% |
| G&A | 10-12% |

## Rule of 40 Scenarios

| Growth Rate | Required Margin | Example |
|-------------|-----------------|---------|
| 50% | -10% (can burn) | Hypergrowth mode |
| 40% | 0% | Breakeven growth |
| 30% | 10% | Balanced |
| 20% | 20% | Profitable growth |
| 10% | 30% | Mature, profitable |
| 0% | 40% | Cash cow |

Median SaaS: 34% (most don't hit 40)
Top quartile bootstrapped: 50%+

## Forecast Accuracy Metrics

### MAPE (Mean Absolute Percentage Error)
```
MAPE = (1/n) × Σ |Actual - Forecast| / |Actual| × 100
```
| MAPE | Rating |
|------|--------|
| <5% | Excellent |
| 5-10% | Good |
| 10-20% | Acceptable |
| >20% | Needs improvement |

Track separately for:
- Revenue (target 5-10% MAPE)
- Expenses (target 10-15% MAPE)
- Cash flow (target 10-15% MAPE)
