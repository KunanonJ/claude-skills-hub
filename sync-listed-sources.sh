#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="$REPO_DIR/skills"
MANIFEST="$REPO_DIR/skills-manifest.txt"
SOURCE_MAP="$REPO_DIR/skills-source-map.tsv"

DEST_DIR="$DEST_DIR" MANIFEST="$MANIFEST" SOURCE_MAP="$SOURCE_MAP" python3 - <<'PY'
from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path


USER_AGENT = "codex-skill-updater/1.0"
SKIP_REPOS = {"KunanonJ/codex-skill-updater"}

SOURCE_INPUTS = [
    {"kind": "repo", "repo": "ComposioHQ/awesome-claude-skills"},
    {"kind": "org", "org": "ComposioHQ"},
    {"kind": "repo", "repo": "sickn33/antigravity-awesome-skills"},
    {"kind": "page", "url": "https://awesomeclaude.ai/awesome-claude-skills"},
    {"kind": "page", "url": "https://www.aitmpl.com/"},
    {"kind": "page", "url": "https://simonwillison.net/2025/Oct/16/claude-skills/"},
    {"kind": "page", "url": "https://mcpservers.org/agent-skills"},
    {"kind": "repo", "repo": "KunanonJ/codex-skill-updater"},
]


@dataclass(frozen=True)
class RepoSpec:
    owner: str
    repo: str
    ref: str | None
    subpath: str | None
    discovered_from: str

    @property
    def repo_key(self) -> str:
        return f"{self.owner}/{self.repo}"

    @property
    def clone_key(self) -> tuple[str, str, str | None]:
        return (self.owner, self.repo, self.ref)

    @property
    def spec_key(self) -> tuple[str, str, str | None, str | None]:
        return (self.owner, self.repo, self.ref, self.subpath)

    @property
    def clone_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}.git"

    @property
    def label(self) -> str:
        label = self.repo_key
        if self.ref:
            label = f"{label}@{self.ref}"
        if self.subpath:
            label = f"{label}:{self.subpath}"
        return label


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8", errors="replace")


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return response.read()


def sync_dir(src: Path, dest: Path) -> None:
    if shutil.which("rsync"):
        dest.mkdir(parents=True, exist_ok=True)
        run(["rsync", "-a", "--delete", "--exclude=.git", f"{src}/", f"{dest}/"])
        return

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".git"))


def extract_github_urls(page_html: str) -> list[str]:
    pattern = re.compile(r"https://github\.com/[^\s\"'<>)]+" , re.IGNORECASE)
    seen: set[str] = set()
    urls: list[str] = []
    for match in pattern.finditer(html.unescape(page_html)):
        url = match.group(0).rstrip(".,;:)]}")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def normalize_github_url(url: str, discovered_from: str) -> RepoSpec | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.lower() != "github.com":
        return None

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None

    owner = parts[0]
    repo = parts[1].removesuffix(".git")
    if owner.lower() == "sponsors":
        return None
    repo_key = f"{owner}/{repo}"
    if repo_key in SKIP_REPOS:
        return None

    if len(parts) == 2:
        return RepoSpec(owner=owner, repo=repo, ref=None, subpath=None, discovered_from=discovered_from)

    if parts[2] not in {"tree", "blob"} or len(parts) < 4:
        return None

    ref = parts[3]
    remainder = parts[4:]
    if parts[2] == "blob" and remainder and remainder[-1] == "SKILL.md":
        remainder = remainder[:-1]
    subpath = "/".join(remainder) if remainder else None
    return RepoSpec(owner=owner, repo=repo, ref=ref, subpath=subpath, discovered_from=discovered_from)


def repo_specs_from_page(url: str) -> list[RepoSpec]:
    html_text = fetch_text(url)
    specs: list[RepoSpec] = []
    seen: set[tuple[str, str, str | None, str | None]] = set()
    for github_url in extract_github_urls(html_text):
        spec = normalize_github_url(github_url, discovered_from=url)
        if spec is None:
            continue
        if spec.spec_key in seen:
            continue
        seen.add(spec.spec_key)
        specs.append(spec)
    return specs


def repo_specs_from_org(org: str) -> list[RepoSpec]:
    api_url = f"https://api.github.com/orgs/{org}/repos?per_page=100"
    repos = json.loads(fetch_text(api_url))
    specs: list[RepoSpec] = []
    for repo_info in sorted(repos, key=lambda item: item["name"].lower()):
        name = repo_info["name"]
        if "skill" not in name.lower():
            continue
        repo_key = f"{org}/{name}"
        if repo_key in SKIP_REPOS:
            continue
        specs.append(RepoSpec(owner=org, repo=name, ref=None, subpath=None, discovered_from=f"https://github.com/{org}"))
    return specs


def list_skill_dirs(search_root: Path, repo_root: Path) -> list[Path]:
    return sorted(path.parent.relative_to(repo_root) for path in search_root.rglob("SKILL.md"))


def extract_zip_bytes(zip_bytes: bytes, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "repo.zip"
    zip_path.write_bytes(zip_bytes)
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(dest_dir)
        top_levels = {name.split("/")[0] for name in zip_file.namelist() if name}
    if len(top_levels) != 1:
        raise RuntimeError("Unexpected archive layout.")
    return dest_dir / next(iter(top_levels))


def resolve_default_branch(owner: str, repo: str) -> str:
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_info = json.loads(fetch_text(api_url))
    branch = repo_info.get("default_branch")
    if not branch:
        raise RuntimeError(f"Unable to resolve default branch for {owner}/{repo}")
    return branch


def materialize_repo(spec: RepoSpec, dest_dir: Path) -> Path:
    cmd = ["git", "clone", "--depth", "1"]
    if spec.ref:
        cmd.extend(["--branch", spec.ref, "--single-branch"])
    cmd.extend([spec.clone_url, str(dest_dir)])

    try:
        run(cmd)
        return dest_dir
    except subprocess.CalledProcessError:
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        ref = spec.ref or resolve_default_branch(spec.owner, spec.repo)
        quoted_ref = urllib.parse.quote(ref, safe="")
        archive_url = f"https://codeload.github.com/{spec.owner}/{spec.repo}/zip/refs/heads/{quoted_ref}"
        return extract_zip_bytes(download_bytes(archive_url), dest_dir)


dest_dir = Path(os.environ["DEST_DIR"]).resolve()
manifest = Path(os.environ["MANIFEST"]).resolve()
source_map = Path(os.environ["SOURCE_MAP"]).resolve()

dest_dir.mkdir(parents=True, exist_ok=True)

ordered_specs: list[RepoSpec] = []
seen_specs: set[tuple[str, str, str | None, str | None]] = set()
for source_input in SOURCE_INPUTS:
    if source_input["kind"] == "repo":
        owner, repo = source_input["repo"].split("/", 1)
        repo_key = f"{owner}/{repo}"
        if repo_key in SKIP_REPOS:
            spec_list = []
        else:
            spec_list = [RepoSpec(owner=owner, repo=repo, ref=None, subpath=None, discovered_from=f"https://github.com/{owner}/{repo}")]
    elif source_input["kind"] == "page":
        spec_list = repo_specs_from_page(source_input["url"])
    elif source_input["kind"] == "org":
        spec_list = repo_specs_from_org(source_input["org"])
    else:
        raise RuntimeError(f"Unsupported source kind: {source_input['kind']}")

    for spec in spec_list:
        if spec.spec_key in seen_specs:
            continue
        seen_specs.add(spec.spec_key)
        ordered_specs.append(spec)

with tempfile.TemporaryDirectory(prefix="codex-listed-source-sync-") as tmp_root:
    tmp_root_path = Path(tmp_root)
    clone_cache: dict[tuple[str, str, str | None], Path] = {}
    owned: dict[str, tuple[RepoSpec, Path, Path]] = {}
    repos_with_skills: set[str] = set()

    for index, spec in enumerate(ordered_specs, start=1):
        clone_root = clone_cache.get(spec.clone_key)
        if clone_root is None:
            repo_dir = tmp_root_path / f"repo-{index:04d}-{spec.owner}-{spec.repo}".replace("/", "-")
            try:
                clone_root = materialize_repo(spec, repo_dir)
            except Exception as exc:
                print(f"Skipped {spec.label}: {exc}")
                continue
            clone_cache[spec.clone_key] = clone_root

        search_root = clone_root / spec.subpath if spec.subpath else clone_root
        if not search_root.exists():
            continue

        rel_skill_dirs = list_skill_dirs(search_root, clone_root)
        if not rel_skill_dirs:
            continue

        repos_with_skills.add(spec.label)
        for rel_skill_dir in rel_skill_dirs:
            skill_name = rel_skill_dir.name or spec.repo
            if skill_name not in owned:
                owned[skill_name] = (spec, clone_root, rel_skill_dir)

    current_names = sorted(owned)
    current_name_set = set(current_names)

    for existing_dir in sorted(path for path in dest_dir.iterdir() if path.is_dir()):
        if existing_dir.name not in current_name_set:
            shutil.rmtree(existing_dir)
            print(f"Removed {existing_dir.name}")

    for skill_name in current_names:
        spec, clone_root, rel_skill_dir = owned[skill_name]
        sync_dir(clone_root / rel_skill_dir, dest_dir / skill_name)

    manifest.write_text("".join(f"{name}\n" for name in current_names))

    source_map_lines = ["skill_name\trepo_spec\trelative_path\tdiscovered_from"]
    for skill_name in current_names:
        spec, _, rel_skill_dir = owned[skill_name]
        source_map_lines.append(
            f"{skill_name}\t{spec.label}\t{rel_skill_dir.as_posix()}\t{spec.discovered_from}"
        )
    source_map.write_text("".join(f"{line}\n" for line in source_map_lines))

    print(f"Input sources: {len(SOURCE_INPUTS)}")
    print(f"Resolved GitHub sources: {len(ordered_specs)}")
    print(f"GitHub sources with skills: {len(repos_with_skills)}")
    print(f"Synced skills: {len(current_names)}")
    print(f"Manifest: {manifest}")
    print(f"Source map: {source_map}")
PY
