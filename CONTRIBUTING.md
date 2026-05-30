# Contributing to claude-skills-hub

thanks for wanting to add to the corpus. this is how it works.

---

## ways to contribute

### 1. add a new skill source repo

found a repo full of `SKILL.md` files that isn't in the corpus yet?

1. open `sync-listed-sources.sh`
2. add your source to `SOURCE_INPUTS`:
   ```python
   {"kind": "repo", "repo": "owner/repo-name"},
   ```
3. run the sync:
   ```bash
   bash sync-listed-sources.sh
   ```
4. open a PR with:
   - updated `skills/`
   - updated `skills-manifest.txt`
   - updated `skills-source-map.tsv`

### 2. drop a single skill directly

1. create `skills/your-skill-name/SKILL.md`
2. use this frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: one clear sentence — what it does and when to use it
   ---
   ```
3. write the skill body (instructions, templates, examples)
4. PR it in

look at [`skills/karpathy-guidelines/SKILL.md`](./skills/karpathy-guidelines/SKILL.md) or [`skills/business-strategy-planning/SKILL.md`](./skills/business-strategy-planning/SKILL.md) for format examples.

### 3. fix a skill

see a skill that's outdated, broken, or missing frontmatter? just fix it and PR.

### 4. flag an unsafe skill

add the skill name to `SKIP_SKILLS` in `sync-listed-sources.sh`:

```python
SKIP_SKILLS: set[str] = {
    "agent-browser",   # Snyk High Risk
    "your-skill",      # reason
}
```

---

## PR checklist

- [ ] skill has valid `---` frontmatter with `name` and `description`
- [ ] skill directory name matches the `name` field
- [ ] `skills-manifest.txt` is updated (run `bash sync-local-skills.sh` or update manually)
- [ ] `skills-source-map.tsv` has an entry for new skills
- [ ] no secrets, credentials, or harmful instructions in skill content

---

## what makes a good skill

- **one clear trigger** — when should Claude activate this skill?
- **concrete examples** — show inputs, outputs, templates
- **action-first** — tell Claude what to do, not what it is
- **no hallucination bait** — don't reference external URLs, APIs, or docs that might change

---

## good first issues

check the [open issues](https://github.com/KunanonJ/claude-skills-hub/issues?q=is%3Aopen+label%3A%22good+first+issue%22) — these are small, well-scoped tasks perfect for a first PR.

---

## questions?

open an issue. we'll get back to you fast.
