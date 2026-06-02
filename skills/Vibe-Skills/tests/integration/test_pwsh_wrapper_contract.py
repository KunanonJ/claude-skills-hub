from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_powershell_install_and_uninstall_wrappers_delegate_to_vgo_cli() -> None:
    install_content = (REPO_ROOT / 'install.ps1').read_text(encoding='utf-8')
    check_content = (REPO_ROOT / 'check.ps1').read_text(encoding='utf-8')
    uninstall_content = (REPO_ROOT / 'uninstall.ps1').read_text(encoding='utf-8')

    assert 'vgo_cli.main' in install_content
    assert 'vgo_cli.main' in uninstall_content
    assert 'scripts\\install\\Install-VgoAdapter.ps1' not in install_content
    assert 'scripts\\check\\Check-VgoAdapter.ps1' not in check_content
    assert 'scripts\\uninstall\\Uninstall-VgoAdapter.ps1' not in uninstall_content
    assert 'no longer falls back to legacy installer scripts' in install_content
    assert 'no longer falls back to legacy uninstall scripts' in uninstall_content


def test_powershell_install_wrapper_keeps_codex_payload_contract_anchor() -> None:
    install_content = (REPO_ROOT / 'install.ps1').read_text(encoding='utf-8')

    assert 'plugins-manifest.codex.json' in install_content


def test_powershell_install_wrapper_searches_static_windows_python_312_and_313_first() -> None:
    install_content = (REPO_ROOT / 'install.ps1').read_text(encoding='utf-8')
    static_start = install_content.find('$absoluteCandidates = @(')
    assert static_start != -1
    static_end = install_content.find('foreach ($programFilesRoot', static_start)
    assert static_end != -1
    static_block = install_content[static_start:static_end]

    assert 'C:\\Python313\\python.exe' in static_block
    assert 'C:\\Python312\\python.exe' in static_block
    assert 'C:\\Python311\\python.exe' in static_block
    assert static_block.index('C:\\Python313\\python.exe') < static_block.index('C:\\Python312\\python.exe')
    assert static_block.index('C:\\Python312\\python.exe') < static_block.index('C:\\Python311\\python.exe')


def test_powershell_install_wrapper_searches_user_local_python_312_and_313() -> None:
    install_content = (REPO_ROOT / 'install.ps1').read_text(encoding='utf-8')
    localappdata_index = install_content.find("if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA))")
    assert localappdata_index != -1
    localappdata_end = install_content.find('foreach ($candidatePath in $absoluteCandidates)', localappdata_index)
    assert localappdata_end != -1
    localappdata_block = install_content[localappdata_index:localappdata_end]

    assert "Programs\\Python\\Python313\\python.exe" in localappdata_block
    assert "Programs\\Python\\Python312\\python.exe" in localappdata_block
    assert "Programs\\Python\\Python311\\python.exe" in localappdata_block
    assert localappdata_block.index("Programs\\Python\\Python313\\python.exe") < localappdata_block.index(
        "Programs\\Python\\Python312\\python.exe"
    )
    assert localappdata_block.index("Programs\\Python\\Python312\\python.exe") < localappdata_block.index(
        "Programs\\Python\\Python311\\python.exe"
    )


def test_powershell_install_and_check_wrappers_define_explicit_help_path() -> None:
    install_content = (REPO_ROOT / 'install.ps1').read_text(encoding='utf-8')
    check_content = (REPO_ROOT / 'check.ps1').read_text(encoding='utf-8')

    for content in (install_content, check_content):
        assert "[Alias('?')]" in content
        assert 'Show-WrapperUsage' in content
        assert 'if ($Help)' in content


def test_check_wrapper_only_rewrites_launcher_paths_on_windows_hosts() -> None:
    check_content = (REPO_ROOT / 'check.ps1').read_text(encoding='utf-8')

    assert 'function Resolve-LocalPathForCheck' in check_content
    assert "[System.IO.Path]::DirectorySeparatorChar -ne '\\'" in check_content
