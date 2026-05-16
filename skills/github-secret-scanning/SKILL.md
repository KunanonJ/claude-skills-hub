---
name: github-secret-scanning
description: "Configure GitHub Secret Protection — secret scanning, push protection, custom patterns, and partner alerts. Trigger when the user wants to prevent credential leaks, enable secret scanning, set up push protection, write custom regex patterns for proprietary tokens, or audit existing leaks. Sourced from github.com/skills/introduction-to-secret-scanning."
---

# GitHub Secret Protection

GitHub leaks over a million tokens to its platform every year. This is preventable infrastructure — turn it on, configure it well, and treat alerts as production incidents.

## What Secret Protection Includes

| Feature | Purpose |
|---|---|
| **Secret scanning** | Scans existing repo content + history for known token patterns (AWS, Stripe, GitHub PATs, etc.). |
| **Push protection** | Blocks the push that introduces a secret, before it ever lands on the remote. |
| **Validity checks** | Calls the partner API to determine if the leaked token is still active. |
| **Custom patterns** | Regex-defined patterns for proprietary secrets the partner program doesn't cover. |
| **Bypass + audit** | Lets developers bypass push protection (with reason) — every bypass is logged. |

## Enabling for a Repo

**Settings → Code security and analysis → Secret Protection → Enable.**

For public repos: free, automatic.
For private/internal: requires GitHub Advanced Security (paid; included with Enterprise + GHAS).

Org-wide enablement: **Org Settings → Code security → "Enable for all eligible repositories."** New repos inherit the setting.

## Custom Patterns

When you have proprietary tokens (internal API keys, partner integration secrets):

**Repo Settings → Secret Protection → Custom patterns → New pattern.**

Define:
- **Name**: `Internal Service Token`
- **Secret format** (regex): `int_[a-zA-Z0-9]{32}`
- **Before secret** (regex, optional): `(?:token|key|secret)["']?\s*[:=]\s*["']?`
- **After secret** (regex, optional): `["']?[\s,]`
- **Additional matches**: `must match`, `must not match` — to narrow further.

Test with "Dry run" against a recent push before enabling enforcement. False positives are common with short or low-entropy tokens; tighten the regex.

Once defined, also enable:
- ✅ **Push protection** for this pattern
- ✅ **Generic secret detection** (catches arbitrary high-entropy strings)

## Push Protection in Practice

When a developer pushes a commit containing a token:

```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote:
remote: - GITHUB PUSH PROTECTION
remote:   —————————————————————————————————————————
remote:    Resolve the following violations before pushing again
remote:
remote:    - GITHUB-PUSH-PROTECTION
remote:        Locations:
remote:          - commit: a1b2c3d
remote:            path: config/secrets.js:42
remote:    - Secret type: AWS Access Key ID
remote:        Detected secret: AKIA****EXAMPLE
remote:
remote:   To bypass, click the URL: https://github.com/...
```

Developers can:
1. **Remove the secret** (preferred): scrub from git history (`git filter-repo`), rotate the key, retry the push.
2. **Bypass with reason**: `It's a test value`, `False positive`, `I'll fix it later`. The bypass is logged — security teams should review weekly.

## Responding to an Active Alert

When secret-scanning flags a token in a commit that already landed:

1. **Rotate the token immediately** — assume it's compromised. Token in a private repo is still a risk: an insider could exfiltrate.
2. **Revoke the old token** at the source provider.
3. **Validate**: check the provider's audit log for unauthorized use during the leak window.
4. **Remove from history** if practical:
   ```bash
   git filter-repo --replace-text <(echo "AKIAEXAMPLE==>REDACTED")
   git push --force-with-lease
   ```
   Force-push only after coordinating with collaborators. GitHub keeps cached views of forks.
5. **Mark the alert resolved** with reason: `revoked` or `false positive`.

## Validity Checks (Partner Integration)

GitHub partners with cloud providers (AWS, Azure, GCP, Stripe, OpenAI, Anthropic, etc.) to check token validity in real time. When secret-scanning detects a known partner pattern, GitHub calls the partner's API to ask "is this still valid?" If yes, the partner may auto-revoke or notify the customer.

This means: even if you can't immediately rotate, the partner often does it for you. Don't rely on that — rotate explicitly.

## CLI Audit

```bash
gh api repos/$OWNER/$REPO/secret-scanning/alerts --jq '.[] | {number, secret_type, state, html_url}'
```

Filter by state:
```bash
gh api repos/$OWNER/$REPO/secret-scanning/alerts?state=open
```

## Anti-Patterns

- ❌ Disabling push protection because "it slows people down" — slowing down a token leak is the point.
- ❌ Treating bypass reasons as a checkbox — actually triage what was bypassed weekly.
- ❌ Not enabling for old repos — historical leaks still expose data.
- ❌ Custom patterns with broad regex like `[a-z]{32}` — generates noise, gets ignored.
- ❌ Removing a secret with `git rm` without `--filter-repo` — still in history.
- ❌ Rotating the token but not invalidating downstream caches/sessions tied to it.

## Quick Checklist

- [ ] Secret scanning enabled at org level for all repos
- [ ] Push protection enabled for all known-pattern types
- [ ] Custom patterns defined for internal token formats
- [ ] Bypasses audited at least weekly
- [ ] Runbook documented for token revocation (per provider)
- [ ] `.gitignore` covers `.env*`, `*.key`, `secrets.json` as defense-in-depth
- [ ] Pre-commit hook (e.g. `gitleaks`) runs locally before push as a faster feedback loop

## References

- Source course: https://github.com/skills/introduction-to-secret-scanning
- Docs: https://docs.github.com/en/code-security/secret-scanning
- Custom patterns: https://docs.github.com/en/code-security/secret-scanning/defining-custom-patterns-for-secret-scanning
- Partner program: https://docs.github.com/en/code-security/secret-scanning/secret-scanning-partner-program
- gitleaks (pre-commit): https://github.com/gitleaks/gitleaks
