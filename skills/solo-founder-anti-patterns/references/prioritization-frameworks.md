# Prioritization Frameworks for Solo Founders

Detailed analysis of feature and task prioritization frameworks adapted for the unique constraints of solo founders and indie hackers.

## Overview

Solo founders face different prioritization challenges than product teams:
- **Limited time**: Every hour matters; no slack for low-impact work
- **No delegation**: Can't hand off tasks to specialists
- **Revenue pressure**: Every decision must consider immediate vs. long-term revenue impact
- **Burnout risk**: Over-committing leads to personal and organizational burnout

Standard product prioritization frameworks (designed for teams with specialized roles) must be adapted for the solo founder reality.

## Framework Comparison Matrix

| Framework | Best For | Time to Apply | Strengths | Weaknesses for Solo Founders |
|-----------|----------|---------------|-----------|------------------------------|
| **Value vs. Effort** | Daily task prioritization | 2-5 min | Fast, intuitive, actionable | Oversimplifies complex tradeoffs |
| **MoSCoW** | MVP scope definition | 15-30 min | Forces hard choices on scope | Prone to "everything is Must-Have" bias |
| **RICE** | Established product roadmap | 20-45 min | Quantitative, reduces bias | Requires data solo founders rarely have |
| **Kano Model** | Competitive differentiation | 30-60 min | Separates basics from delighters | Complex, requires user research |
| **ICE** | Quick scoring without data | 5-10 min | Simpler than RICE, no "Reach" needed | Still requires confidence estimates |
| **Buy a Feature** | User-driven prioritization | 30-45 min | Direct customer input | Requires engaged user base |

## Framework 1: Value vs. Effort Matrix (Recommended for Daily Use)

### Overview

The simplest and most actionable framework for solo founders. Plot each task on two axes:
- **X-axis: Effort** (time and complexity to implement)
- **Y-axis: Value** (impact on revenue, retention, or acquisition)

### The Four Quadrants

```
High Value
    │
    │  Big Bets        Quick Wins
    │  (High Value,    (High Value,
    │   High Effort)    Low Effort)
    │
────┼──────────────────────────
    │
    │  Time Sinks      Fill-Ins
    │  (Low Value,     (Low Value,
    │   High Effort)    Low Effort)
    │
Low Value            High Effort
                     →
```

### Quadrant Actions

#### 1. Quick Wins (High Value, Low Effort)
**Action**: Do these immediately, today if possible.

**Examples**:
- Fix critical bug affecting 50% of users (30 min fix)
- Add "Share on Twitter" button that drives referrals (15 min)
- Send email to churned users asking why they left (1 hour)
- Update pricing page with clearer value prop based on user feedback (2 hours)

**Why these matter for solo founders**:
- Maximum ROI on time
- Build momentum (ship wins fast)
- Often unblock growth immediately

**How to identify**:
- User requests that are trivial to implement
- Low-hanging fruit from analytics (e.g., "50% of users drop off at this step")
- One-line code changes with outsized impact

#### 2. Big Bets (High Value, High Effort)
**Action**: Schedule deliberately. Do one at a time. Only after Quick Wins are exhausted.

**Examples**:
- Build new core feature users are requesting (40 hours)
- Migrate to new payment processor to reduce fees by 50% (60 hours)
- Complete SEO overhaul to target new keyword cluster (80 hours)
- Build integration with major platform (100 hours)

**Why these matter for solo founders**:
- Can't be avoided if truly high value
- Require dedicated focus (not interruption-driven work)
- Risk burnout if you do too many simultaneously

**How to approach**:
1. **Validate first**: Is this truly high value, or is it just high effort? Talk to users.
2. **Timebox**: Set hard deadline. If it takes 3x longer than expected, reassess.
3. **Ship iteratively**: Can you ship 20% of this for 5% of the effort? (MVP within MVP)
4. **No context switching**: Block off days/weeks to focus solely on this. Don't interrupt for Quick Wins.

**Red flags**:
- You have 5 "Big Bets" in progress simultaneously (pick one, finish it)
- Big Bet has been "in progress" for 3+ months (reassess value or break down further)
- You're doing Big Bets while Quick Wins pile up (wrong order)

#### 3. Fill-Ins (Low Value, Low Effort)
**Action**: Do these when blocked on other work or for mental breaks. Never prioritize over Quick Wins or Big Bets.

**Examples**:
- Update README with new screenshots (15 min)
- Refactor variable names for clarity (30 min)
- Add Easter egg to 404 page (10 min)
- Respond to non-urgent support emails (20 min)

**Why these matter for solo founders**:
- Good for "low energy" time (end of day, post-lunch slump)
- Provide small wins when stuck on Big Bets
- Keep things tidy without significant time sink

**How to use**:
- Keep a "Fill-Ins" list for when you're waiting on API calls, deployments, or just mentally fried
- Don't let these crowd out real work
- Batch them (e.g., "Fill-In Friday" for 2 hours)

**Red flags**:
- Spending more than 10% of your time here (procrastination disguised as productivity)
- Doing Fill-Ins to avoid hard conversations or marketing work
- Fill-Ins list is longer than Quick Wins list (wrong focus)

#### 4. Time Sinks (Low Value, High Effort)
**Action**: **DELETE IMMEDIATELY. Do not postpone, do not put on backlog. Delete.**

**Examples**:
- Perfect code coverage (95% → 100%) when you have no team (40 hours)
- Support for IE11 when 0.1% of traffic uses it (20 hours)
- Feature requested by one user who pays $5/month (30 hours)
- Rewrite working code in "cleaner" architecture (60 hours)
- Build admin dashboard when you're the only admin (50 hours)

**Why these are fatal for solo founders**:
- Burn weeks with no revenue/growth impact
- Often driven by perfectionism or procrastination, not user value
- Opportunity cost is massive (could have done 10 Quick Wins instead)

**How to ruthlessly cut**:
1. **Ask**: "If I spend 40 hours on this, will it directly result in $X more revenue or Y% more users?" If no, delete.
2. **Ask**: "Would a user pay me $1,000 to do this?" If no, delete.
3. **Ask**: "Is this avoiding a harder problem (marketing, sales, hard feature)?" If yes, delete.

**Common Time Sink disguises**:
- "This will make the codebase cleaner" (users don't care)
- "This is a best practice" (best practices are for teams, not solo founders)
- "This will make future development faster" (you don't have a future if you don't ship now)
- "Competitors have this" (your users aren't asking for it)

### How to Apply Value vs. Effort

#### Step 1: Dump all tasks
Write down everything you think you should do. User requests, bugs, features, refactors, marketing ideas, everything.

#### Step 2: Score Effort (1-10)
- 1-2: Less than 1 hour
- 3-4: 1-4 hours
- 5-6: 4-8 hours (half day to full day)
- 7-8: 2-5 days
- 9-10: 1+ weeks

**Be honest**: Solo founders consistently underestimate effort. Multiply your initial estimate by 1.5x.

#### Step 3: Score Value (1-10)
- 1-2: Nice to have, no measurable impact
- 3-4: Slight improvement to experience, minor impact
- 5-6: Moderate improvement, measurable but not game-changing
- 7-8: Significant impact on key metric (revenue, retention, acquisition)
- 9-10: Existential. If we don't do this, business is at risk.

**Key question**: "If I do this, which number goes up, and by how much?"
- Revenue: How much more MRR?
- Retention: How much does churn decrease?
- Acquisition: How many more sign-ups?

If you can't answer with a number, it's probably 1-4 value.

#### Step 4: Plot on matrix
Draw a 2x2 grid. Plot each task based on Effort and Value scores.

**Simplified quadrant boundaries**:
- **Quick Wins**: Value ≥ 6, Effort ≤ 5
- **Big Bets**: Value ≥ 6, Effort ≥ 6
- **Fill-Ins**: Value ≤ 5, Effort ≤ 5
- **Time Sinks**: Value ≤ 5, Effort ≥ 6

#### Step 5: Execute in order
1. All Quick Wins (sorted by Value descending)
2. One Big Bet at a time (highest Value first)
3. Fill-Ins when blocked or low energy
4. **Delete all Time Sinks** (don't even put them on a backlog)

### Value vs. Effort Example

**Scenario**: SaaS product with 500 users, $5k MRR, $50/year ARPU. High churn (15%/month).

**Task list**:
1. Add dark mode
2. Fix bug causing payment failures (affecting 10% of renewals)
3. Build integration with popular tool (users requesting)
4. Rewrite frontend in React (currently jQuery)
5. Add export to CSV feature
6. Send win-back email to churned users
7. Optimize database queries (site is slow)
8. Support for Safari (10% of traffic, currently broken)
9. Build GraphQL API (currently REST)
10. Add social login (Google/GitHub)

**Scoring**:

| Task | Effort | Value | Reasoning | Quadrant |
|------|--------|-------|-----------|----------|
| Dark mode | 6 | 3 | 20% of users request it, but doesn't affect revenue/retention | Time Sink |
| Fix payment bug | 2 | 10 | Directly losing 10% of renewals = $500/month revenue loss | Quick Win |
| Popular integration | 8 | 8 | 30% of users request it, could reduce churn 5% | Big Bet |
| Rewrite to React | 10 | 2 | Users don't care about tech stack, no revenue impact | Time Sink |
| CSV export | 3 | 5 | 10% of users request, nice-to-have | Fill-In |
| Win-back email | 1 | 7 | Could recover 10% of churned users = +$250 MRR | Quick Win |
| Optimize DB | 4 | 7 | Site slowness causing 5% drop-off in sign-ups | Quick Win |
| Safari support | 5 | 6 | 10% of traffic broken, losing sign-ups | Quick Win |
| GraphQL API | 9 | 1 | No user request, no clear value | Time Sink |
| Social login | 4 | 4 | Mild improvement to sign-up flow | Fill-In |

**Execution order**:
1. **Quick Wins first** (Week 1):
   - Fix payment bug (2 hours) → +$500/month immediately
   - Send win-back email (1 hour) → +$250 MRR potential
   - Optimize DB (4 hours) → +5% sign-ups
   - Fix Safari (5 hours) → +10% sign-ups
   - **Total: 12 hours, +$750 MRR + 15% more sign-ups**

2. **Big Bet** (Week 2-3):
   - Build popular integration (40 hours) → Reduce churn 5% = +$250/month retained
   - **Total: 40 hours, +$250/month retention**

3. **Fill-Ins** (when blocked):
   - CSV export (3 hours)
   - Social login (4 hours)

4. **Time Sinks** (DELETE):
   - ~~Dark mode~~ (deleted)
   - ~~React rewrite~~ (deleted)
   - ~~GraphQL API~~ (deleted)

**Result**: In 2-3 weeks, shipped 4 Quick Wins + 1 Big Bet, added ~$1,000/month to bottom line. Avoided wasting 25+ hours on Time Sinks.

---

## Framework 2: MoSCoW (MVP Scope Definition)

### Overview

MoSCoW forces hard decisions about what's in vs. out of scope for an MVP or release. Designed for scope management, not daily prioritization.

**Acronym**:
- **M**ust Have
- **S**hould Have
- **C**ould Have
- **W**on't Have (this time)

### How to Use MoSCoW

#### 1. Must Have
Features **without which the product cannot launch**. If it's not there, the core value proposition is broken.

**Solo founder litmus test**:
- "If I remove this, can I still charge money?" If yes, it's not a Must Have.
- "Does this directly enable the one core job-to-be-done?" If no, it's not a Must Have.

**Example (Invoice Tool)**:
- Must Have: Create invoice, send invoice, track payment status
- Not Must Have: Recurring invoices, multi-currency, team collaboration

**Common mistake**: Calling everything "Must Have" because users might want it. Must Haves are **necessary for viability**, not **nice to have**.

**Target**: 1-3 features maximum for MVP. If you have 10 Must Haves, you're lying to yourself.

#### 2. Should Have
Important features that improve the product but aren't launch-blockers. Can be added in v1.1 or v1.2.

**Solo founder litmus test**:
- "Would users pay without this?" If yes, it's a Should Have, not Must Have.
- "Does this make the product 2x better?" If no, it's Could Have.

**Example (Invoice Tool)**:
- Should Have: Invoice templates, automatic payment reminders, late fee calculations

**Target**: 3-7 features. These get built in the first 3-6 months post-launch.

#### 3. Could Have
Nice-to-haves that differentiate or delight but aren't critical. Build only if you have excess capacity (rare for solo founders).

**Solo founder litmus test**:
- "Would any user choose a competitor over us solely because we lack this?" If no, Could Have.

**Example (Invoice Tool)**:
- Could Have: Custom branding, PDF customization, client portal

**Target**: These often never get built. That's okay.

#### 4. Won't Have (This Time)
Explicitly out of scope for this release. Documenting these prevents scope creep.

**Solo founder litmus test**:
- "Is this a distraction from the core value prop?" If yes, Won't Have.
- "Are we building this because competitors have it, not because users are asking?" If yes, Won't Have.

**Example (Invoice Tool)**:
- Won't Have: Expense tracking, time tracking, project management, team collaboration

**Target**: This list should be longer than Must Have + Should Have combined. Saying "no" is the most important skill.

### Applying MoSCoW: Worked Example

**Scenario**: Building a landing page builder for indie hackers.

**Initial brainstorm** (everything you could build):
1. Drag-and-drop page builder
2. Pre-built templates
3. Custom domain support
4. Email integration
5. A/B testing
6. Analytics dashboard
7. SEO optimization
8. Mobile responsive
9. Custom code injection
10. Form builder
11. Payment integration
12. Multi-language support
13. Team collaboration
14. Version history
15. SSL certificates

**MoSCoW classification**:

**Must Have** (without these, it's not a landing page builder):
1. Drag-and-drop page builder
2. Mobile responsive (default expectation)
3. Publish to custom domain

**Should Have** (important, but can launch without):
4. Pre-built templates (can launch with 1 template, add more later)
5. Form builder (core use case for lead capture)
6. SEO optimization (meta tags, etc.)

**Could Have** (nice differentiation):
7. A/B testing (advanced feature, not needed for MVP)
8. Analytics dashboard (users can use Google Analytics)
9. Email integration (users can copy/paste form submissions)

**Won't Have** (explicit scope cuts):
10. Custom code injection (power feature, niche use case)
11. Payment integration (out of scope, landing pages don't need payments)
12. Multi-language (unnecessary complexity for MVP)
13. Team collaboration (solo users first, teams later)
14. Version history (nice-to-have, not essential)
15. SSL certificates (use Netlify/Vercel, they handle it)

**Outcome**: Launch with 3 Must Haves. Add 3 Should Haves in first 6 months. Ignore the rest unless users scream for them.

### MoSCoW Anti-Patterns for Solo Founders

**Anti-Pattern 1: "Must Have" Bloat**
- Symptom: 10+ features in Must Have category
- Fix: Apply litmus test ruthlessly. Most are Should/Could Haves in disguise.

**Anti-Pattern 2: Ignoring "Won't Have"**
- Symptom: No explicit Won't Have list, scope keeps growing
- Fix: Document what you're NOT building. Review weekly to prevent creep.

**Anti-Pattern 3: Building Should Haves Before Launching**
- Symptom: MVP has been "95% ready" for months because you're adding Should Haves
- Fix: Launch with Must Haves only. Add Should Haves after getting user feedback.

---

## Framework 3: RICE (Quantitative Roadmap Scoring)

### Overview

RICE is a quantitative framework designed to reduce bias in feature prioritization. Most useful for established products with data.

**Formula**:
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

### Components

#### Reach
**Question**: How many users will this affect in a given time period (usually per month or quarter)?

**Measurement**:
- Number of users who will interact with this feature per month
- For new features: Estimate based on similar features or % of user base

**Example**:
- Fix critical bug: 500 users affected per month (100% of user base)
- Niche feature: 50 users per month (10% of user base)

**Solo founder challenge**: You often don't have enough data for accurate Reach estimates.

#### Impact
**Question**: How much will this move the key metric (revenue, retention, engagement)?

**Scoring** (use standardized scale):
- **3**: Massive impact (3x improvement in metric)
- **2**: High impact (2x improvement)
- **1**: Medium impact (50% improvement)
- **0.5**: Low impact (25% improvement)
- **0.25**: Minimal impact (barely measurable)

**Example**:
- Feature that reduces churn from 15% to 7.5% (50% improvement): Impact = 1
- Feature that increases conversion from 2% to 6% (3x improvement): Impact = 3

**Solo founder challenge**: Hard to estimate impact without A/B testing infrastructure.

#### Confidence
**Question**: How confident are you in your Reach and Impact estimates?

**Scoring**:
- **100%**: High confidence (based on data, user research, or proven similar features)
- **80%**: Medium confidence (based on anecdotal feedback or similar product data)
- **50%**: Low confidence (gut feeling, no data)

**Example**:
- Confidence = 100%: "50 users explicitly requested this, and we have data showing similar features get 80% adoption"
- Confidence = 50%: "I think users might like this, but no one has asked for it"

**Solo founder challenge**: Confidence is often inflated by founder bias.

#### Effort
**Question**: How much time will this take (in person-weeks or person-months)?

**Measurement**:
- Estimate in "person-weeks" (40 hours of work)
- Include design, development, testing, deployment, documentation

**Example**:
- Small bug fix: 0.1 person-weeks (4 hours)
- New feature: 2 person-weeks (80 hours)
- Major integration: 8 person-weeks (320 hours)

**Solo founder adjustment**: You're the only person, so person-weeks = calendar weeks (no parallel work).

### RICE Calculation Example

**Feature**: Add Stripe integration for payments

**Estimates**:
- Reach: 400 users per month (80% of user base will use payments)
- Impact: 2 (high impact - enables monetization, doubles revenue potential)
- Confidence: 80% (based on user requests and competitor data)
- Effort: 3 person-weeks (120 hours to integrate, test, handle edge cases)

**RICE Score**:
```
RICE = (400 × 2 × 0.8) / 3 = 640 / 3 = 213
```

**Feature**: Add dark mode

**Estimates**:
- Reach: 100 users per month (20% of users might use it)
- Impact: 0.25 (minimal impact on retention/revenue)
- Confidence: 50% (no one has requested it, just a hunch)
- Effort: 1.5 person-weeks (60 hours to implement across all pages)

**RICE Score**:
```
RICE = (100 × 0.25 × 0.5) / 1.5 = 12.5 / 1.5 = 8.3
```

**Decision**: Stripe integration (213) >> dark mode (8.3). Build Stripe first.

### When RICE Works for Solo Founders

**Good scenarios**:
- You have 500+ users and actual usage data
- You're choosing between 5+ features and want to reduce bias
- You have clear metrics (MRR, churn, sign-ups) to measure Impact
- Features have measurable Reach (you can count affected users)

**Bad scenarios**:
- Pre-launch (no users = no Reach data)
- Fewer than 100 users (not enough data for confident estimates)
- Qualitative decisions (brand positioning, messaging, etc.)
- You're already confident about priority (RICE takes 20-45 min per feature)

### RICE Anti-Patterns for Solo Founders

**Anti-Pattern 1: Fake Precision**
- Symptom: Spending 30 minutes debating if Impact is 1.0 or 1.2
- Fix: Use rough estimates. RICE is for comparing orders of magnitude (10 vs 100), not fine-tuning (98 vs 102).

**Anti-Pattern 2: Optimism Bias in Confidence**
- Symptom: Everything is 80-100% Confidence because "I feel good about it"
- Fix: Default to 50% Confidence unless you have hard data or user requests.

**Anti-Pattern 3: Ignoring Effort Uncertainty**
- Symptom: Estimating 1 week for features that take 4 weeks
- Fix: Multiply effort estimates by 1.5x-2x for solo work (no pair programming, more interruptions).

---

## Framework 4: Kano Model (Feature Differentiation)

### Overview

The Kano Model categorizes features based on their relationship to customer satisfaction. Helps differentiate "table stakes" from "delighters."

**Three categories**:
1. **Basic Expectations** (Threshold Attributes): Must-haves that don't increase satisfaction, but their absence causes dissatisfaction
2. **Performance Attributes** (Satisfiers): More is better; directly correlate to satisfaction
3. **Delighters** (Excitement Attributes): Unexpected features that create delight but aren't missed if absent

### Feature Categories Explained

#### 1. Basic Expectations
**Definition**: Features users expect by default. Presence doesn't increase satisfaction, absence causes frustration.

**Examples**:
- Landing page builder: Mobile responsive, SSL, page load speed
- SaaS product: Reliable uptime, data security, password reset
- E-commerce: Shopping cart, checkout, order confirmation

**Solo founder implication**: Build these first, but don't expect them to differentiate you. Users won't praise you for having them, but will churn if you don't.

**How to identify**:
- Look at competitors: What do 100% of them have?
- Ask users: "What would make you immediately reject a product?"
- Check reviews: What do users complain about when it's missing?

#### 2. Performance Attributes
**Definition**: Features where more/better = more satisfaction. Linear relationship.

**Examples**:
- Landing page builder: Number of templates, page load speed, ease of use
- SaaS product: Feature completeness, integration count, customer support quality
- E-commerce: Product selection, price, shipping speed

**Solo founder implication**: Compete here selectively. Pick 1-2 Performance Attributes to excel at; be "good enough" on others.

**How to identify**:
- User surveys: "What would make you upgrade to a paid plan?"
- Feature requests: These are usually Performance Attributes
- Competitor comparison: Where do users compare products head-to-head?

#### 3. Delighters
**Definition**: Unexpected features that create wow moments. Users don't ask for them because they don't know to ask.

**Examples**:
- Landing page builder: AI-generated copy, automatic performance optimization, built-in A/B testing insights
- SaaS product: Surprise free upgrade, proactive support, delightful Easter eggs
- E-commerce: Handwritten thank-you note, free upgrade to faster shipping

**Solo founder implication**: Use sparingly. Delighters are high-risk (users might not care) but high-reward (can drive word-of-mouth).

**How to identify**:
- What do users rave about in reviews? (Not just "like" but "love")
- What features get shared on social media?
- What makes your product memorable vs. competitors?

### Applying Kano Model

#### Step 1: Categorize Your Features

List all planned/existing features and categorize:

**Example (Project Management Tool)**:

| Feature | Kano Category | Reasoning |
|---------|---------------|-----------|
| Create tasks | Basic | Every PM tool has this; users expect it |
| Assign tasks | Basic | Core functionality, not differentiating |
| Due dates | Basic | Expected feature, won't impress anyone |
| Gantt charts | Performance | More/better charts = more satisfaction for some users |
| Integrations (Slack, etc.) | Performance | More integrations = better product |
| AI task estimation | Delighter | Unexpected, could create wow moment |
| Dark mode | Performance | Some users care a lot, most don't care |
| Custom automations | Delighter | Power feature, unexpected by most |

#### Step 2: Prioritize by Category

**For MVP**:
1. Build all Basic Expectations (table stakes)
2. Excel at 1-2 Performance Attributes (your differentiation)
3. Skip Delighters (too risky for MVP)

**For established product**:
1. Maintain all Basic Expectations (non-negotiable)
2. Improve your chosen Performance Attributes (competitive advantage)
3. Add 1 Delighter per quarter (drive word-of-mouth)

#### Step 3: Allocate Time

**Solo founder time allocation**:
- 30% on Basic Expectations (maintaining reliability, security, core features)
- 50% on Performance Attributes (your competitive edge)
- 20% on Delighters (experimentation, innovation)

**Anti-pattern**: Spending 80% on Delighters while Basic Expectations are broken (users churn despite cool features).

### Kano Model Example: Email Marketing Tool

**Scenario**: Building email marketing tool for solo founders.

**Feature list categorization**:

**Basic Expectations** (must-have, no differentiation):
- Send email campaigns
- Email list management
- Unsubscribe handling
- Spam compliance (CAN-SPAM, GDPR)
- Basic analytics (open rate, click rate)
- Email templates

**Performance Attributes** (competitive differentiation):
- Deliverability rate (the better, the more satisfaction)
- Number of templates (more = better)
- Ease of use (faster/simpler = better)
- Automation workflows (more complex = better for power users)
- Segmentation options (more precise = better)

**Delighters** (unexpected wow moments):
- AI-generated subject lines that increase open rates
- Automatic send-time optimization per subscriber
- Predictive churn detection ("This subscriber will likely unsubscribe soon")
- Built-in affiliate program for users to earn referrals

**Solo founder strategy**:
1. **Build all Basic Expectations** (Week 1-4): Email sending, list management, compliance, basic analytics
2. **Excel at 2 Performance Attributes** (Week 5-12):
   - **Deliverability**: Partner with SendGrid/Postmark, obsess over inbox placement
   - **Ease of use**: Simplest UI in the market, fewer clicks than competitors
3. **Add 1 Delighter** (Week 13-16):
   - **AI subject line optimizer**: Unexpected, high perceived value, defensible

**Time allocation**:
- 30% maintaining Basic Expectations (uptime, compliance, bug fixes)
- 50% improving Deliverability and Ease of Use (core differentiation)
- 20% iterating on AI features (future delighters)

### Kano Model Anti-Patterns

**Anti-Pattern 1: Delighter Obsession**
- Symptom: Building cool features while core functionality is broken
- Fix: Basic Expectations first, always. Delighters only after basics are solid.

**Anti-Pattern 2: Competing on All Performance Attributes**
- Symptom: Trying to have the most templates AND the best deliverability AND the most integrations AND the best automation
- Fix: Pick 1-2 Performance Attributes to win at. Be "good enough" on the rest.

**Anti-Pattern 3: Ignoring Category Shifts**
- Symptom: A feature that was a Delighter 2 years ago is now a Basic Expectation (e.g., mobile responsive design)
- Fix: Reassess categories annually. What was differentiating becomes expected over time.

---

## Choosing the Right Framework

### Decision Tree

**For daily task prioritization**:
→ Use **Value vs. Effort Matrix** (fast, actionable, intuitive)

**For defining MVP scope**:
→ Use **MoSCoW** (forces hard cuts, prevents scope creep)

**For established product with data**:
→ Use **RICE** (quantitative, reduces bias, requires user data)

**For competitive positioning**:
→ Use **Kano Model** (differentiate basics from delighters)

**For quick prioritization without data**:
→ Use **ICE** (simpler than RICE, no Reach estimates needed)

### Combining Frameworks

**Best practice**: Use multiple frameworks for different purposes.

**Example workflow**:
1. **MoSCoW** to define MVP scope (one-time, during product planning)
2. **Value vs. Effort** for weekly task prioritization (ongoing)
3. **Kano Model** for quarterly feature categorization (check if you're balancing basics, performance, delighters)
4. **RICE** when choosing between 5+ features and you have data (ad-hoc, when needed)

### Framework Overhead Warning

**Don't over-process**:
- Frameworks are tools, not religion
- If you spend more time prioritizing than building, you're doing it wrong
- Default to Value vs. Effort for 80% of decisions (fast, good enough)
- Use heavy frameworks (RICE, Kano) only when decision is truly unclear

---

## Prioritization for Solo Founders: Core Principles

Regardless of framework chosen, apply these solo founder-specific principles:

### Principle 1: Bias Toward Shipping
When in doubt between "build more" and "ship now," ship now. Shipped products generate feedback and revenue. Perfect products in development generate neither.

### Principle 2: Delete Aggressively
The most important prioritization decision is what NOT to build. Your backlog should shrink over time, not grow.

### Principle 3: Revenue-First Lens
If a task doesn't plausibly lead to more revenue (new customers, retained customers, higher ARPU), question whether it's worth doing.

### Principle 4: Avoid Context Switching
Doing 10 things 10% of the way is worse than doing 1 thing 100% of the way. Finish what you start.

### Principle 5: User Requests > Competitor Features
Build what your users ask for, not what your competitors have. Your users chose you for a reason; don't become a worse version of the competition.

### Principle 6: Quick Wins Create Momentum
Shipping small wins frequently beats shipping big features slowly. Momentum matters for morale and user perception.

### Principle 7: Automate Before Hiring
Before adding a person to do repetitive work, explore automation. Robots are cheaper and easier than people.

### Principle 8: Time Is the Only Resource
You have 40-60 productive hours per week. Every hour spent on low-value work is an hour not spent on high-value work. Prioritization is existential.

---

## Conclusion

Prioritization frameworks don't make decisions for you—they clarify tradeoffs and reduce bias. For solo founders:

- **Default to Value vs. Effort** for daily decisions (fast, actionable)
- **Use MoSCoW** to fight scope creep on new projects (forces hard cuts)
- **Apply RICE** when you have data and need to reduce bias (quantitative)
- **Reference Kano Model** to balance basics, performance, and delighters (competitive positioning)

Most importantly: **Ruthlessly delete Time Sinks**. The difference between successful and failed solo founders is often what they chose NOT to build.
