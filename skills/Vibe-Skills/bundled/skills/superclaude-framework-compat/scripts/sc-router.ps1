[CmdletBinding()]
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$ArgsIn
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($null -eq $ArgsIn) {
  $ArgsIn = @()
}

function Resolve-MapPath {
  return [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\command-map.json"))
}

function Normalize-CommandToken {
  param([Parameter(Mandatory = $true)][string]$Token)

  $t = $Token.Trim()
  if ([string]::IsNullOrWhiteSpace($t)) {
    return ""
  }
  if ($t -eq "/sc") { return "/sc" }
  if ($t -eq "sc") { return "/sc" }
  if ($t.StartsWith("/sc:")) { return $t.ToLowerInvariant() }
  if ($t.StartsWith("sc:")) { return ("/" + $t.ToLowerInvariant()) }
  if ($t.StartsWith("sc-")) {
    $suffix = $t.Substring(3).ToLowerInvariant()
    return "/sc:" + $suffix
  }
  return "/sc:" + $t.ToLowerInvariant()
}

function Show-Help {
  @(
    "SuperClaude Codex Compatibility Router",
    "",
    "Usage:",
    "  sc-router.ps1 --list",
    "  sc-router.ps1 --show /sc:implement",
    "  sc-router.ps1 /sc:implement [free text]",
    "  sc-router.ps1 sc-implement [free text]",
    "",
    "Notes:",
    "  - This is a compatibility layer (not native Claude slash-command execution).",
    "  - It maps SuperClaude commands to Codex-native skills and /vibe flows."
  ) | ForEach-Object { Write-Host $_ }
}

$mapPath = Resolve-MapPath
if (-not (Test-Path -LiteralPath $mapPath)) {
  throw "command-map.json not found: $mapPath"
}

$map = Get-Content -LiteralPath $mapPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($null -eq $map) {
  throw "Unable to parse command-map.json"
}

$index = @{}
foreach ($item in @($map)) {
  $index[$item.slash_command.ToLowerInvariant()] = $item
  $index[$item.name.ToLowerInvariant()] = $item
}

if ($ArgsIn.Count -eq 0 -or $ArgsIn[0] -in @("--help", "-h", "help")) {
  Show-Help
  exit 0
}

if ($ArgsIn[0] -eq "--list") {
  @($map | Sort-Object slash_command | Select-Object slash_command, status, codex_flow) | Format-Table -AutoSize
  exit 0
}

if ($ArgsIn[0] -eq "--json") {
  $map | ConvertTo-Json -Depth 8
  exit 0
}

if ($ArgsIn[0] -eq "--show") {
  if ($ArgsIn.Count -lt 2) {
    throw "--show requires one command token, e.g. --show /sc:implement"
  }
  $cmdNorm = Normalize-CommandToken -Token $ArgsIn[1]
  if (-not $index.ContainsKey($cmdNorm.ToLowerInvariant())) {
    throw "Unknown SuperClaude command: $($ArgsIn[1])"
  }
  $item = $index[$cmdNorm.ToLowerInvariant()]
  $item | ConvertTo-Json -Depth 8
  exit 0
}

$token = $ArgsIn[0]
$cmd = Normalize-CommandToken -Token $token
if (-not $index.ContainsKey($cmd.ToLowerInvariant())) {
  Write-Host "Unknown command token: $token"
  Write-Host "Run with --list to see mapped commands."
  exit 1
}

$spec = $index[$cmd.ToLowerInvariant()]
$extraText = if ($ArgsIn.Count -gt 1) { ($ArgsIn[1..($ArgsIn.Count - 1)] -join " ").Trim() } else { "" }
$skills = @($spec.codex_skills) -join ", "

Write-Host ("SuperClaude command: " + $spec.slash_command)
Write-Host ("Compatibility status: " + $spec.status)
Write-Host ("Codex flow: " + $spec.codex_flow)
Write-Host ("Mapped skills: " + $skills)
Write-Host ("Notes: " + $spec.notes)
Write-Host ""
Write-Host "Recommended Codex prompt:"

if ($extraText) {
  Write-Host ("/vibe " + $extraText)
} else {
  Write-Host ("/vibe execute the goal of " + $spec.slash_command + " and prioritize mapped skills.")
}