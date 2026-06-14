# Story Splitting Patterns Reference Guide

Deep-dive reference for the 9 canonical Richard Lawrence story-splitting patterns plus optional "Major Effort First." Companion to `SKILL.md`.

---

## 0. Why Vertical Slicing

A story is vertically sliced when it includes everything needed to deliver user value end-to-end: UI, API, database, deployment, monitoring -- whatever it takes to demo. Horizontal slicing produces "build the back-end this sprint, the front-end next sprint" -- shippable code, no shippable value.

The benefits of vertical slicing are mechanical:

- **Faster feedback.** Users see the slice in the next release, not three releases later.
- **Lower risk.** Each slice tests assumptions in production conditions, not at integration.
- **Easier to deprioritize.** A vertical slice can be cut without leaving behind half-built layers.
- **Predictable estimation.** Vertical slices converge on similar size and cycle time, enabling throughput-based forecasting (see `cycle-time-analyzer/`).

---

## 1. Pattern 1: Workflow Steps

**Cue:** The story description includes "user goes through X, then Y, then Z" or maps to a multi-step flow.

**Recipe:** Each step becomes a story. Ship in order or in parallel if independent.

### Worked Examples

#### Example 1a: User Onboarding

**Before:** *"As a new user, I want to complete onboarding so I can start using the product."*

**After:**
1. Verify email and create password
2. Connect first data source
3. Invite first teammate
4. Build first dashboard

Each slice is releasable behind a progressive-disclosure UI. Skip-and-resume support can be its own later story.

#### Example 1b: Checkout Flow

**Before:** *"As a shopper, I want to check out so I can complete my purchase."*

**After:**
1. Review cart and shipping address
2. Enter or select payment method
3. Confirm and place order
4. Receive order confirmation

---

## 2. Pattern 2: Business Rule Variations

**Cue:** The story embeds "the system should apply discount X for case A, discount Y for case B..." or multiple eligibility rules.

**Recipe:** Each business rule becomes a slice. Ship the most-common case first.

### Worked Examples

#### Example 2a: Pricing Discounts

**Before:** *"As an admin, I want to apply promotional discounts."*

**After:**
1. Flat percentage-off discount (covers 70% of promotions)
2. Buy-one-get-one promotion
3. Tiered volume discount (10% off 50+ units, 20% off 100+)
4. Coupon code with expiration date and usage limit

#### Example 2b: Eligibility Rules for Features

**Before:** *"As a customer, I want enterprise features when my plan qualifies."*

**After:**
1. Enable enterprise features for any team on the enterprise plan
2. Enable enterprise features for teams with 50+ seats, regardless of plan name
3. Enable enterprise features during the 14-day trial extension period

---

## 3. Pattern 3: Happy / Unhappy Path

**Cue:** The story includes "with error handling" or "validates input and rejects when..."

**Recipe:** Ship the happy path first. Each unhappy path becomes its own slice.

### Worked Examples

#### Example 3a: CSV Upload

**Before:** *"As a user, I want to upload a CSV with full validation."*

**After:**
1. Upload a valid CSV up to 10 MB and see the records imported (happy path)
2. Reject non-CSV files and show file-type error
3. Reject CSVs over 10 MB with size-limit message
4. Show line-numbered errors for malformed rows
5. Provide a downloadable error report for partial imports

#### Example 3b: Payment Processing

**Before:** *"As a customer, I want to pay for my order with payment failure handling."*

**After:**
1. Successful credit-card charge (happy path)
2. Show clear error when card is declined
3. Allow retry with a different card
4. Handle network timeout with retry-after delay
5. Notify admin when payment is repeatedly failing across customers

---

## 4. Pattern 4: Input/Output Variations (Interface Options)

**Cue:** The story supports multiple input methods or output formats simultaneously.

**Recipe:** Each input or output variation becomes a slice. Ship the most-used variation first.

### Worked Examples

#### Example 4a: Report Export

**Before:** *"As a user, I want to export reports."*

**After:**
1. Export to CSV (most-requested format)
2. Export to PDF
3. Export to Excel with formatting
4. Schedule recurring CSV export by email
5. Expose report data via JSON API

#### Example 4b: Multi-Channel Notifications

**Before:** *"As a user, I want to be notified of important events."*

**After:**
1. In-app notification banner
2. Email notification
3. SMS notification
4. Slack / Teams integration notification
5. Mobile push notification

---

## 5. Pattern 5: Data Variations

**Cue:** The story handles "any" type of input, source, or entity that varies by category.

**Recipe:** Each data type or source becomes a slice.

### Worked Examples

#### Example 5a: Data Source Connectors

**Before:** *"As a user, I want to connect a database."*

**After:**
1. Connect Postgres (most common in our user base)
2. Connect MySQL
3. Connect Snowflake
4. Connect BigQuery
5. Upload static CSV (no live connection)

#### Example 5b: Identity Provider Integration

**Before:** *"As an admin, I want SSO with any identity provider."*

**After:**
1. SAML 2.0 with Okta
2. SAML 2.0 with Azure AD
3. SAML 2.0 with Google Workspace
4. OIDC with custom configuration
5. SCIM for user provisioning

---

## 6. Pattern 6: Data Entry Methods

**Cue:** The story supports "or" entry methods for the same data: typing, pasting, uploading, syncing.

**Recipe:** Each entry method is a slice.

### Worked Examples

#### Example 6a: Contact Management

**Before:** *"As a sales rep, I want to add contacts to my CRM."*

**After:**
1. Manual single-contact form
2. Bulk paste from spreadsheet
3. CSV import with field mapping
4. Sync from email integration (Gmail/Outlook)
5. Web-form submission directly to CRM
6. API ingest from external systems

#### Example 6b: Profile Picture

**Before:** *"As a user, I want to set my profile picture."*

**After:**
1. Upload from file
2. Take a photo from webcam
3. Import from Gravatar
4. Drag and drop from social profile URLs

---

## 7. Pattern 7: Deferred Performance / Quality

**Cue:** The story includes a performance, accessibility, or polish target ("under 1 second", "WCAG AA").

**Recipe:** Ship the functional baseline first. Each performance/quality improvement is a follow-up slice.

This pattern is among the most underused. Teams confuse "shipping at quality" with "shipping each story at final quality" -- they are different.

### Worked Examples

#### Example 7a: Dashboard Load Time

**Before:** *"As a user, I want my dashboard to load in under 1 second."*

**After:**
1. Render the dashboard with any performance (functional baseline; may take 5+ seconds)
2. Add server-side caching to bring load under 3 seconds
3. Add client-side rendering optimization to bring under 1 second
4. Add prefetch on hover to feel instant

#### Example 7b: Accessibility Compliance

**Before:** *"As a user, I want the form to be fully WCAG 2.1 AA compliant."*

**After:**
1. Form works functionally with mouse/touch (functional baseline)
2. Add keyboard navigation and focus management
3. Add ARIA labels and screen reader testing
4. Add high-contrast theme support
5. Full WCAG 2.1 AA audit pass

---

## 8. Pattern 8: Operations (CRUD)

**Cue:** The story implies "manage" / "administer" / "configure" -- a verb that hides multiple operations.

**Recipe:** Split by CRUD operation. Ship Read first (no risk of bad data); then Create (now you have data); then Delete (helps user recover from mistakes); then Update.

### Worked Examples

#### Example 8a: Saved Search Management

**Before:** *"As a user, I want to manage my saved searches."*

**After:**
1. View list of my saved searches (Read)
2. Save a new search from the search bar (Create)
3. Delete a saved search (Delete)
4. Rename a saved search (Update)
5. Share a saved search with a teammate (extended)

#### Example 8b: API Key Management

**Before:** *"As a developer, I want to manage my API keys."*

**After:**
1. View my existing API keys (Read; truncated for security)
2. Create a new API key with name and scope (Create)
3. Revoke an API key (Delete-equivalent)
4. Rotate an API key (Create + Revoke combined)

---

## 9. Pattern 9: Break Out a Spike

**Cue:** The team cannot estimate the story because of technical uncertainty: a new library, an unknown vendor API, a novel performance requirement.

**Recipe:** The first "slice" is a timeboxed spike. Its outcome is enough learning to apply Patterns 1-8.

### Spike Rules

- **Timeboxed.** 2-3 days maximum, regardless of progress.
- **Written outcome.** Define what we will know at the end ("we will know whether library X supports our auth flow").
- **Not user-facing.** Spikes produce learning, not features.
- **One owner.** A spike does not need a team; one engineer with focus.

### Worked Examples

#### Example 9a: SSO Integration

**Before:** *"As an admin, I want SSO with my company's identity provider."* (We have never built SSO.)

**After:**
1. **Spike (2 days):** Test SAML 2.0 against Okta, Azure AD, and Google Workspace using `python3-saml`. Determine whether one library supports all three. Output: written decision and example integration.
2. SAML 2.0 with Okta
3. SAML 2.0 with Azure AD
4. SAML 2.0 with Google Workspace

#### Example 9b: Real-Time Sync

**Before:** *"As a user, I want changes to sync to my team in real time."* (Team has not used WebSockets before.)

**After:**
1. **Spike (3 days):** Build a 2-user proof of concept with WebSockets; measure latency, server load, reconnection behavior. Output: architecture proposal.
2. Real-time presence indicators (lowest-risk first use)
3. Real-time text-field collaboration
4. Real-time conflict resolution

---

## 10. Optional Pattern: Major Effort First

**Cue:** A story's effort is dominated by a one-time infrastructure cost: building the integration framework, the import pipeline, the test harness.

**Recipe:** Ship the first instance (which absorbs the setup) as one story; ship each subsequent instance as a small story.

### Worked Example

#### Vendor Integration Framework

**Before:** *"As a user, I want to integrate with Salesforce, HubSpot, and Pipedrive."*

**After:**
1. Integrate with Salesforce (includes building the integration framework: OAuth, polling, webhook ingestion, mapping UI). Large story.
2. Integrate with HubSpot (reuses framework; OAuth + mapping config only). Small story.
3. Integrate with Pipedrive (reuses framework). Small story.

The cost is concentrated in slice 1; slices 2 and 3 are cheap.

---

## 11. Pattern Selection: Which to Try First

When a story is splittable in multiple ways, prefer:

1. **Pattern 9 (Spike)** if there is real technical uncertainty.
2. **Pattern 3 (Happy/Unhappy)** because it produces the simplest demoable first slice.
3. **Pattern 8 (CRUD)** because the order (Read -> Create -> Delete -> Update) is reliable.
4. **Pattern 1 (Workflow)** when the order is naturally sequential.
5. **Pattern 7 (Deferred Quality)** when performance is the stated requirement.
6. **Patterns 2, 4, 5, 6** when the story is fundamentally about variation.

---

## 12. Anti-Patterns

| Anti-Pattern | What Goes Wrong | Fix |
|--------------|-----------------|-----|
| **Horizontal slicing** | "Build the back-end, then the front-end" -- no slice is shippable alone | Force each slice to cross all layers |
| **Slice 1 = everything that doesn't fit later** | First slice is huge; subsequent slices are trivial | Re-order; first slice = smallest end-to-end value |
| **Spike with no outcome statement** | Spike runs forever, produces no decision | Always define "at the end we will know X" |
| **Splitting by team or layer ownership** | "Mobile slice", "Web slice", "API slice" -- platform variants, not user value | Split by user value first; address per-platform with Pattern 5 (Data Variations) only if user behavior differs |
| **Same pattern every time** | Team converges on one comfortable pattern; missing opportunities | Force a different pattern; review whether the convergence is real or lazy |
| **Splits violate INVEST-V** | Slices are not independently valuable | Each slice must have a user-payoff statement |
| **Splitting during refinement** | Refinement runs 90+ min; team exhausted | Pre-split the largest items before refinement; use refinement to validate |

---

## 13. INVEST Check After Splitting

Each slice should pass:

| Letter | Question |
|--------|----------|
| **I**ndependent | Can this slice ship without waiting on another slice? |
| **N**egotiable | Is the implementation open to engineering judgment? |
| **V**aluable | Can we state user payoff in one sentence? |
| **E**stimable | Can the team estimate it with confidence? |
| **S**mall | Will it fit in a sprint and below the team's 85th-percentile cycle time? |
| **T**estable | Can we describe observable acceptance criteria? |

If a slice fails any letter, re-split or restate.

---

## 14. References

- Lawrence, Richard. "Patterns for Splitting User Stories." 2009.
- Lawrence, Richard. *Story Splitting Flowchart*, 2012. (Canonical visual decision tree.)
- Cohn, Mike. *User Stories Applied for Agile Software Development*. Addison-Wesley, 2004.
- Patton, Jeff. *User Story Mapping: Discover the Whole Story, Build the Right Product*. O'Reilly, 2014.
- Adzic, Gojko. *Fifty Quick Ideas to Improve Your User Stories*. Neuri Consulting, 2014.
