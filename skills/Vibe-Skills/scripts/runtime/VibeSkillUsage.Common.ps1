Set-StrictMode -Version Latest

function Resolve-VibeSkillUsageSkillPath {
    param(
        [Parameter(Mandatory)] [string]$RepoRoot,
        [Parameter(Mandatory)] [string]$SkillId,
        [AllowEmptyString()] [string]$TargetRoot = '',
        [AllowEmptyString()] [string]$HostId = ''
    )

    $candidates = @(
        (Join-Path $RepoRoot ("bundled\skills\{0}\SKILL.md" -f $SkillId)),
        (Join-Path $RepoRoot ("bundled\skills\{0}\SKILL.runtime-mirror.md" -f $SkillId))
    )
    if ([string]::Equals($SkillId, 'vibe', [System.StringComparison]::OrdinalIgnoreCase)) {
        $candidates += (Join-Path $RepoRoot 'SKILL.md')
    }
    if (Get-Command -Name Resolve-VgoInstalledSkillsRoot -ErrorAction SilentlyContinue) {
        $installedSkillsRoot = Resolve-VgoInstalledSkillsRoot -TargetRoot $TargetRoot -HostId $HostId
        $candidates += @(
            (Join-Path $installedSkillsRoot (Join-Path $SkillId 'SKILL.md')),
            (Join-Path $installedSkillsRoot (Join-Path $SkillId 'SKILL.runtime-mirror.md')),
            (Join-Path $installedSkillsRoot (Join-Path 'custom' (Join-Path $SkillId 'SKILL.md'))),
            (Join-Path $installedSkillsRoot (Join-Path 'custom' (Join-Path $SkillId 'SKILL.runtime-mirror.md')))
        )
    }

    foreach ($candidate in $candidates) {
        if (-not [string]::IsNullOrWhiteSpace([string]$candidate) -and (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            return [System.IO.Path]::GetFullPath($candidate)
        }
    }
    return $null
}

function New-VibeSkillUsageLoadedSkill {
    param(
        [Parameter(Mandatory)] [string]$RepoRoot,
        [Parameter(Mandatory)] [string]$SkillId,
        [Parameter(Mandatory)] [string]$LoadedAtStage,
        [AllowEmptyString()] [string]$TargetRoot = '',
        [AllowEmptyString()] [string]$HostId = ''
    )

    $skillPath = Resolve-VibeSkillUsageSkillPath -RepoRoot $RepoRoot -SkillId $SkillId -TargetRoot $TargetRoot -HostId $HostId
    if ([string]::IsNullOrWhiteSpace([string]$skillPath)) {
        return [pscustomobject]@{
            skill_id = $SkillId
            skill_md_path = $null
            skill_md_sha256 = $null
            load_status = 'missing_skill_md'
            loaded_at_stage = $LoadedAtStage
            loaded_byte_count = 0
            loaded_line_count = 0
            unused_reason = 'not_loaded_full_skill_md'
        }
    }

    $content = Get-Content -LiteralPath $skillPath -Raw -Encoding UTF8
    $hash = (Get-FileHash -LiteralPath $skillPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $lines = if ([string]::IsNullOrEmpty($content)) { @() } else { @($content -split "`r?`n") }
    if (@($lines).Count -gt 0 -and [string]$lines[-1] -eq '') {
        $lines = @($lines | Select-Object -First (@($lines).Count - 1))
    }
    $lineCount = @($lines).Count
    $byteCount = [System.Text.Encoding]::UTF8.GetByteCount($content)
    return [pscustomobject]@{
        skill_id = $SkillId
        skill_md_path = [System.IO.Path]::GetFullPath($skillPath)
        skill_md_sha256 = $hash
        load_status = 'loaded_full_skill_md'
        loaded_at_stage = $LoadedAtStage
        loaded_byte_count = [int]$byteCount
        loaded_line_count = [int]$lineCount
    }
}

function New-VibeInitialSkillUsage {
    param(
        [AllowNull()] [object[]]$LoadedSkills = @(),
        [AllowNull()] [object[]]$TouchedSkills = @()
    )

    $loaded = @($LoadedSkills | Where-Object { $null -ne $_ })
    $loadedIds = @($loaded | ForEach-Object { [string]$_.skill_id } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
    $unusedRows = New-Object System.Collections.Generic.List[object]
    $seen = @{}
    foreach ($touch in @($TouchedSkills)) {
        if ($null -eq $touch) {
            continue
        }
        $skillId = if ($touch.PSObject.Properties.Name -contains 'skill_id') { [string]$touch.skill_id } else { '' }
        if ([string]::IsNullOrWhiteSpace($skillId) -or $seen.ContainsKey($skillId)) {
            continue
        }
        $reason = if ($touch.PSObject.Properties.Name -contains 'reason' -and -not [string]::IsNullOrWhiteSpace([string]$touch.reason)) {
            [string]$touch.reason
        } elseif ($loadedIds -contains $skillId) {
            'selected_but_no_artifact_impact'
        } else {
            'candidate_only'
        }
        $unusedRows.Add([pscustomobject]@{ skill_id = $skillId; reason = $reason }) | Out-Null
        $seen[$skillId] = $true
    }

    foreach ($loadedSkill in $loaded) {
        $skillId = [string]$loadedSkill.skill_id
        if (-not [string]::IsNullOrWhiteSpace($skillId) -and -not $seen.ContainsKey($skillId)) {
            $unusedRows.Add([pscustomobject]@{ skill_id = $skillId; reason = 'selected_but_no_artifact_impact' }) | Out-Null
            $seen[$skillId] = $true
        }
    }

    return [pscustomobject]@{
        schema_version = 2
        state_model = 'binary_used_unused'
        used = @()
        unused = [object[]]$unusedRows.ToArray()
        used_skills = @()
        unused_skills = [object[]]@($unusedRows.ToArray() | ForEach-Object { [string]$_.skill_id })
        loaded_skills = [object[]]@($loaded)
        evidence = @()
        unused_reasons = [object[]]$unusedRows.ToArray()
    }
}

function Select-VibeSkillUsageRowsExceptSkill {
    param(
        [AllowNull()] [object]$Rows = $null,
        [Parameter(Mandatory)] [string]$SkillId
    )

    $selectedRows = @()
    foreach ($row in @($Rows)) {
        if ($null -eq $row) {
            continue
        }
        $rowSkillId = if ($row.PSObject.Properties.Name -contains 'skill_id') { [string]$row.skill_id } else { '' }
        if ([string]::IsNullOrWhiteSpace($rowSkillId)) {
            continue
        }
        if (-not [string]::Equals($rowSkillId, $SkillId, [System.StringComparison]::OrdinalIgnoreCase)) {
            $selectedRows += $row
        }
    }

    return [object[]]@($selectedRows)
}

function Update-VibeSkillUsageArtifactImpact {
    param(
        [Parameter(Mandatory)] [object]$SkillUsage,
        [Parameter(Mandatory)] [string]$SkillId,
        [Parameter(Mandatory)] [string]$Stage,
        [Parameter(Mandatory)] [string]$ArtifactRef,
        [Parameter(Mandatory)] [string]$ImpactSummary
    )

    $loaded = @($SkillUsage.loaded_skills)
    $loadedRecord = @($loaded | Where-Object { [string]$_.skill_id -eq $SkillId } | Select-Object -First 1)
    $usedRows = if ($SkillUsage.PSObject.Properties.Name -contains 'used' -and $null -ne $SkillUsage.used) {
        @(Select-VibeSkillUsageRowsExceptSkill -Rows $SkillUsage.used -SkillId $SkillId)
    } else {
        @()
    }
    $unusedRows = if ($SkillUsage.PSObject.Properties.Name -contains 'unused' -and $null -ne $SkillUsage.unused) {
        @(Select-VibeSkillUsageRowsExceptSkill -Rows $SkillUsage.unused -SkillId $SkillId)
    } elseif ($SkillUsage.PSObject.Properties.Name -contains 'unused_reasons' -and $null -ne $SkillUsage.unused_reasons) {
        @(Select-VibeSkillUsageRowsExceptSkill -Rows $SkillUsage.unused_reasons -SkillId $SkillId)
    } else {
        @()
    }
    $evidence = @($SkillUsage.evidence)
    $impactRecord = [pscustomobject]@{
        stage = $Stage
        artifact_path = $ArtifactRef
        impact = $ImpactSummary
    }
    $legacyEvidenceRecord = [pscustomobject]@{
        skill_id = $SkillId
        stage = $Stage
        artifact_ref = $ArtifactRef
        impact_summary = $ImpactSummary
        skill_md_path = if (@($loadedRecord).Count -gt 0) { [string]$loadedRecord[0].skill_md_path } else { $null }
        skill_md_sha256 = if (@($loadedRecord).Count -gt 0) { [string]$loadedRecord[0].skill_md_sha256 } else { $null }
    }
    $evidence += $legacyEvidenceRecord
    $usedRows += [pscustomobject]@{
        skill_id = $SkillId
        skill_md_path = if (@($loadedRecord).Count -gt 0) { [string]$loadedRecord[0].skill_md_path } else { $null }
        skill_md_sha256 = if (@($loadedRecord).Count -gt 0) { [string]$loadedRecord[0].skill_md_sha256 } else { $null }
        evidence = @($impactRecord)
    }

    return [pscustomobject]@{
        schema_version = 2
        state_model = 'binary_used_unused'
        used = [object[]]$usedRows
        unused = [object[]]$unusedRows
        used_skills = [object[]]@($usedRows | ForEach-Object { [string]$_.skill_id } | Select-Object -Unique)
        unused_skills = [object[]]@($unusedRows | ForEach-Object { [string]$_.skill_id } | Select-Object -Unique)
        loaded_skills = [object[]]$loaded
        evidence = [object[]]$evidence
        unused_reasons = [object[]]$unusedRows
    }
}

function Get-VibeSkillUsagePath {
    param(
        [Parameter(Mandatory)] [string]$SessionRoot
    )
    return [System.IO.Path]::GetFullPath((Join-Path $SessionRoot 'skill-usage.json'))
}

function Read-VibeSkillUsageArtifact {
    param(
        [Parameter(Mandatory)] [string]$SessionRoot,
        [AllowNull()] [object]$Fallback = $null
    )
    $path = Get-VibeSkillUsagePath -SessionRoot $SessionRoot
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        return Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
    }
    return $Fallback
}
