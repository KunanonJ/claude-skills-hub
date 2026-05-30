# Solo Founder Risk Index (SFRI): Complete Validation Framework

This document provides the complete scoring rubric for the Solo Founder Risk Index, a quantitative framework for assessing project viability and identifying anti-patterns before they become fatal.

## Overview

The SFRI evaluates projects across three weighted dimensions:
1. **Validation and Market Risk (VMR)**: 50% weight
2. **Product and Technical Risk (PTR)**: 30% weight
3. **Growth and Leanness Risk (GLR)**: 20% weight

Each dimension is scored 1-10 (low score = high risk), then combined using the weighted formula:

```
SFRI = (0.5 × VMR) + (0.3 × PTR) + (0.2 × GLR)
```

## Dimension 1: Validation and Market Risk (VMR)

**Weight: 50%** - This is the most critical dimension because building the wrong thing is more expensive than building the right thing poorly.

### 1.1 Problem Specificity

**Question**: Is this solving a daily annoyance or a hypothetical nice-to-have?

**Scoring**:
- **10**: Daily, recurring pain point that causes measurable loss (time, money, frustration)
  - Example: "I waste 2 hours every day manually copying data between systems"
  - Example: "I miss customer emails because they're buried in spam"
- **7-9**: Frequent annoyance (weekly) with clear impact
  - Example: "Every week I have to manually compile team reports from 5 different tools"
- **4-6**: Occasional problem (monthly) or moderate convenience improvement
  - Example: "Once a month I need to export analytics in a specific format"
- **1-3**: Hypothetical or rare problem, idea-driven rather than pain-driven
  - Example: "Wouldn't it be cool if..." or "I thought it might be useful to..."
  - Example: Problems that only occur during edge cases

**Red flags** (auto-score 1-3):
- No specific person has articulated this exact problem
- The problem is based on "I think people might want..."
- Solution looking for a problem

### 1.2 Willingness to Pay

**Question**: Have you observed customers paying for this solution or manual workarounds?

**Scoring**:
- **10**: Direct evidence of payment for this exact solution
  - Competitors have paying customers
  - People pay for manual services that solve this (VAs, consultants, agencies)
  - Existing SaaS tools in this space have public revenue figures
- **7-9**: Adjacent evidence of payment
  - People pay for partial solutions
  - Companies budget for this category of tools
  - Job postings exist for people to do this manually
- **4-6**: Indirect signals of value
  - Free users willing to provide detailed feedback
  - High engagement with free alternatives
  - People build internal tools for this
- **1-3**: No payment evidence
  - Only free alternatives exist
  - "I'd pay for this" statements without credit card
  - No comparable products have succeeded

**Red flags** (auto-score 1-3):
- Graveyard of failed competitors in this space
- Only free open-source solutions exist (suggests no willingness to pay)
- "Friends and family" sign-ups only

### 1.3 Customer Proximity

**Question**: Can you reach and talk to target users without paid acquisition?

**Scoring**:
- **10**: You ARE the target user and know 10+ others exactly like you
  - Example: Developer building tools for developers at your company size
  - Example: Freelancer building tools for other freelancers in your network
- **7-9**: Direct access to target community
  - Active member of Slack/Discord/forums where target users congregate
  - Can post and get feedback within 24 hours
  - Know target users personally through work/network
- **4-6**: Indirect access
  - Can find target users through cold outreach
  - Have to pay for access (ads, sponsorships)
  - One or two degrees of separation
- **1-3**: No access without significant effort
  - Need to build audience from scratch
  - Cold LinkedIn/email only path
  - Don't personally know anyone in target market

**Red flags** (auto-score 1-3):
- Target users are "everyone" or "businesses"
- Geographic or language barriers to access
- Target users in heavily gatekept industries (enterprise buyers, government)

### 1.4 Market Bubble Risk

**Question**: Is this product for other indie hackers/developers/makers?

**Scoring**:
- **10**: Target market is established industries outside tech/maker space
  - Example: Workflow tools for dental offices, landscaping companies, restaurants
  - Example: B2B SaaS for manufacturing, logistics, healthcare
- **7-9**: Adjacent to maker space but broader appeal
  - Example: Creator economy tools (YouTubers, newsletter writers, podcasters)
  - Example: SMB tools that happen to include indie businesses
- **4-6**: Partially in the bubble
  - Example: Developer tools with enterprise applications
  - Example: Productivity tools marketed to "makers" but usable by anyone
- **1-3**: Squarely in the indie hacker bubble
  - Example: Landing page builders for indie hackers
  - Example: Tweet schedulers for "building in public"
  - Example: AI logo generators for startups
  - Example: Tools to help indie hackers track MRR

**Red flags** (auto-score 1-3):
- Primary distribution channel is Twitter/Product Hunt
- TAM calculation assumes "all indie hackers"
- Marketing copy uses phrases like "for makers" or "for solopreneurs"

### VMR Calculation

```
VMR = (Problem_Specificity + Willingness_to_Pay + Customer_Proximity + Market_Bubble_Risk) / 4
```

**Example: High VMR (9.25)**
- Problem Specificity: 10 (dental offices waste 3 hrs/day on appointment reminders)
- Willingness to Pay: 10 (offices currently pay VAs $15/hr to make calls)
- Customer Proximity: 8 (partner is a dentist, knows 20 local practices)
- Market Bubble: 9 (healthcare industry, not maker space)
- **VMR = (10+10+8+9)/4 = 9.25**

**Example: Low VMR (3.5)**
- Problem Specificity: 3 ("wouldn't it be cool if indie hackers could share revenue data")
- Willingness to Pay: 2 (no competitors, only free solutions)
- Customer Proximity: 4 (active on Twitter, could reach indie hackers)
- Market Bubble: 1 (explicitly for indie hackers)
- **VMR = (3+2+4+1)/4 = 2.5**

## Dimension 2: Product and Technical Risk (PTR)

**Weight: 30%** - Technical choices determine velocity and maintenance burden.

### 2.1 Stack Simplicity

**Question**: Are you using technologies you could learn in a weekend or already know deeply?

**Scoring**:
- **10**: Using tools you know extremely well (5+ years experience)
  - Can debug blindfolded
  - Know common pitfalls and workarounds
  - Have deployed similar projects before
- **7-9**: Using "boring" technology with massive community support
  - PHP, Python/Flask, Ruby/Rails, vanilla JavaScript
  - SQLite, PostgreSQL, MySQL
  - Frameworks with 10+ years of Stack Overflow answers
  - Could become productive in a weekend
- **4-6**: Modern but established stack
  - React, Vue, Next.js (if you know them)
  - More complex but well-documented
  - Hiring-friendly if you need help
- **1-3**: Bleeding edge or niche technology
  - Brand new frameworks (less than 2 years old)
  - Obscure languages with small communities
  - "Resume-driven development" choices
  - Would take weeks to become productive

**Red flags** (auto-score 1-3):
- Using this project to "learn" a new language/framework
- Tech stack chosen because "it's what everyone's using now"
- Can't find Stack Overflow answers for common problems

### 2.2 Infrastructure Complexity

**Question**: Is a simple monolith sufficient, or does this require complex infrastructure?

**Scoring**:
- **10**: Single server monolith is sufficient
  - Single process application
  - SQLite or single database
  - Deploying to simple VPS or managed platform (Heroku, Render, Fly.io)
  - No container orchestration needed
- **7-9**: Simple multi-component architecture
  - App server + database (managed)
  - Maybe Redis for caching
  - Standard Docker deployment (not Kubernetes)
  - Managed services for complexity (Auth0, Stripe, SendGrid)
- **4-6**: Moderate complexity
  - Multiple services (but not "microservices architecture")
  - Queue system (Sidekiq, Celery, Bull)
  - CDN and asset pipeline
  - Docker-compose with 3-5 services
- **1-3**: High infrastructure complexity
  - Kubernetes or other orchestration
  - True microservices (5+ separate services)
  - Custom infrastructure code (Terraform, Ansible)
  - Serverless with complex function orchestration
  - "Need to scale to millions" before first customer

**Red flags** (auto-score 1-3):
- Kubernetes mentioned for MVP
- "Microservices" in the architecture doc
- Infrastructure complexity is the selling point
- More than 5 moving parts to deploy

### 2.3 Feature Creep Control

**Question**: Is there a clearly defined "95% ready" line, or is the scope unbounded?

**Scoring**:
- **10**: Single core feature defined, everything else explicitly cut
  - "This does X and only X"
  - Clear one-sentence value proposition
  - Less than 5 user-facing features
  - Explicit "not doing Y, Z" list
- **7-9**: Core features defined with clear MVP scope
  - 5-10 features maximum
  - Each feature necessary for core value prop
  - Nice-to-haves documented but deferred
- **4-6**: Moderate scope with some creep
  - 10-20 features planned
  - Some "wouldn't it be cool if" features included
  - MVP definition keeps expanding
- **1-3**: Unbounded scope
  - "We'll need to compete with X feature-for-feature"
  - Constantly adding features before launch
  - No clear MVP definition
  - "95% ready" for months

**Red flags** (auto-score 1-3):
- Roadmap has more features than weeks until runway ends
- Saying "just one more feature" for 3+ months
- Feature list grows faster than feature completion
- Building "platform" instead of product

### 2.4 Maintenance Tax

**Question**: Will this feature require ongoing manual intervention or is it automated?

**Scoring**:
- **10**: Fully automated, zero human intervention needed
  - Self-service onboarding and billing
  - Automated monitoring and alerting
  - No manual data entry or processing
  - Automated customer support for common issues
- **7-9**: Mostly automated with minimal manual work
  - Onboarding automated, occasional hand-holding
  - Automated billing with rare edge cases
  - Support mostly self-service (docs, FAQ)
  - Manual work scales logarithmically, not linearly
- **4-6**: Significant manual components
  - Some manual onboarding steps
  - Regular manual data processing
  - Support inbox requires daily attention
  - Manual work scales sub-linearly (less than linear but more than log)
- **1-3**: High manual maintenance burden
  - Custom onboarding for each customer
  - Manual billing, invoicing, or data processing
  - Support requires deep expertise for each ticket
  - Manual work scales linearly or worse with users

**Red flags** (auto-score 1-3):
- "White glove onboarding" for low-ticket product
- Agency model (manual work for each customer)
- Custom development for each client
- "Concierge MVP" without automation plan

### PTR Calculation

```
PTR = (Stack_Simplicity + Infrastructure_Complexity + Feature_Creep + Maintenance_Tax) / 4
```

**Example: High PTR (9.0)**
- Stack Simplicity: 10 (Rails developer building Rails app)
- Infrastructure Complexity: 9 (Heroku deployment, Postgres, Redis)
- Feature Creep: 8 (3 core features, clear MVP)
- Maintenance Tax: 9 (fully automated billing and onboarding)
- **PTR = (10+9+8+9)/4 = 9.0**

**Example: Low PTR (3.25)**
- Stack Simplicity: 2 (learning Rust to build this)
- Infrastructure Complexity: 1 (Kubernetes, microservices, service mesh)
- Feature Creep: 5 (MVP keeps growing, but bounded)
- Maintenance Tax: 5 (some manual onboarding, mostly automated)
- **PTR = (2+1+5+5)/4 = 3.25**

## Dimension 3: Growth and Leanness Risk (GLR)

**Weight: 20%** - Sustainable growth without burning cash or time.

### 3.1 Acquisition Strategy

**Question**: Is there a realistic path to organic customer acquisition?

**Scoring**:
- **10**: Multiple organic channels with compounding effects
  - SEO for high-intent keywords (proven with keyword research)
  - Content marketing with distribution built-in (existing audience/network)
  - Community-led growth in accessible communities
  - Engineering as marketing (free tools that drive awareness)
  - Built-in virality (users invite users naturally)
- **7-9**: Strong organic channel + supplementary channels
  - SEO for long-tail keywords
  - Content marketing to build audience from scratch
  - Partner/affiliate program
  - Build in Public momentum
- **4-6**: Organic possible but slow, might need some paid
  - SEO for competitive keywords (will take 12+ months)
  - Content marketing without distribution
  - Organic social (Twitter, LinkedIn) without existing audience
  - Community building from zero
- **1-3**: Paid acquisition required or no clear strategy
  - Only path is paid ads
  - Enterprise sales required (multi-month cycles)
  - Cold outbound only
  - "If we build it they will come"

**Red flags** (auto-score 1-3):
- Only acquisition plan is paid ads
- Depending on "going viral"
- Product Hunt launch is the entire strategy
- No existing audience or distribution

### 3.2 Automation Potential

**Question**: Can the core value be delivered by automated systems ("robots")?

**Scoring**:
- **10**: Core value is pure automation
  - Data aggregation and presentation
  - Automated workflows and triggers
  - Scheduled jobs and monitoring
  - No human in the loop for value delivery
- **7-9**: Mostly automated with minimal human touch
  - AI/ML does the work, human validates
  - Automated processes with edge case handling
  - Self-service tools with optional expert support
- **4-6**: Hybrid automated/manual delivery
  - Software + human expertise required
  - Automated tools + consulting/implementation
  - Product requires ongoing expert intervention
- **1-3**: Manual delivery is the product
  - Agency/consulting model
  - Done-for-you services
  - Custom development for each customer
  - Software is just a thin wrapper on human labor

**Red flags** (auto-score 1-3):
- Revenue scales linearly with your time
- Need to hire people to deliver value
- "Productized service" without path to pure product
- Each customer requires custom work

### 3.3 Unit Economics

**Question**: Is the average revenue per user (ARPU) high enough to justify the support burden?

**Scoring**:
- **10**: High-ticket B2B with enterprise ARPU
  - $500+ per month per customer
  - Annual contracts $5k+
  - Can afford high-touch support for volume of customers needed
- **7-9**: Mid-market B2B or premium prosumer
  - $100-$500 per month
  - Annual contracts $1k-$5k
  - Support burden manageable at scale needed for profitability
- **4-6**: SMB or low-tier B2B
  - $20-$100 per month
  - Need hundreds of customers for sustainability
  - Support burden significant but manageable with automation
- **1-3**: Consumer or micro-business pricing
  - $5-$20 per month
  - Need thousands of customers
  - Support burden prohibitive without extensive automation
  - Ad-supported or freemium (unproven conversion)

**Red flags** (auto-score 1-3):
- Pricing under $10/month for complex product
- Need 10,000+ customers to reach $10k MRR
- Support:revenue ratio looks like consumer app but pricing is consumer

**Framework for support burden**:
```
Support_Sustainability = ARPU / (Expected_Support_Hours_Per_Customer × Your_Hourly_Rate)
```

If ratio < 1, unsustainable. If ratio > 10, healthy margin.

### 3.4 Founder-Market Fit

**Question**: Does this project intrinsically excite you for a 5-year horizon?

**Scoring**:
- **10**: This is your life's work, would do it for free
  - Deep domain expertise
  - Personal passion for the problem
  - Would use this product yourself daily
  - Excited to talk about this problem for hours
- **7-9**: Strong interest and alignment
  - Genuine interest in the domain
  - Would use this product regularly
  - Excited to learn more about this space
  - Comfortable becoming "the expert" in this niche
- **4-6**: Mild interest, mostly opportunity-driven
  - Seems like good business opportunity
  - Willing to learn the domain
  - Could see working on this for 2-3 years
  - Interest is professional, not personal
- **1-3**: Chasing trends or money only
  - "This could make money"
  - No intrinsic interest in problem or users
  - Would quit if it's not profitable in 6 months
  - Picked because "AI is hot" or "everyone's doing X"

**Red flags** (auto-score 1-3):
- Chasing whatever's trending (AI wrappers, crypto, etc.)
- Can't articulate why this problem matters to you personally
- Would switch to different idea if this doesn't work immediately
- Building something you'd never use yourself

### GLR Calculation

```
GLR = (Acquisition_Strategy + Automation_Potential + Unit_Economics + Founder_Market_Fit) / 4
```

**Example: High GLR (8.75)**
- Acquisition Strategy: 9 (SEO for high-intent keywords, existing network)
- Automation Potential: 10 (pure data aggregation, zero human delivery)
- Unit Economics: 8 ($99/month, need 100 customers for $10k MRR)
- Founder-Market Fit: 8 (passionate about domain, would use daily)
- **GLR = (9+10+8+8)/4 = 8.75**

**Example: Low GLR (3.5)**
- Acquisition Strategy: 2 (paid ads only path)
- Automation Potential: 3 (mostly manual service delivery)
- Unit Economics: 4 ($29/month, need 350 customers)
- Founder-Market Fit: 5 (seems interesting, not passionate)
- **GLR = (2+3+4+5)/4 = 3.5**

## Complete SFRI Calculation

### Formula

```
SFRI = (0.5 × VMR) + (0.3 × PTR) + (0.2 × GLR)
```

### Interpretation Thresholds

**8.5 - 10.0: Highly Viable "Scrappy" Project**
- Strong validation signals
- Simple, familiar tech stack
- Organic growth path exists
- Low maintenance burden
- **Action**: Ship immediately. This has all the characteristics of successful solo projects.

**6.5 - 8.4: Moderate Risk - Needs Optimization**
- Some validation, but gaps exist
- Tech stack might be too complex
- Growth strategy unclear
- **Action**: Before building, address specific weak dimensions:
  - If low VMR: Get more validation, talk to more users
  - If low PTR: Simplify stack, cut features, reduce infrastructure
  - If low GLR: Find organic acquisition channel, increase pricing, or improve automation

**Below 6.5: Critical Anti-Patterns - High Failure Risk**
- Weak validation or no market
- Over-engineered or wrong stack
- Unsustainable growth model
- **Action**: Seriously reconsider. Projects in this range have structural problems that make success unlikely. Either pivot significantly or abandon for better opportunity.

## Worked Examples

### Example 1: High SFRI (8.8) - Invoice Automation for Freelancers

**VMR: 9.25**
- Problem Specificity: 10 (freelancers waste 2-3 hrs/week on invoices)
- Willingness to Pay: 10 (FreshBooks, Wave, Invoice Ninja all have paying customers)
- Customer Proximity: 9 (you're a freelancer, know 50+ others)
- Market Bubble: 8 (broader SMB market, not just indie hackers)

**PTR: 8.75**
- Stack Simplicity: 10 (Rails developer, building Rails app)
- Infrastructure: 9 (Heroku + Postgres + Stripe)
- Feature Creep: 7 (MVP is "create invoice, send, track payment" - 3 features)
- Maintenance Tax: 9 (fully automated billing via Stripe, self-service)

**GLR: 8.0**
- Acquisition: 8 (SEO for "invoice template for [profession]", content marketing)
- Automation: 9 (pure software, no manual delivery)
- Unit Economics: 7 ($49/month, need 200 customers for $10k MRR)
- Founder-Market Fit: 8 (you're the user, passionate about helping freelancers)

**SFRI = (0.5 × 9.25) + (0.3 × 8.75) + (0.2 × 8.0) = 4.625 + 2.625 + 1.6 = 8.85**

**Assessment**: Highly viable. Ship this.

### Example 2: Low SFRI (4.3) - AI-Powered Tweet Scheduler for Indie Hackers

**VMR: 3.5**
- Problem Specificity: 4 (tweeting consistently is annoying, but not critical pain)
- Willingness to Pay: 3 (Hypefury/Typefully exist, but market saturation high)
- Customer Proximity: 6 (active on Twitter, can reach indie hackers)
- Market Bubble: 1 (squarely in indie hacker bubble)

**PTR: 6.0**
- Stack Simplicity: 8 (Next.js, familiar stack)
- Infrastructure: 7 (Vercel + Supabase)
- Feature Creep: 5 (MVP growing: scheduling, AI writing, analytics, thread composer)
- Maintenance Tax: 4 (Twitter API rate limits require manual monitoring)

**GLR: 4.25**
- Acquisition: 3 (paid Twitter ads or Product Hunt, saturated market)
- Automation: 8 (mostly automated)
- Unit Economics: 2 ($15/month, need 700 customers for $10k MRR)
- Founder-Market Fit: 4 (interested in AI, but not passionate about Twitter tools)

**SFRI = (0.5 × 3.5) + (0.3 × 6.0) + (0.2 × 4.25) = 1.75 + 1.8 + 0.85 = 4.4**

**Assessment**: Critical anti-patterns. High failure risk. In the indie hacker bubble, saturated market, low pricing requires massive scale. Abandon or pivot to broader market outside maker space.

### Example 3: Moderate SFRI (7.2) - Kubernetes Deployment Tool

**VMR: 7.0**
- Problem Specificity: 8 (DevOps engineers struggle with K8s complexity)
- Willingness to Pay: 9 (companies pay for DevOps tools)
- Customer Proximity: 5 (can reach via cold outreach, some network)
- Market Bubble: 6 (adjacent to maker space, broader DevOps market)

**PTR: 5.5**
- Stack Simplicity: 4 (need to learn Go ecosystem deeply)
- Infrastructure: 3 (inherently complex: need K8s cluster to test)
- Feature Creep: 7 (clear MVP: deploy apps to K8s easily)
- Maintenance Tax: 8 (mostly automated once working)

**GLR: 9.0**
- Acquisition: 9 (excellent SEO opportunity, content marketing to DevOps audience)
- Automation: 10 (pure software automation)
- Unit Economics: 9 ($299/month, need 35 customers for $10k MRR)
- Founder-Market Fit: 8 (DevOps background, love infrastructure)

**SFRI = (0.5 × 7.0) + (0.3 × 5.5) + (0.2 × 9.0) = 3.5 + 1.65 + 1.8 = 6.95**

**Assessment**: Moderate risk. Strong market and growth potential, but technical complexity is concerning. Before building:
1. Simplify tech stack if possible (use existing K8s libraries, don't reinvent)
2. Validate willingness to pay with landing page + pre-sales
3. Consider if you can build MVP without deep K8s expertise
4. If you can address PTR concerns (especially stack/infrastructure), this could hit 8.0+

## Usage Guidelines

### When to Calculate SFRI

**Required scenarios**:
- Evaluating a new product idea before writing code
- Deciding whether to pivot or persist on existing project
- Choosing between multiple product opportunities
- Explaining to co-founder/advisor why an idea is risky

**Optional but helpful**:
- Quarterly review of existing product health
- Post-mortem analysis of failed projects
- Validating feature additions (calculate impact on each dimension)

### How to Use Scores

**Don't be dogmatic**: SFRI is a tool, not a rule. A 6.4 vs 6.6 isn't meaningfully different. Use it to identify weak dimensions and make improvements, not to make binary go/no-go decisions on borderline scores.

**Focus on weak dimensions**: If overall score is moderate but one dimension is extremely low, that's the critical risk. Address the weakest link first.

**Track over time**: Calculate SFRI at idea stage, MVP launch, and quarterly after launch. Dimension scores should generally improve as you validate and optimize. If scores decline, investigate why.

**Use for prioritization**: When choosing between multiple ideas, SFRI provides a quantitative framework to compare opportunities.

### Common Scoring Mistakes

**Mistake 1: Optimism Bias**
Founders tend to score their own ideas 1-2 points higher than reality on each dimension.

**Mitigation**: Have someone else score it blindly, or force yourself to justify each score with specific evidence.

**Mistake 2: Weighing All Dimensions Equally**
The formula intentionally weighs VMR at 50% because building the wrong thing is worse than building the right thing poorly.

**Mitigation**: Don't override the weights. If VMR is low, the project is risky regardless of other scores.

**Mistake 3: Scoring Aspirationally**
Scoring based on "we could eventually..." rather than current reality.

**Mitigation**: Score based on day-0 state, not 12-month roadmap. You can calculate separate scores for "now" vs "in 12 months" to track planned improvements.

**Mistake 4: Ignoring Red Flags**
If any sub-dimension triggers a "red flag," it should auto-score at the low end (1-3) regardless of other considerations.

**Mitigation**: Red flags exist for a reason. Don't rationalize your way out of them.

## Integration with Other Frameworks

### SFRI + Lean Canvas

Use SFRI to validate your Lean Canvas before building:
- **Problem**: Feeds into VMR (Problem Specificity, Customer Proximity)
- **Solution**: Feeds into PTR (Stack Simplicity, Feature Creep)
- **Channels**: Feeds into GLR (Acquisition Strategy)
- **Revenue Streams**: Feeds into GLR (Unit Economics)

### SFRI + Mom Test

Use Mom Test conversations to gather evidence for SFRI scoring:
- Ask about current solutions and payment (Willingness to Pay)
- Ask about frequency and impact (Problem Specificity)
- Ask about budget and decision-making (Unit Economics)

### SFRI + Value Proposition Canvas

Map value proposition elements to SFRI dimensions:
- **Jobs to be Done**: Problem Specificity
- **Pains**: Willingness to Pay validation
- **Gains**: Founder-Market Fit alignment

## Conclusion

The SFRI provides a quantitative, systematic framework for identifying anti-patterns before they become fatal. Use it early and often, be honest about scores, and focus on improving weak dimensions before writing code.

Remember: A low SFRI doesn't mean "never build this." It means "fix these specific problems first, then re-evaluate."
