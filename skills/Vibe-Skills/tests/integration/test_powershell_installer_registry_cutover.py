from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_powershell_installer_resolves_adapter_metadata_from_registry_surface() -> None:
    content = (REPO_ROOT / 'scripts' / 'install' / 'Install-VgoAdapter.ps1').read_text(encoding='utf-8')

    assert r'scripts\common\Resolve-VgoAdapter.ps1' not in content
    assert r'config\adapter-registry.json' in content
    assert r'adapters\index.json' in content


def test_powershell_installer_internal_corpus_is_strictmode_and_self_copy_safe() -> None:
    content = (REPO_ROOT / 'scripts' / 'install' / 'Install-VgoAdapter.ps1').read_text(encoding='utf-8')

    assert "$corpus.PSObject.Properties.Name -contains 'enabled'" in content
    assert "[bool]$corpus.enabled" in content
    assert "$destinationFullName" in content
    assert "$bundledFullName" in content
    assert "$destinationFullName -ne $bundledFullName" in content
