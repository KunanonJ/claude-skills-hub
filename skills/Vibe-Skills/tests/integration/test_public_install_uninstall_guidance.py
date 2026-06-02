from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_root_readme_uses_host_explicit_uninstall_commands() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "uninstall.ps1 -HostId <host>" in readme
    assert "uninstall.sh --host <host>" in readme
    assert "Running `uninstall.ps1` or `uninstall.sh --host <host>`" not in readme


def test_root_chinese_readme_uses_host_explicit_uninstall_commands() -> None:
    readme = (REPO_ROOT / "README.zh.md").read_text(encoding="utf-8")

    assert "uninstall.ps1 -HostId <host>" in readme
    assert "uninstall.sh --host <host>" in readme
    assert "运行 `uninstall.ps1` 或 `uninstall.sh --host <host>`" not in readme
