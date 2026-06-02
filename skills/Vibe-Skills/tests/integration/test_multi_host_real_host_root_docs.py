from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_public_install_docs_prefer_real_host_roots_for_requested_hosts() -> None:
    zh_rules = (REPO_ROOT / "docs/install/installation-rules.md").read_text(encoding="utf-8")
    en_rules = (REPO_ROOT / "docs/install/installation-rules.en.md").read_text(encoding="utf-8")
    zh_recommended = (REPO_ROOT / "docs/install/recommended-full-path.md").read_text(encoding="utf-8")
    en_recommended = (REPO_ROOT / "docs/install/recommended-full-path.en.md").read_text(encoding="utf-8")

    assert 'CLAUDE_HOME="$HOME/.claude"' in zh_rules
    assert 'CLAUDE_HOME="$HOME/.claude"' in en_rules
    assert "~/.cursor" in zh_rules
    assert "~/.cursor" in en_rules
    assert "~/.codeium/windsurf" in zh_rules
    assert "~/.codeium/windsurf" in en_rules
    assert "~/.openclaw" in zh_rules
    assert "~/.openclaw" in en_rules
    assert "~/.config/opencode" in zh_rules
    assert "~/.config/opencode" in en_rules

    assert 'CLAUDE_HOME="$HOME/.claude" bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile full' in zh_recommended
    assert 'CLAUDE_HOME="$HOME/.claude" bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile full' in en_recommended
    assert "~/.cursor" in zh_recommended
    assert "~/.cursor" in en_recommended
    assert "~/.codeium/windsurf" in zh_recommended
    assert "~/.codeium/windsurf" in en_recommended
    assert "~/.openclaw" in zh_recommended
    assert "~/.openclaw" in en_recommended
    assert "~/.config/opencode" in zh_recommended
    assert "~/.config/opencode" in en_recommended


def test_host_specific_docs_stop_describing_isolated_roots_as_defaults() -> None:
    zh_openclaw = (REPO_ROOT / "docs/install/openclaw-path.md").read_text(encoding="utf-8")
    en_openclaw = (REPO_ROOT / "docs/install/openclaw-path.en.md").read_text(encoding="utf-8")
    zh_opencode = (REPO_ROOT / "docs/install/opencode-path.md").read_text(encoding="utf-8")
    en_opencode = (REPO_ROOT / "docs/install/opencode-path.en.md").read_text(encoding="utf-8")

    assert "~/.openclaw" in zh_openclaw
    assert "~/.openclaw" in en_openclaw
    assert "~/.config/opencode" in zh_opencode
    assert "~/.config/opencode" in en_opencode


def test_configuration_guides_keep_real_follow_up_paths_for_host_managed_surfaces() -> None:
    zh_config = (REPO_ROOT / "docs/install/configuration-guide.md").read_text(encoding="utf-8")
    en_config = (REPO_ROOT / "docs/install/configuration-guide.en.md").read_text(encoding="utf-8")

    assert ".vibeskills/host-settings.json" in zh_config
    assert ".vibeskills/host-closure.json" in zh_config
    assert ".vibeskills/host-settings.json" in en_config
    assert ".vibeskills/host-closure.json" in en_config

    assert "~/.config/opencode/opencode.json" in zh_config
    assert "opencode.json.example" in zh_config
    assert "~/.config/opencode/opencode.json" in en_config
    assert "opencode.json.example" in en_config
