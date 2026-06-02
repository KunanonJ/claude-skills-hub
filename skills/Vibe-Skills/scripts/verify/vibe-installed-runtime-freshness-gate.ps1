param(
    [string]$TargetRoot = '',
    [switch]$WriteArtifacts,
    [switch]$WriteReceipt
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\common\vibe-governance-helpers.ps1')
if ([string]::IsNullOrWhiteSpace($TargetRoot)) {
    $TargetRoot = Resolve-VgoTargetRoot
}

$runnerPath = Join-Path $PSScriptRoot 'runtime_neutral\freshness_gate.py'
if (-not (Test-Path -LiteralPath $runnerPath)) {
    throw "runtime-neutral freshness gate missing: $runnerPath"
}

$pythonInvocation = Get-VgoPythonCommand

$args = @(
    $runnerPath,
    '--target-root', $TargetRoot
)
if ($WriteArtifacts) {
    $args += '--write-artifacts'
}
if ($WriteReceipt) {
    $args += '--write-receipt'
}

& $pythonInvocation.host_path @($pythonInvocation.prefix_arguments) @args
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "vibe-installed-runtime-freshness-gate failed with exit code $exitCode"
}

Write-Host '[PASS] vibe-installed-runtime-freshness-gate passed' -ForegroundColor Green
