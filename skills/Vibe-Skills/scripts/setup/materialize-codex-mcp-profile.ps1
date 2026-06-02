param(
    [string]$TargetRoot = '',
    [string]$Profile,
    [string]$OutputPath,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot '..\common\vibe-governance-helpers.ps1')
if ([string]::IsNullOrWhiteSpace($TargetRoot)) {
    $TargetRoot = Resolve-VgoTargetRoot
}

function Get-SettingsProfile {
    param(
        [Parameter(Mandatory)] [string]$SettingsPath
    )

    if (-not (Test-Path -LiteralPath $SettingsPath)) {
        return $null
    }

    try {
        $settings = Get-Content -LiteralPath $SettingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
        throw ("Failed to parse settings.json: " + $_.Exception.Message)
    }

    if ($settings.PSObject.Properties.Name -contains 'vco' -and $null -ne $settings.vco) {
        if ($settings.vco.PSObject.Properties.Name -contains 'mcp_profile') {
            return [string]$settings.vco.mcp_profile
        }
    }

    return $null
}

$repoRoot = Resolve-VgoRepoRoot -StartPath $PSCommandPath
$settingsPath = Join-Path $TargetRoot 'settings.json'
$resolvedProfile = if (-not [string]::IsNullOrWhiteSpace($Profile)) {
    $Profile
} else {
    Get-SettingsProfile -SettingsPath $settingsPath
}
if ([string]::IsNullOrWhiteSpace($resolvedProfile)) {
    $resolvedProfile = 'full'
}

$serversTemplatePath = Join-Path $repoRoot 'mcp\servers.template.json'
$profilePath = Join-Path $repoRoot ("mcp\profiles\{0}.json" -f $resolvedProfile)
if (-not (Test-Path -LiteralPath $serversTemplatePath)) {
    throw "MCP servers template not found: $serversTemplatePath"
}
if (-not (Test-Path -LiteralPath $profilePath)) {
    throw "MCP profile not found: $profilePath"
}

$template = Get-Content -LiteralPath $serversTemplatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$profileObj = Get-Content -LiteralPath $profilePath -Raw -Encoding UTF8 | ConvertFrom-Json
$enabledServers = @($profileObj.enabled_servers | ForEach-Object { [string]$_ })

$activeServers = [ordered]@{}
$missingServers = New-Object System.Collections.Generic.List[string]
foreach ($serverName in $enabledServers) {
    if ($template.servers.PSObject.Properties.Name -notcontains $serverName) {
        $missingServers.Add($serverName) | Out-Null
        continue
    }

    $server = $template.servers.$serverName
    $entry = [ordered]@{}
    foreach ($prop in $server.PSObject.Properties) {
        $entry[$prop.Name] = $prop.Value
    }
    $activeServers[$serverName] = [pscustomobject]$entry
}

if ($missingServers.Count -gt 0) {
    throw ("MCP profile references unknown servers: " + (($missingServers | Select-Object -Unique) -join ', '))
}

$resolvedOutputPath = if (-not [string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath
} else {
    Join-Path $TargetRoot 'mcp\servers.active.json'
}

if ((Test-Path -LiteralPath $resolvedOutputPath) -and -not $Force) {
    throw "Output already exists. Use -Force to overwrite: $resolvedOutputPath"
}

$artifact = [ordered]@{
    generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    target_root = [System.IO.Path]::GetFullPath($TargetRoot)
    profile = $resolvedProfile
    source_template = (Get-VgoRelativePathPortable -BasePath $repoRoot -TargetPath $serversTemplatePath)
    source_profile = (Get-VgoRelativePathPortable -BasePath $repoRoot -TargetPath $profilePath)
    enabled_servers = @($enabledServers)
    servers = [pscustomobject]$activeServers
}

Write-VgoUtf8NoBomText -Path $resolvedOutputPath -Content (($artifact | ConvertTo-Json -Depth 20) + "`r`n")

[pscustomobject]@{
    result = 'PASS'
    target_root = [System.IO.Path]::GetFullPath($TargetRoot)
    output_path = [System.IO.Path]::GetFullPath($resolvedOutputPath)
    profile = $resolvedProfile
    enabled_server_count = $enabledServers.Count
} | ConvertTo-Json -Depth 10
