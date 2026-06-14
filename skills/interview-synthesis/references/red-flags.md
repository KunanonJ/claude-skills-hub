# Red Flags: Interview Synthesis

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just produced themed insights, an opportunity solution tree, or a synthesis readout, scan the red flags below before sharing. Each red flag shows the *bad* and *good* version, anchored in Torres, Portigal, and Klement's synthesis methods.

---

## Red Flag 1: "Themes" That Are Just Quote Collections

**Symptom.** Output contains 7 "themes", each a paragraph header followed by 4 unrelated quotes. No abstraction; no insight; no opportunity surfaced.

**Why it's bad.** A theme should *explain* what is happening, not merely group what was said. Klein's narrative-based research and Torres' opportunity language both require interpretive abstraction. Theme-as-quote-collection is filing, not synthesis.

**Bad example:**
> "Theme: Onboarding. Quote 1: 'It took me a while.' Quote 2: 'Setup is confusing.' Quote 3: 'I didn't know what to do first.'"

**Good example:**
> "Theme: 'Users abandon onboarding because they cannot tell which step matters most.' Evidence: 6 of 8 interviewees described scanning the setup screen looking for 'the important one'. 3 abandoned at this scan. Quote: 'I just closed the tab because I didn't know which to do first.' Opportunity: signal the activation-critical step visually."

**How to catch it.** Read each theme. Is there an *interpretive sentence* that abstracts the quotes? If only quotes appear, it is not yet a theme.

---

## Red Flag 2: Confirmation-Coded Synthesis (Hearing What You Wanted)

**Symptom.** The themes that emerge from synthesis happen to match the PM's pre-interview hypothesis exactly. Contradicting evidence is absent.

**Why it's bad.** The brain pattern-matches; synthesis without discipline becomes hypothesis-confirmation. Portigal's "look for surprises and contradictions" rule is in the SKILL.md for this reason — if synthesis surfaces no surprises, it surfaced no truth.

**Bad example:**
> "PM hypothesis: 'Users want a faster checkout.' Synthesis themes: (1) Users want faster checkout. (2) Speed is the top priority. (3) Users wish checkout were faster." [Interview transcripts also mention pricing, trust, and confusion — none of which appear in the themes.]

**Good example:**
> "PM hypothesis: 'Users want faster checkout.' Synthesis themes: (1) Speed mentioned by 3 of 8 users, never as #1 issue. (2) Trust signals (privacy, security) mentioned by 7 of 8 as primary blocker. (3) Surprise: 4 users have abandoned because of pricing surprise at the last step. Revised hypothesis: trust > speed."

**How to catch it.** Does the synthesis contain at least one finding that contradicts or expands the original hypothesis? If none, you confirmation-coded.

---

## Red Flag 3: Themes That Combine Different Customer Segments

**Symptom.** A theme says "users want X" but pools data from enterprise admins, end users, and trial dropouts as if they were one group.

**Why it's bad.** Different segments have different jobs and pains. Pooling them produces themes that are technically true but operationally useless — you cannot build for "users in general." The synthesis must segment.

**Bad example:**
> "Theme: 'Users want better onboarding.'" (Source data: 4 admins setting up the workspace, 4 end-users in week 1.)

**Good example:**
> "Theme A (admins, 4 interviews): 'Setup takes too long because permissions UI is buried.' Theme B (end-users week 1, 4 interviews): 'I don't know what this product does until someone shows me.' Different jobs, different solutions."

**How to catch it.** Each theme should specify which segment it applies to. Cross-segment themes need separate validation per segment.

---

## Red Flag 4: Opportunity Solution Tree with No Branches Pruned

**Symptom.** Tree shows the outcome, 12 opportunities, and 47 solutions. Every opportunity has multiple branches. Nothing is prioritized.

**Why it's bad.** Torres' tree is a *prioritization* tool, not an inventory. An unpruned tree has the same content problem as an unsorted backlog: everything exists, nothing leads. The synthesis output must surface a top opportunity (or two), not a comprehensive map.

**Bad example:**
> Tree: outcome -> 12 opportunities -> 47 solutions. All equal, all listed.

**Good example:**
> Tree: outcome -> 12 opportunities. Top 3 highlighted (based on evidence frequency, severity, segment importance). Top opportunity has 4 candidate solutions, 1 marked as next experiment. Others parked for later."

**How to catch it.** Can you identify the top opportunity from the tree at a glance? If everything looks equal, the tree was inventory.

---

## Red Flag 5: Insights with No Quote Backing (Floating Claims)

**Symptom.** Synthesis says "users hate the onboarding" but no direct quote supports the claim. The PM remembers it that way.

**Why it's bad.** Quote-free insights are unverifiable. Stakeholders cannot pressure-test them; future PMs cannot trace them; the team builds on unsubstantiated claims. Portigal: the quote is the evidence; without it, the insight is fiction.

**Bad example:**
> "Insight: Users hate the onboarding."

**Good example:**
> "Insight: 5 of 8 users abandoned onboarding before completing setup. Quotes: 'I gave up after 10 minutes' (P3), 'I just closed the tab' (P5), 'I couldn't figure out where to start' (P7). Quantitative parallel: 78% drop-off observed in product analytics for the same flow."

**How to catch it.** Every insight should have 2+ supporting quotes plus, where possible, a quantitative parallel. Floating claims must be cut or sourced.

---

## Red Flag 6: Over-Aggregating ("Most Users Want X")

**Symptom.** Synthesis claims "most users want X" based on 3 of 5 interviewees mentioning it.

**Why it's bad.** N=5 is not "most users." Small qualitative samples reveal *what is possible* (themes worth exploring further), not *what is true* across the population. Overstating sample size in synthesis misleads downstream readers.

**Bad example:**
> "60% of users want feature X." (n=5 interviews; 3 mentioned it.)

**Good example:**
> "3 of 5 interviewees mentioned wanting feature X. This is a candidate theme worth surveying or testing quantitatively before treating as a population-level finding."

**How to catch it.** Search the doc for percentages. For each, is the sample size large enough to justify the percentage frame? If not, switch to "X of N" language.

---

## Red Flag 7: Missing the Contradictions

**Symptom.** Synthesis presents only the dominant pattern. Outlier quotes — "I actually love the slow onboarding because it teaches me" — are dropped because they don't fit.

**Why it's bad.** Contradictions are signal. They reveal segments you haven't named, edge cases that may be important, or assumptions you have wrong. Klement's JTBD synthesis specifically looks for the moment of switch and contradictory forces. Dropping outliers is dropping insight.

**Bad example:**
> Theme: "Users find onboarding too slow." (Drops the 2 users who mentioned wanting *more* guidance.)

**Good example:**
> Theme: "Users have polarized reactions to onboarding pace. 6 of 8 find it too slow; 2 of 8 find it too fast (one a non-native English speaker, one a non-technical buyer). The polarization suggests segmenting onboarding by user type."

**How to catch it.** Search the synthesis for "but", "however", "except", "interestingly". If these words are absent, you sanitized.

---

## Red Flag 8: Jumping to Solutions in the Theme

**Symptom.** Theme reads: "Theme: We should add a progress bar to onboarding." Solution masquerading as theme.

**Why it's bad.** Torres' opportunity language separates *problem space* (themes/opportunities) from *solution space* (candidate solutions). Conflating them locks the team into one solution when multiple may exist. The progress bar is one candidate solution to a deeper opportunity.

**Bad example:**
> "Theme: We need a progress bar in onboarding."

**Good example:**
> "Theme/Opportunity: Users abandon onboarding because they cannot see how close they are to completion. Candidate solutions: (a) progress bar, (b) step counter, (c) estimated time remaining, (d) skip-able optional steps."

**How to catch it.** Does the theme name a feature? If yes, you collapsed problem and solution.

---

## Red Flag 9: Synthesis Treated as a One-PM Task

**Symptom.** PM does the synthesis alone in a private doc. Designer and engineer see the output but not the process.

**Why it's bad.** Synthesis is interpretive; different perspectives surface different themes. Solo synthesis is biased by one person's lens. Torres' trio cadence (PM + Designer + Engineer reviewing interviews together) is the antidote.

**Bad example:**
> "PM synthesizes 8 interviews alone, presents themes to designer and engineer for awareness."

**Good example:**
> "Trio reviews transcript snippets together (3-hour session). Each codes independently; then compare. Disagreements (engineer reads one quote as feasibility risk, PM as customer need) are the most valuable signals."

**How to catch it.** Was synthesis solo or trio? Solo synthesis is a confirmation echo chamber.

---

## Red Flag 10: Synthesis Output Doesn't Generate Follow-Up Questions

**Symptom.** Synthesis report has insights and opportunities. No section for "what we still don't know."

**Why it's bad.** Discovery is continuous. Every round of synthesis should surface *evidence gaps* — assumptions still untested, segments still unrepresented, contradictions still unresolved. Without follow-up questions, the next interview round is unplanned.

**Bad example:**
> Synthesis report: 4 themes, 1 opportunity solution tree. End of doc.

**Good example:**
> Synthesis report: 4 themes, 1 OST, *plus* 'Open questions': (1) We have 0 interviews with churned users — need 3-5 for next round. (2) Theme B is well-evidenced for SMB; does it hold for enterprise? Need 4 enterprise interviews. (3) Quote 'I would have paid more' from P3 is intriguing but unverified; design a price-test interview."

**How to catch it.** Does the synthesis end with an open-questions list for the next round? If not, you closed the discovery loop prematurely.

---

## Red Flag 11: Themes Without Severity Calibration

**Symptom.** All themes presented as equal. A minor preference and a deal-breaker pain are listed side by side.

**Why it's bad.** Severity drives prioritization. A theme that 8 of 8 users find merely annoying ranks differently from one that 3 of 8 mention as why they would churn. Synthesis output must signal severity.

**Bad example:**
> "Theme 1: 'Users wish onboarding were nicer.' Theme 2: 'Users churn because of the data-loss bug.' (Listed side by side, no calibration.)"

**Good example:**
> "Theme 1: Cosmetic preference (low severity, 8/8 users mention, none churn over it). Theme 2: Data-loss bug (critical severity, 3/8 mention but all 3 churned within 30 days)."

**How to catch it.** Does each theme have an explicit severity tag (e.g., delight / preference / pain / blocker)? If not, prioritization is missing.

---

## Red Flag 12: Synthesis Document Nobody Reads Again

**Symptom.** The 12-page synthesis doc is presented once. Three months later, the team is debating something the doc already answered, but no one remembers.

**Why it's bad.** Synthesis is institutional memory. If the doc is unfindable or unreadable, that memory is lost. Format matters: a 12-page report buried in Confluence is functionally dead.

**Bad example:**
> 12-page narrative report. Posted in Confluence. Never re-opened.

**Good example:**
> Synthesis output formats: (a) 1-page executive summary (top 3 themes, top opportunity), (b) opportunity solution tree in Miro, (c) detailed report in Confluence with quote evidence, (d) Notion database of themes that gets queried each planning cycle. Linked from team handbook."

**How to catch it.** Will anyone open this document 3 months from now? If you cannot imagine the use case, restructure for findability.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Themes Are Just Quotes | Interpretive sentence above the quotes? |
| 2 | Confirmation Coding | At least one finding contradicts the original hypothesis? |
| 3 | Pooling Segments | Each theme tagged to specific segment? |
| 4 | OST Not Pruned | Top opportunity identifiable at a glance? |
| 5 | Insights Without Quotes | 2+ supporting quotes per insight? |
| 6 | Over-Aggregating | "X of N" not "60%" for n<20? |
| 7 | Missing Contradictions | Outliers acknowledged in the synthesis? |
| 8 | Theme = Solution | Theme names problem space, not feature? |
| 9 | Solo Synthesis | Trio coded independently before merging? |
| 10 | No Follow-Up Questions | Open-questions list at end of doc? |
| 11 | No Severity Calibration | Each theme tagged with severity? |
| 12 | Document Never Reread | Will anyone open this 3 months later? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/coding-method.md (for the affinity / clustering method, if present)
- customer-interview-script/references/red-flags.md (for upstream interview quality)
- identify-assumptions/references/red-flags.md (for opportunity-to-assumption mapping)
