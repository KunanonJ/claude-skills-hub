"""Quality checks for the lean claude-skills-hub corpus."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MANIFEST = ROOT / "skills-manifest.txt"
SOURCE_MAP = ROOT / "skills-source-map.tsv"

KEEP_SKILLS = {
    "analyze-codebase-for-mcp",
    "api-analyzer",
    "api-design-principles",
    "api-documentation-generator",
    "api-security-best-practices",
    "architecture-decision-records",
    "architecture-patterns",
    "backend-api-design",
    "backend-dev-guidelines",
    "backend-security-coder",
    "browser-screenshot-diff",
    "browser-testing-with-devtools",
    "bug-hunter",
    "build-custom-mcp-server",
    "ci-cd-patterns",
    "clean-code",
    "cloudflare-deploy",
    "code-deduplication",
    "code-documentation-code-explain",
    "code-review",
    "codebase-cleanup-tech-debt",
    "codebase-onboarding",
    "codeql",
    "commit",
    "commit-hygiene",
    "context7-auto-research",
    "create-dockerfile",
    "database-design",
    "debugging-toolkit-smart-debug",
    "dependency-check",
    "deployment-patterns",
    "design-to-code",
    "django-patterns",
    "docker-patterns",
    "documentation",
    "e2e-testing-patterns",
    "fastapi-pro",
    "frontend-a11y",
    "frontend-design-direction",
    "frontend-dev-guidelines",
    "frontend-developer",
    "frontend-security-coder",
    "git-pr-review",
    "git-pr-workflows-onboard",
    "git-worktree",
    "github-actions-advanced",
    "github-actions-creator",
    "github-pr-review",
    "golang-patterns",
    "implementing-secret-scanning-with-gitleaks",
    "javascript-mastery",
    "javascript-testing-patterns",
    "kubernetes-architect",
    "kubernetes-patterns",
    "learn-codebase",
    "mcp-integration",
    "mcp-server-patterns",
    "modern-javascript-patterns",
    "mutation-testing",
    "nextjs-app-router-patterns",
    "nextjs-best-practices",
    "nodejs-backend-patterns",
    "openai-docs",
    "performance-optimizer",
    "playwright",
    "playwright-cli",
    "postgresql",
    "property-based-testing",
    "python-best-practices",
    "python-packaging",
    "python-testing",
    "python-testing-patterns",
    "react-best-practices",
    "react-doctor",
    "react-patterns",
    "react-testing",
    "refactoring-patterns",
    "rust-pro",
    "rust-testing",
    "secrets-management",
    "security-auditor",
    "security-review",
    "setup-github-actions-ci",
    "setup-pre-commit",
    "software-architecture",
    "springboot-patterns",
    "sql-optimization-patterns",
    "systematic-debugging",
    "tailwind-patterns",
    "terraform-best-practices",
    "terraform-specialist",
    "test-driven-development",
    "testing-patterns",
    "typescript-advanced-types",
    "typescript-expert",
    "ui-review",
    "unit-testing-test-generate",
    "using-git-worktrees",
    "vercel-deployment",
    "web-performance-optimization",
}


def read_manifest() -> list[str]:
    return [line.strip() for line in MANIFEST.read_text().splitlines() if line.strip()]


def read_source_map() -> list[dict[str, str]]:
    with SOURCE_MAP.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def top_level_skill_dirs() -> list[str]:
    return sorted(path.name for path in SKILLS_DIR.iterdir() if path.is_dir())


def top_level_skill_files() -> list[str]:
    return sorted(path.name for path in SKILLS_DIR.iterdir() if path.is_file())


def broken_symlinks() -> list[str]:
    return sorted(
        str(path.relative_to(ROOT))
        for path in SKILLS_DIR.rglob("*")
        if path.is_symlink() and not path.exists()
    )


def parse_frontmatter(skill_name: str) -> dict[str, str]:
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    text = skill_path.read_text(errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata


def report(errors: list[str], warnings: list[str]) -> int:
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


def validate_lean(_: argparse.Namespace) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    manifest = read_manifest()
    manifest_set = set(manifest)
    source_rows = read_source_map()
    source_names = [row["skill_name"] for row in source_rows]
    top_dirs = top_level_skill_dirs()

    if len(manifest) != 100:
        errors.append(f"skills-manifest.txt must contain exactly 100 entries, got {len(manifest)}")
    if len(manifest_set) != len(manifest):
        errors.append("skills-manifest.txt contains duplicate names")
    if manifest != sorted(manifest):
        errors.append("skills-manifest.txt must be sorted alphabetically")
    if manifest_set != KEEP_SKILLS:
        errors.append("skills-manifest.txt does not match the canonical 100-skill keep list")

    for skill_name in manifest:
        if not (SKILLS_DIR / skill_name / "SKILL.md").is_file():
            errors.append(f"manifest skill is missing a resolvable SKILL.md: {skill_name}")

    top_dir_set = set(top_dirs)
    extra_dirs = sorted(top_dir_set - KEEP_SKILLS)
    missing_dirs = sorted(KEEP_SKILLS - top_dir_set)
    extra_files = top_level_skill_files()
    if extra_dirs:
        errors.append(f"unexpected top-level skill directories: {', '.join(extra_dirs)}")
    if missing_dirs:
        errors.append(f"missing top-level skill directories: {', '.join(missing_dirs)}")
    if extra_files:
        errors.append(f"unexpected top-level files under skills/: {', '.join(extra_files)}")

    if len(source_rows) != 100:
        errors.append(f"skills-source-map.tsv must contain exactly 100 data rows, got {len(source_rows)}")
    if set(source_names) != manifest_set:
        errors.append("skills-source-map.tsv skill names must match skills-manifest.txt")
    if len(set(source_names)) != len(source_names):
        errors.append("skills-source-map.tsv contains duplicate skill names")

    for row in source_rows:
        for field in ("skill_name", "repo_spec", "relative_path", "discovered_from"):
            if not row.get(field, "").strip():
                errors.append(f"skills-source-map.tsv row has blank {field}: {row}")

    dangling = broken_symlinks()
    if dangling:
        errors.append(f"broken symlinks under skills/: {', '.join(dangling[:10])}")

    if not errors:
        print("Lean corpus validation passed: 100 skills, manifest/source map aligned.")
    return report(errors, warnings)


def normalize_metadata(args: argparse.Namespace) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    manifest = read_manifest()
    for skill_name in manifest:
        skill_path = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"missing SKILL.md: {skill_name}")
            continue
        metadata = parse_frontmatter(skill_name)
        if not metadata.get("name"):
            errors.append(f"missing frontmatter name: {skill_name}")
        if not metadata.get("description"):
            errors.append(f"missing frontmatter description: {skill_name}")
        description = metadata.get("description", "")
        if description and not description.lower().startswith("this skill should be used when"):
            warnings.append(f"weak description trigger format: {skill_name}")

    if args.check:
        if not errors:
            print("Metadata check passed.")
        return report(errors, warnings)

    print("No metadata rewrite mode is implemented yet; use --check.")
    return report(errors, warnings)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate-lean")
    validate_parser.set_defaults(func=validate_lean)

    normalize_parser = subparsers.add_parser("normalize-metadata")
    normalize_parser.add_argument("--check", action="store_true", help="Check metadata without rewriting files.")
    normalize_parser.set_defaults(func=normalize_metadata)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
