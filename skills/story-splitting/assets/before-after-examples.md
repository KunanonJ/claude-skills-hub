# Before/After Story Splitting Examples

Fifteen worked examples across SaaS, mobile, B2B, and platform scenarios. Each shows the original too-large story, identifies which Lawrence patterns apply, and gives the ordered slice list.

---

## SaaS

### 1. Onboarding Wizard (Patterns: 1, 3)

**Before:** *"As a new user, I want a guided onboarding wizard so I activate quickly."*

**After (ordered):**
1. Step 1 of wizard: welcome screen + account confirmation (Pattern 1)
2. Step 2 of wizard: connect a data source (Pattern 1)
3. Step 3 of wizard: invite a teammate (Pattern 1)
4. Step 4 of wizard: build first dashboard (Pattern 1)
5. Skip-and-resume support (Pattern 3: unhappy path of "I left before finishing")
6. Mobile-optimized wizard (Pattern 5: data variation by device)

---

### 2. Reporting and Export (Patterns: 4, 7)

**Before:** *"As a user, I want fast, exportable reports in multiple formats."*

**After:**
1. View a report on screen (no export yet; functional baseline) (Pattern 7)
2. Export current view to CSV (Pattern 4)
3. Export current view to PDF (Pattern 4)
4. Cache report data to load in < 3 seconds (Pattern 7)
5. Schedule recurring email export (Pattern 4)
6. Cache aggressively to load in < 1 second (Pattern 7)

---

### 3. Subscription Management (Patterns: 8, 2, 3)

**Before:** *"As a customer, I want to manage my subscription -- view, upgrade, downgrade, cancel, change payment, retry failures."*

**After:**
1. View my current plan and renewal date (Pattern 8: Read)
2. Cancel my subscription effective end of period (Pattern 8: Delete + Pattern 2: simplest rule)
3. Upgrade my plan with immediate proration (Pattern 8: Update + Pattern 2)
4. Downgrade my plan effective end of period (Pattern 2: deferred rule)
5. Update my payment method (Pattern 4: input variation -- card vs bank)
6. Retry a failed payment from billing page (Pattern 3: unhappy path)
7. Cancel a scheduled cancellation (Pattern 3: edge case last)

---

### 4. Notification Preferences (Patterns: 4, 8)

**Before:** *"As a user, I want fine-grained control over notifications across channels and event types."*

**After:**
1. View my current notification settings (Pattern 8: Read)
2. Toggle email notifications on/off globally (simplest control)
3. Toggle in-app notifications globally
4. Per-event-type opt-out for email (Pattern 2: business-rule variation)
5. Per-event-type opt-out for in-app
6. Add SMS notification channel (Pattern 4: output variation)
7. Add Slack/Teams notification channel (Pattern 4)
8. Quiet hours (Pattern 2: time-based rule)

---

### 5. Search (Patterns: 5, 7)

**Before:** *"As a user, I want fast, fuzzy search across all my data with autocomplete and filters."*

**After:**
1. Search by exact name match (Pattern 5: simplest data variation)
2. Search by substring (case-insensitive) (Pattern 5)
3. Search with fuzzy matching for typos (Pattern 5)
4. Add result-type filters (Pattern 2: business-rule variation)
5. Autocomplete suggestions (Pattern 7: progressive quality)
6. Search across multiple indexed fields (Pattern 5)
7. Optimize search latency to < 100ms p95 (Pattern 7)

---

## Mobile

### 6. Push Notifications (Patterns: 9, 5)

**Before:** *"As a user, I want push notifications for important events."* (Team has not implemented push before.)

**After:**
1. **Spike (3 days):** Set up APNs and FCM with provider X; build minimal end-to-end push to test devices. Decide on architecture. (Pattern 9)
2. Push for one event type (new message received) on iOS (Pattern 5: platform first)
3. Same on Android (Pattern 5)
4. Push for second event type (mention) (Pattern 2: event-type variation)
5. Per-event-type opt-out in app settings
6. Rich push with images and actions (Pattern 7: quality)

---

### 7. Offline Mode (Patterns: 9, 1, 7)

**Before:** *"As a user, I want the app to work offline with full sync when I reconnect."*

**After:**
1. **Spike (3 days):** Evaluate local DB options (Realm, SQLite, Core Data); decide sync conflict strategy. (Pattern 9)
2. View previously loaded data while offline (Pattern 1: read step)
3. Queue local edits and apply on reconnect (Pattern 1: write step, last-write-wins)
4. Show offline indicator and conflict prompts (Pattern 7: quality)
5. Conflict resolution UI for non-trivial conflicts (Pattern 2: business-rule variation)

---

### 8. Camera Capture (Patterns: 3, 7)

**Before:** *"As a user, I want to attach a photo, scanned doc, or PDF to a message."*

**After:**
1. Take a photo and attach (happy path, photo only) (Pattern 3)
2. Choose existing photo from camera roll (Pattern 6: data-entry method)
3. Show error if camera permission denied (Pattern 3: unhappy path)
4. Show error if storage full (Pattern 3: unhappy path)
5. Scan document with auto edge-detection (Pattern 7: quality upgrade)
6. Attach PDF from files app (Pattern 5: data type variation)

---

## B2B / Enterprise

### 9. SSO Integration (Patterns: 9, 5)

**Before:** *"As an admin, I want SSO with any major identity provider."*

**After:**
1. **Spike (2 days):** Test python3-saml against Okta, Azure AD, Google. (Pattern 9)
2. SAML 2.0 with Okta (most common in our base) (Pattern 5)
3. SAML 2.0 with Azure AD (Pattern 5)
4. SAML 2.0 with Google Workspace (Pattern 5)
5. OIDC with custom configuration (Pattern 5)
6. SCIM user provisioning (Pattern 4: integration variation)

---

### 10. Audit Log (Patterns: 8, 4)

**Before:** *"As a compliance officer, I want a complete audit log I can search and export."*

**After:**
1. View paginated audit-log entries in UI (Pattern 8: Read)
2. Filter by user (Pattern 4: input variation)
3. Filter by event type
4. Filter by date range
5. Export filtered results to CSV (Pattern 4: output variation)
6. Schedule monthly export to S3 (Pattern 4)
7. Tamper-evident log signing (Pattern 7: quality upgrade)

---

### 11. Role-Based Access Control (Patterns: 8, 2)

**Before:** *"As an admin, I want fine-grained RBAC with custom roles."*

**After:**
1. View built-in roles and their permissions (Pattern 8: Read)
2. Assign a built-in role to a user (Pattern 8: Update; Pattern 2 simplest rule)
3. Revoke a role from a user (Pattern 8: Delete)
4. Create a custom role from a built-in template (Pattern 8: Create)
5. Define permissions on a custom role (Pattern 2: rule variation)
6. Audit who has which role (Pattern 8: Read; secondary view)
7. Bulk role assignment via CSV (Pattern 6: entry method)

---

## Platform / Infrastructure

### 12. API Rate Limiting (Patterns: 7, 2)

**Before:** *"As a platform, we need configurable rate limits per plan tier with smart backoff."*

**After:**
1. Apply a single global rate limit across all plans (functional baseline; Pattern 7)
2. Per-plan-tier rate limit (Pattern 2: business-rule variation)
3. Per-endpoint rate limit (Pattern 2)
4. 429 response with Retry-After header (Pattern 3: unhappy path with respect)
5. Burst allowance per plan (Pattern 2)
6. Adaptive rate limit based on load (Pattern 7: quality)

---

### 13. Data Import Pipeline (Patterns: "Major Effort First", 5)

**Before:** *"As a customer, I want to import data from Salesforce, HubSpot, and Pipedrive."*

**After:**
1. Salesforce integration: build full pipeline (auth, polling, mapping UI, error handling, monitoring). Large story. (Major Effort First)
2. HubSpot integration: reuse pipeline framework; new connector + mapping config. Small story. (Pattern 5)
3. Pipedrive integration: same. Small story. (Pattern 5)
4. Marketo integration: same. Small story. (Pattern 5)
5. Custom REST integration via mapping UI. (Pattern 5)

---

### 14. Webhook Delivery (Patterns: 3, 7)

**Before:** *"As an integrator, I want reliable webhook delivery with retries and an admin UI."*

**After:**
1. Deliver a webhook on event with no retry (happy path; Pattern 3)
2. Retry failed webhook delivery with exponential backoff (Pattern 3: unhappy path)
3. View delivery history for one webhook endpoint (Pattern 8: Read)
4. Test webhook from admin UI (Pattern 4: entry method)
5. Replay a failed webhook delivery (Pattern 8: Update equivalent)
6. Per-endpoint dead-letter queue with alerting (Pattern 7: quality)

---

### 15. Feature Flag System (Patterns: 9, 8, 2)

**Before:** *"As a team, we want a feature-flag system with targeting, rollout percentages, and audit."*

**After:**
1. **Spike (2 days):** Compare LaunchDarkly, Unleash, and a build vs buy memo. (Pattern 9)
2. Toggle a boolean flag on/off globally (Pattern 8: Update; simplest)
3. Target a flag to a specific user (Pattern 2: simplest targeting rule)
4. Target by user attribute (e.g., plan tier) (Pattern 2)
5. Percentage-based rollout (Pattern 2)
6. Audit history of flag changes (Pattern 8: Read on history)
7. Flag dependencies and prerequisites (Pattern 2: advanced rule)

---

## How to Use These Examples

When refining a story that feels too large:

1. Find the closest analog in the list above.
2. Identify the patterns applied.
3. Apply the same patterns to your story.
4. Walk through the decision tree in `SKILL.md` to verify nothing earlier in the tree applies.

The goal is not to copy these splits but to internalize the moves so they become reflexive in refinement.
