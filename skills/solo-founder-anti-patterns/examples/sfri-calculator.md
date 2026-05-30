# SFRI Calculator: Step-by-Step Walkthroughs

This document provides complete worked examples of the Solo Founder Risk Index (SFRI) calculation for different project scenarios. Use these as templates when evaluating your own projects.

## How to Use This Guide

1. **Choose a similar scenario** to your project from the examples below
2. **Follow the scoring process** step-by-step
3. **Adapt the questions** to your specific context
4. **Calculate your SFRI** using the weighted formula
5. **Compare to thresholds** to assess viability

## Example 1: SaaS Invoicing Tool for Freelancers

### Project Description
Building a simple invoicing tool specifically for freelance developers and designers. Allows creating invoices, sending them via email, and tracking payment status. Pricing: $19/month.

### Dimension 1: Validation and Market Risk (VMR)

#### 1.1 Problem Specificity (Score: 9/10)

**Question**: Is this solving a daily annoyance or a hypothetical nice-to-have?

**Evidence**:
- Freelancers create 2-10 invoices per month (weekly task)
- Current solutions: Manual Word/Excel templates (time-consuming), FreshBooks (too complex), PayPal invoicing (unprofessional)
- Pain point: "I spend 30 minutes per invoice on formatting and tracking payments"

**Reasoning**: This is a recurring, measurable pain (30 min/invoice × 5 invoices/month = 2.5 hours wasted monthly). Not daily, but frequent and painful enough.

**Score**: **9/10** (weekly recurring pain with measurable time loss)

#### 1.2 Willingness to Pay (Score: 10/10)

**Question**: Have you observed customers paying for this solution or manual workarounds?

**Evidence**:
- FreshBooks: $15-50/month, hundreds of thousands of paying customers
- Wave: Free tier exists, but paid tier is $16/month
- Invoice Ninja: Open source but has cloud hosted paid tier at $10/month
- Some freelancers pay VAs $20-30/hour to manage invoicing

**Reasoning**: Clear evidence of willingness to pay. Multiple competitors have paying customers at similar price points. Even manual workarounds (VAs) cost more than proposed pricing.

**Score**: **10/10** (strong payment evidence across multiple competitors)

#### 1.3 Customer Proximity (Score: 10/10)

**Question**: Can you reach and talk to target users without paid acquisition?

**Evidence**:
- You ARE a freelance developer (perfect founder-market fit)
- Active in 3 freelance Slack communities (1,500+ members combined)
- Know 20+ freelance developers personally from past contracts
- Can post in communities and get feedback within 24 hours

**Reasoning**: You are the target user AND have direct access to hundreds more exactly like you. No cold outreach needed.

**Score**: **10/10** (you are the user + direct community access)

#### 1.4 Market Bubble Risk (Score: 8/10)

**Question**: Is this product for other indie hackers/developers/makers?

**Evidence**:
- Target market: All freelancers (developers, designers, writers, consultants)
- Developers/designers are subset, but freelancing is much broader market
- Many freelancers are not "indie hackers" or "makers" (e.g., freelance accountants, lawyers, translators)

**Reasoning**: While you're starting with developer/designer freelancers (slightly in the bubble), the product applies to all freelancers. Natural expansion path to broader market. Not purely indie hacker tools.

**Score**: **8/10** (adjacent to bubble but broader market exists)

**Red flags check**: None triggered

#### VMR Calculation

```
VMR = (9 + 10 + 10 + 8) / 4 = 37 / 4 = 9.25
```

**Assessment**: Excellent validation. Strong problem, proven willingness to pay, perfect customer access, broad market.

---

### Dimension 2: Product and Technical Risk (PTR)

#### 2.1 Stack Simplicity (Score: 10/10)

**Question**: Are you using technologies you could learn in a weekend or already know deeply?

**Evidence**:
- Planning to use: Rails (5 years experience), PostgreSQL (familiar), Heroku (deployed 10 projects)
- Frontend: Vanilla JavaScript + Tailwind CSS (both familiar)
- Payments: Stripe (integrated before, have working code samples)

**Reasoning**: Using stack you know extremely well. Could start building today without tutorials. Have deployed similar projects before.

**Score**: **10/10** (expert-level familiarity with entire stack)

#### 2.2 Infrastructure Complexity (Score: 9/10)

**Question**: Is a simple monolith sufficient, or does this require complex infrastructure?

**Evidence**:
- Architecture: Rails monolith
- Database: Single PostgreSQL instance (managed by Heroku)
- Email: SendGrid integration
- Payments: Stripe webhooks
- Hosting: Heroku (one-click deploy)
- No queues, no Redis, no microservices

**Reasoning**: Simple monolith deployed to Heroku. Entire infrastructure is managed services. Can deploy in 10 minutes.

**Score**: **9/10** (monolith + managed services, loses 1 point for Heroku cost vs VPS)

#### 2.3 Feature Creep Control (Score: 8/10)

**Question**: Is there a clearly defined "95% ready" line, or is the scope unbounded?

**Evidence**:
- MVP features (Must Have):
  1. Create invoice
  2. Send invoice via email
  3. Track payment status (paid/unpaid)
  4. Basic invoice template
- Explicitly cut (Won't Have in MVP):
  - Recurring invoices
  - Multiple invoice templates
  - Time tracking
  - Expense management
  - Multi-currency
  - Client portal

**Reasoning**: Clear 4-feature MVP. Explicit "Won't Have" list prevents creep. Scope is well-defined.

**Score**: **8/10** (clear MVP, but could be tighter - might be tempted to add "just one more" template)

#### 2.4 Maintenance Tax (Score: 9/10)

**Question**: Will this feature require ongoing manual intervention or is it automated?

**Evidence**:
- Onboarding: Self-service sign-up via Stripe
- Billing: Automated via Stripe (webhooks handle everything)
- Email sending: Automated via SendGrid
- Support: FAQ + email support (manageable at small scale)
- No manual data entry required

**Reasoning**: Fully automated billing and core features. Only manual work is support emails, which scale logarithmically (same questions repeatedly, can build FAQ).

**Score**: **9/10** (mostly automated, loses 1 point for manual support inbox)

**Red flags check**: None triggered

#### PTR Calculation

```
PTR = (10 + 9 + 8 + 9) / 4 = 36 / 4 = 9.0
```

**Assessment**: Very low technical risk. Familiar stack, simple infrastructure, controlled scope, minimal maintenance burden.

---

### Dimension 3: Growth and Leanness Risk (GLR)

#### 3.1 Acquisition Strategy (Score: 8/10)

**Question**: Is there a realistic path to organic customer acquisition?

**Evidence**:
- SEO opportunity: "invoice template for [freelance niche]" - 100+ long-tail keywords with low competition
- Content marketing: Blog about freelance finances, invoicing best practices (you have expertise)
- Community: Can share in 3 Slack communities organically (not spam)
- Word of mouth: Freelancers talk to other freelancers
- No paid ads budget needed

**Reasoning**: Multiple organic channels. SEO is proven for invoicing tools. Existing community access. Content marketing plays to your strengths.

**Score**: **8/10** (strong organic strategy, loses points for competitive SEO market)

#### 3.2 Automation Potential (Score: 10/10)

**Question**: Can the core value be delivered by automated systems ("robots")?

**Evidence**:
- Invoice creation: Pure software (user fills form, PDF generated)
- Email sending: Automated via SendGrid
- Payment tracking: Automated via Stripe webhooks
- Reminders: Could add cron job for automated reminders
- Zero human intervention needed for core value delivery

**Reasoning**: This is pure automation. No manual work required to deliver value to customers.

**Score**: **10/10** (100% automated value delivery)

#### 3.3 Unit Economics (Score: 7/10)

**Question**: Is the average revenue per user (ARPU) high enough to justify the support burden?

**Evidence**:
- Pricing: $19/month = $228/year ARPU
- To reach $10k MRR: Need ~526 customers
- Estimated support: 5 hours/week at 500 customers (based on similar tools)
- Support:revenue ratio: 20 hours/month ÷ $10k = $500/hour effective rate (good)

**Reasoning**: ARPU is decent for a simple tool. Need ~500 customers for sustainability, which is achievable but not trivial. Support burden manageable with FAQ + automation.

**Score**: **7/10** (workable economics, but need significant user base; higher pricing like $49/month would score 9/10)

#### 3.4 Founder-Market Fit (Score: 10/10)

**Question**: Does this project intrinsically excite you for a 5-year horizon?

**Evidence**:
- You've been frustrated with invoicing for 3 years as a freelancer
- You would use this product yourself daily/weekly
- Passionate about helping freelancers succeed (you identify as one)
- Excited to talk about freelance business operations for hours
- This scratches a personal itch

**Reasoning**: Perfect founder-market fit. You are the user, you feel the pain, you'd build this even if it didn't make money (but it will).

**Score**: **10/10** (intrinsic motivation, personal passion, would use yourself)

**Red flags check**: None triggered

#### GLR Calculation

```
GLR = (8 + 10 + 7 + 10) / 4 = 35 / 4 = 8.75
```

**Assessment**: Strong growth potential with organic channels and perfect founder fit. Unit economics require scale but are sustainable.

---

### Final SFRI Calculation

```
SFRI = (0.5 × VMR) + (0.3 × PTR) + (0.2 × GLR)
SFRI = (0.5 × 9.25) + (0.3 × 9.0) + (0.2 × 8.75)
SFRI = 4.625 + 2.7 + 1.75
SFRI = 9.075
```

### Interpretation

**Score**: **9.1 / 10**
**Category**: **Highly Viable "Scrappy" Project**

**Recommendation**: **Ship this immediately.** This project has all the hallmarks of successful solo founder projects:
- Strong validation (VMR: 9.25)
- Low technical risk (PTR: 9.0)
- Sustainable growth path (GLR: 8.75)
- You are the user
- Simple, proven tech stack
- Clear organic acquisition strategy

**Action items**:
1. Build MVP (4 features) in 2-3 weeks
2. Launch to your Slack communities for feedback
3. Iterate based on early user feedback
4. Focus on SEO content marketing while building

**Potential improvements to reach 9.5+**:
- Increase pricing to $29-49/month (improves Unit Economics to 9/10)
- Partner with freelance community influencers (improves Acquisition to 9/10)

---

## Example 2: AI-Powered Social Media Scheduler for Indie Hackers

### Project Description
Building a Twitter/LinkedIn scheduler with AI-generated post suggestions. Helps indie hackers build in public. Pricing: $15/month.

### Dimension 1: Validation and Market Risk (VMR)

#### 1.1 Problem Specificity (Score: 4/10)

**Question**: Is this solving a daily annoyance or a hypothetical nice-to-have?

**Evidence**:
- Indie hackers "should" tweet regularly, but is it painful or just advisable?
- Current solutions: Buffer, Hyperfury, Typefully (many options exist)
- Pain point: "I forget to tweet" (not "I waste hours tweeting")

**Reasoning**: This is a nice-to-have, not a daily pain. Forgetting to tweet doesn't cost money or cause measurable loss. It's aspirational ("I should tweet more") rather than solving existing pain.

**Score**: **4/10** (mild annoyance, not critical pain)

#### 1.2 Willingness to Pay (Score: 3/10)

**Question**: Have you observed customers paying for this solution or manual workarounds?

**Evidence**:
- Competitors exist (Hyperfury: $19/month, Typefully: $12.50/month)
- BUT: Market is saturated with competitors
- No evidence people pay for manual workarounds (no VAs for tweeting)
- High churn in this category (users cancel after a few months)

**Reasoning**: Some willingness to pay exists (competitors have customers), but saturated market and high churn suggest weak retention. No payment for manual alternatives.

**Score**: **3/10** (weak evidence, saturated market, high churn)

#### 1.3 Customer Proximity (Score: 6/10)

**Question**: Can you reach and talk to target users without paid acquisition?

**Evidence**:
- Active on Twitter (2,000 followers)
- In indie hacker communities
- Can tweet about it and get feedback
- But: Reaching people on Twitter ≠ converting them to paying customers

**Reasoning**: Good access to target audience for feedback, but audience is on Twitter (where they already are). Conversion from "Twitter user" to "paying customer" is the challenge.

**Score**: **6/10** (can reach users, but conversion uncertain)

#### 1.4 Market Bubble Risk (Score: 1/10)

**Question**: Is this product for other indie hackers/developers/makers?

**Evidence**:
- Explicitly for "indie hackers"
- Marketing is "build in public" (indie hacker concept)
- Users are other makers/builders
- This is the definition of the indie hacker bubble

**Reasoning**: Squarely in the bubble. Building tools for indie hackers to build in public is peak circular economy.

**Score**: **1/10** (core bubble anti-pattern)

**Red flag triggered**: ✗ Explicitly for indie hackers (auto-score 1-3)

#### VMR Calculation

```
VMR = (4 + 3 + 6 + 1) / 4 = 14 / 4 = 3.5
```

**Assessment**: Weak validation. Not solving critical pain, saturated market, in the indie hacker bubble.

---

### Dimension 2: Product and Technical Risk (PTR)

#### 2.1 Stack Simplicity (Score: 7/10)

**Question**: Are you using technologies you could learn in a weekend or already know deeply?

**Evidence**:
- Planning: Next.js (familiar, 2 years experience)
- Database: Supabase (some experience)
- AI: OpenAI API (new, but simple integration)
- OAuth: Twitter/LinkedIn APIs (documentation is good)

**Reasoning**: Mostly familiar stack, but AI integration and OAuth are new complexity. Not expert-level, but manageable.

**Score**: **7/10** (familiar but not expert, some new integrations)

#### 2.2 Infrastructure Complexity (Score: 7/10)

**Question**: Is a simple monolith sufficient?

**Evidence**:
- Next.js app deployed to Vercel
- Supabase for database + auth
- Cron jobs for scheduled posting
- Redis for queue management (scheduled posts)
- Webhooks for Twitter/LinkedIn

**Reasoning**: Moderately simple, but requires queue system, cron jobs, and multiple API integrations. More moving parts than ideal.

**Score**: **7/10** (more complex than monolith, but managed services help)

#### 2.3 Feature Creep Control (Score: 5/10)

**Question**: Is there a clearly defined "95% ready" line?

**Evidence**:
- MVP features:
  1. Schedule tweets
  2. AI post suggestions
  3. Thread composer
  4. Analytics dashboard
  5. LinkedIn support
  6. Image uploads
  7. Link shortening
- That's 7 features for "MVP"

**Reasoning**: MVP is already bloated. Trying to compete with established players feature-for-feature. No clear "Won't Have" list.

**Score**: **5/10** (MVP scope is too large, creeping toward feature parity)

#### 2.4 Maintenance Tax (Score: 4/10)

**Question**: Will this require ongoing manual intervention?

**Evidence**:
- Twitter API rate limits require monitoring
- Occasional failed posts need manual retry
- AI suggestions might need content moderation
- Support for "why didn't my post send?" queries
- OAuth tokens expire, need refresh handling

**Reasoning**: Significant manual maintenance. API dependencies create ongoing support burden. Rate limits are unpredictable.

**Score**: **4/10** (high maintenance due to API dependencies and support burden)

**Red flag triggered**: None (but approaching threshold)

#### PTR Calculation

```
PTR = (7 + 7 + 5 + 4) / 4 = 23 / 4 = 5.75
```

**Assessment**: Moderate technical risk. Familiar stack but complex integrations and high maintenance burden.

---

### Dimension 3: Growth and Leanness Risk (GLR)

#### 3.1 Acquisition Strategy (Score: 3/10)

**Question**: Is there a realistic path to organic customer acquisition?

**Evidence**:
- SEO: Highly competitive ("social media scheduler", "Twitter scheduler")
- Content marketing: Possible, but many competitors doing this
- Word of mouth: Maybe, but high churn limits referrals
- Organic social: Can tweet about it, but need to stand out
- Realistic path: Probably need paid ads to compete

**Reasoning**: Organic is difficult in saturated market. SEO is expensive/slow. Social media marketing for a social media tool is meta but not unique.

**Score**: **3/10** (organic possible but unlikely to scale without paid ads)

#### 3.2 Automation Potential (Score: 8/10)

**Question**: Can the core value be delivered by automated systems?

**Evidence**:
- Scheduling: Fully automated
- AI suggestions: Fully automated (API call)
- Posting: Automated via API
- Billing: Stripe automation
- Minimal human intervention needed

**Reasoning**: Core product is automatable. Only support is manual.

**Score**: **8/10** (mostly automated, loses points for API dependency risks)

#### 3.3 Unit Economics (Score: 2/10)

**Question**: Is the ARPU high enough to justify support burden?

**Evidence**:
- Pricing: $15/month = $180/year ARPU
- To reach $10k MRR: Need ~667 customers
- High churn in this space (3-6 month avg lifetime)
- Support burden: Medium (API issues, failed posts)
- Need massive scale to be sustainable

**Reasoning**: Low pricing + high user count needed + high churn = unsustainable economics. Would need 1,000+ active customers to hit $10k MRR with churn factored in.

**Score**: **2/10** (poor economics, need massive scale)

**Red flag triggered**: ✗ Pricing under $10/month for complex product (auto-score 1-3)

#### 3.4 Founder-Market Fit (Score: 5/10)

**Question**: Does this project intrinsically excite you for a 5-year horizon?

**Evidence**:
- You tweet occasionally but aren't passionate about it
- Building because "AI is hot" and "Twitter tools are popular"
- Wouldn't use this yourself (you prefer manual tweeting)
- Interest is professional, not personal

**Reasoning**: Opportunity-driven, not passion-driven. Would likely pivot if not profitable in 6 months.

**Score**: **5/10** (mild interest, mostly chasing trends)

#### GLR Calculation

```
GLR = (3 + 8 + 2 + 5) / 4 = 18 / 4 = 4.5
```

**Assessment**: Weak growth prospects. Hard to acquire customers organically, poor unit economics, low founder passion.

---

### Final SFRI Calculation

```
SFRI = (0.5 × VMR) + (0.3 × PTR) + (0.2 × GLR)
SFRI = (0.5 × 3.5) + (0.3 × 5.75) + (0.2 × 4.5)
SFRI = 1.75 + 1.725 + 0.9
SFRI = 4.375
```

### Interpretation

**Score**: **4.4 / 10**
**Category**: **Critical Anti-Patterns Detected - High Failure Risk**

**Recommendation**: **Do NOT build this.** Multiple critical anti-patterns:

**Red flags**:
1. ✗ Indie hacker bubble (VMR: Market Bubble = 1)
2. ✗ Low pricing + high scale needed (GLR: Unit Economics = 2)
3. Weak validation (VMR: 3.5)
4. Poor economics (GLR: 4.5)

**Why this will likely fail**:
- Not solving critical pain (nice-to-have)
- Saturated market with many competitors
- Squarely in indie hacker bubble (circular economy)
- Need 667+ customers to reach $10k MRR
- High churn expected
- No organic acquisition advantage
- Opportunity-driven, not passion-driven

**Alternative paths**:
1. **Pivot to broader market**: Social media tools for local businesses, real estate agents, etc. (escape the bubble)
2. **Increase pricing**: $49-99/month for agencies/businesses (fix unit economics)
3. **Find different niche**: Instead of "for indie hackers", target specific industry (real estate, fitness coaches, etc.)
4. **Abandon for better opportunity**: Use SFRI to evaluate other ideas scoring 7+

**If you insist on building**:
- Test willingness to pay FIRST (pre-sales, landing page with pricing)
- Target businesses, not indie hackers
- Price at $49/month minimum
- Focus on one platform (Twitter OR LinkedIn, not both)
- Re-calculate SFRI after pivots

---

## Example 3: Kubernetes Deployment Simplification Tool

### Project Description
CLI tool that simplifies deploying apps to Kubernetes. Target users: DevOps engineers and backend developers at small-mid companies. Pricing: $99/month per team.

### Quick SFRI Calculation

#### VMR: 7.0
- Problem Specificity: 8 (K8s is genuinely complex and painful)
- Willingness to Pay: 9 (companies pay for DevOps tools)
- Customer Proximity: 5 (can reach via cold outreach, some network)
- Market Bubble: 6 (adjacent to indie hackers but broader DevOps market)

#### PTR: 5.5
- Stack Simplicity: 4 (need to learn Go ecosystem deeply)
- Infrastructure: 3 (need K8s cluster to test, inherently complex)
- Feature Creep: 7 (clear MVP: simple deployments)
- Maintenance Tax: 8 (mostly automated once working)

#### GLR: 9.0
- Acquisition: 9 (great SEO opportunity, content marketing)
- Automation: 10 (pure automation)
- Unit Economics: 9 ($99/month, only need ~100 teams for $10k MRR)
- Founder-Market Fit: 8 (DevOps background, passionate about infrastructure)

```
SFRI = (0.5 × 7.0) + (0.3 × 5.5) + (0.2 × 9.0)
SFRI = 3.5 + 1.65 + 1.8 = 6.95
```

**Category**: **Moderate Risk - Needs Optimization**

**Recommendation**: Strong market and growth potential, but technical complexity is concerning. Before building:
1. Validate with pre-sales (get 10 companies to commit $99/month)
2. Simplify tech if possible (use existing K8s libraries, don't build from scratch)
3. Consider if you can build MVP without being K8s expert
4. If PTR improves to 7+, overall SFRI hits 8.0+ (viable)

---

## Using These Examples

### When to Score Yourself

**Do a full SFRI calculation when**:
- Starting a new project (before writing code)
- Deciding between multiple ideas
- Pivoting existing project
- Feeling stuck/unsure if you should continue

**Do a quick gut-check when**:
- Adding a major feature
- Considering technical stack change
- Quarterly health check

### How to Be Honest

**Common biases to avoid**:
1. **Optimism bias**: "I think users will love this" → Score based on evidence, not hopes
2. **Sunk cost**: "I've already spent 100 hours" → Score the idea as if starting fresh
3. **Competitor envy**: "X competitor has this" → Score based on your users, not their features
4. **Aspiration vs reality**: "Users could eventually…" → Score current state, not future roadmap

### Improving Your Score

**If SFRI < 6.5, focus on weakest dimension**:

**Low VMR (<6)**:
- Talk to more users
- Get pre-sales commitments
- Validate willingness to pay with real money
- Escape indie hacker bubble (target broader market)

**Low PTR (<6)**:
- Simplify tech stack to what you know
- Cut features ruthlessly (fewer is better)
- Move to monolith if using microservices
- Reduce infrastructure complexity

**Low GLR (<6)**:
- Find organic acquisition channel
- Increase pricing (fix unit economics)
- Build more automation (reduce manual delivery)
- Assess founder-market fit honestly (pivot if mismatched)

**Action**: Recalculate SFRI after making improvements. Goal is 8.0+ before building.

---

## Blank SFRI Template

Copy this template to score your own projects:

### Project: [Your Project Name]

**Description**: [1-2 sentence description]

#### VMR Scores
- Problem Specificity: ___ / 10 (Reasoning: ___)
- Willingness to Pay: ___ / 10 (Reasoning: ___)
- Customer Proximity: ___ / 10 (Reasoning: ___)
- Market Bubble: ___ / 10 (Reasoning: ___)
- **VMR = ___**

#### PTR Scores
- Stack Simplicity: ___ / 10 (Reasoning: ___)
- Infrastructure: ___ / 10 (Reasoning: ___)
- Feature Creep: ___ / 10 (Reasoning: ___)
- Maintenance Tax: ___ / 10 (Reasoning: ___)
- **PTR = ___**

#### GLR Scores
- Acquisition: ___ / 10 (Reasoning: ___)
- Automation: ___ / 10 (Reasoning: ___)
- Unit Economics: ___ / 10 (Reasoning: ___)
- Founder-Market Fit: ___ / 10 (Reasoning: ___)
- **GLR = ___**

#### Final SFRI
```
SFRI = (0.5 × ___) + (0.3 × ___) + (0.2 × ___)
SFRI = ___ + ___ + ___ = ___
```

**Category**: ___
**Recommendation**: ___

---

## Next Steps

After calculating your SFRI:

**If SFRI ≥ 8.5**: Ship it! Focus on execution.
**If SFRI 6.5-8.4**: Improve weak dimensions before building.
**If SFRI < 6.5**: Seriously reconsider or pivot significantly.

For detailed scoring criteria, see `references/validation-framework.md`.
