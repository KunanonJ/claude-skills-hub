function New-VibeRetiredSpecialistConsultationLifecycleLayerProjection {
    param(
        [AllowNull()] [object]$ConsultationReceipt
    )

    if ($null -eq $ConsultationReceipt -or -not [bool]$ConsultationReceipt.enabled) {
        return $null
    }

    $windowId = if ((Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'window_id') -and -not [string]::IsNullOrWhiteSpace([string]$ConsultationReceipt.window_id)) {
        [string]$ConsultationReceipt.window_id
    } else {
        $null
    }
    if ($windowId -notin @('discussion', 'planning')) {
        throw 'Enabled specialist consultation receipts must declare window_id as discussion or planning.'
    }
    $consultedUnits = if (
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'consulted_units') -and
        $null -ne $ConsultationReceipt.consulted_units
    ) {
        @($ConsultationReceipt.consulted_units)
    } else {
        @()
    }
    $routedUnits = if (
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'routed_units') -and
        $null -ne $ConsultationReceipt.routed_units
    ) {
        @($ConsultationReceipt.routed_units)
    } else {
        @()
    }
    $consultedCount = if (
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'summary') -and
        $null -ne $ConsultationReceipt.summary -and
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt.summary -PropertyName 'consulted_unit_count')
    ) {
        [int]$ConsultationReceipt.summary.consulted_unit_count
    } else {
        @($consultedUnits).Count
    }
    $routedCount = if (
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'summary') -and
        $null -ne $ConsultationReceipt.summary -and
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt.summary -PropertyName 'routed_unit_count')
    ) {
        [int]$ConsultationReceipt.summary.routed_unit_count
    } else {
        @($routedUnits).Count
    }

    $skills = New-Object System.Collections.Generic.List[object]
    $renderedLines = @(if ($routedCount -gt 0 -and $consultedCount -eq 0) {
        ('Specialist consultation routing during {0}:' -f $windowId)
    } elseif ($consultedCount -gt 0 -and $routedCount -eq 0) {
        ('Specialist consultation during {0}:' -f $windowId)
    } else {
        ('Recorded specialist consultation chain during {0}:' -f $windowId)
    })
    foreach ($disclosure in @($ConsultationReceipt.user_disclosures)) {
        if ($null -eq $disclosure) {
            continue
        }

        $consultedUnit = $null
        foreach ($candidate in @($consultedUnits)) {
            if ($null -ne $candidate -and [string]$candidate.skill_id -eq [string]$disclosure.skill_id) {
                $consultedUnit = $candidate
                break
            }
        }
        $routedUnit = $null
        foreach ($candidate in @($routedUnits)) {
            if ($null -ne $candidate -and [string]$candidate.skill_id -eq [string]$disclosure.skill_id) {
                $routedUnit = $candidate
                break
            }
        }

        $skills.Add(
            [pscustomobject]@{
                skill_id = [string]$disclosure.skill_id
                why_now = if ((Test-VibeObjectHasProperty -InputObject $disclosure -PropertyName 'why_now') -and -not [string]::IsNullOrWhiteSpace([string]$disclosure.why_now)) { [string]$disclosure.why_now } else { $null }
                native_skill_entrypoint = if ((Test-VibeObjectHasProperty -InputObject $disclosure -PropertyName 'native_skill_entrypoint') -and -not [string]::IsNullOrWhiteSpace([string]$disclosure.native_skill_entrypoint)) { [string]$disclosure.native_skill_entrypoint } else { $null }
                native_skill_description = if ((Test-VibeObjectHasProperty -InputObject $disclosure -PropertyName 'native_skill_description') -and -not [string]::IsNullOrWhiteSpace([string]$disclosure.native_skill_description)) { [string]$disclosure.native_skill_description } else { $null }
                state = if ($consultedUnit -and (Test-VibeObjectHasProperty -InputObject $consultedUnit -PropertyName 'status')) {
                    [string]$consultedUnit.status
                } elseif ($routedUnit -and (Test-VibeObjectHasProperty -InputObject $routedUnit -PropertyName 'status')) {
                    [string]$routedUnit.status
                } else {
                    'consultation_disclosed'
                }
                summary = if ($consultedUnit -and (Test-VibeObjectHasProperty -InputObject $consultedUnit -PropertyName 'summary')) {
                    [string]$consultedUnit.summary
                } elseif ($routedUnit -and (Test-VibeObjectHasProperty -InputObject $routedUnit -PropertyName 'summary')) {
                    [string]$routedUnit.summary
                } else {
                    $null
                }
            }
        ) | Out-Null
        $renderedLines += ('- {0}: {1} ({2})' -f [string]$disclosure.skill_id, [string]$disclosure.why_now, (Get-VibeSpecialistEntrypointDisplayText -SkillRecord $disclosure))
    }

    if ($skills.Count -eq 0) {
        return $null
    }

    return [pscustomobject]@{
        layer_id = ('{0}_consultation' -f $windowId)
        truth_layer = 'consultation'
        stage = if ((Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'stage') -and -not [string]::IsNullOrWhiteSpace([string]$ConsultationReceipt.stage)) { [string]$ConsultationReceipt.stage } else { $windowId }
        skill_count = [int]$skills.Count
        skills = [object[]]$skills.ToArray()
        rendered_text = ($renderedLines -join "`n")
    }
}

function New-VibeRetiredHostUserBriefingSegmentProjection {
    param(
        [AllowNull()] [object]$LifecycleLayer = $null,
        [AllowNull()] [object]$ConsultationReceipt = $null
    )

    if ($null -eq $LifecycleLayer) {
        return $null
    }

    $segmentId = if ((Test-VibeObjectHasProperty -InputObject $LifecycleLayer -PropertyName 'layer_id') -and -not [string]::IsNullOrWhiteSpace([string]$LifecycleLayer.layer_id)) {
        [string]$LifecycleLayer.layer_id
    } else {
        return $null
    }

    if ($segmentId -notmatch '^(discussion|planning)_consultation$') {
        return $null
    }

    $windowId = [string]$Matches[1]
    $freezeGate = Get-VibePropertySafe -InputObject $ConsultationReceipt -PropertyName 'freeze_gate'
    if ($freezeGate) {
        $gateStatus = if ([bool]$freezeGate.passed) { 'passed' } else { 'failed' }
        $status = if ([bool]$freezeGate.passed) { 'gate_passed' } else { 'gate_failed' }
    } else {
        $gateStatus = 'not_applicable'
        $status = 'gate_unknown'
    }

    $consultedUnits = if (
        $ConsultationReceipt -and
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'consulted_units') -and
        $null -ne $ConsultationReceipt.consulted_units
    ) {
        @($ConsultationReceipt.consulted_units)
    } else {
        @()
    }
    $routedUnits = if (
        $ConsultationReceipt -and
        (Test-VibeObjectHasProperty -InputObject $ConsultationReceipt -PropertyName 'routed_units') -and
        $null -ne $ConsultationReceipt.routed_units
    ) {
        @($ConsultationReceipt.routed_units)
    } else {
        @()
    }
    $summary = Get-VibePropertySafe -InputObject $ConsultationReceipt -PropertyName 'summary'
    $consultedCount = Get-VibeNestedPropertySafe -InputObject $summary -PropertyPath @('consulted_unit_count') -DefaultValue @($consultedUnits).Count
    $routedCount = Get-VibeNestedPropertySafe -InputObject $summary -PropertyPath @('routed_unit_count') -DefaultValue @($routedUnits).Count

    $segmentLines = @()
    if ($routedCount -gt 0 -and $consultedCount -eq 0) {
        $segmentLines += ('Vibe routed these Skills for legacy consultation disclosure during {0}; freeze gate: {1}. Usage claims still require `skill_usage` evidence.' -f $windowId, $gateStatus)
    } elseif ($consultedCount -gt 0 -and $routedCount -eq 0) {
        $segmentLines += ('Vibe recorded these Skills in the {0} consultation audit chain; freeze gate: {1}. Usage claims still require `skill_usage` evidence.' -f $windowId, $gateStatus)
    } else {
        $segmentLines += ('Vibe recorded these Skills in the {0} consultation chain; freeze gate: {1}.' -f $windowId, $gateStatus)
    }

    foreach ($skill in @($LifecycleLayer.skills)) {
        if ($null -eq $skill) {
            continue
        }
        $skillId = if ((Test-VibeObjectHasProperty -InputObject $skill -PropertyName 'skill_id') -and -not [string]::IsNullOrWhiteSpace([string]$skill.skill_id)) {
            [string]$skill.skill_id
        } else {
            continue
        }
        $state = if ((Test-VibeObjectHasProperty -InputObject $skill -PropertyName 'state') -and -not [string]::IsNullOrWhiteSpace([string]$skill.state)) { [string]$skill.state } else { 'reported' }
        $entrypoint = Get-VibeSpecialistEntrypointDisplayText -SkillRecord $skill
        $whyNow = if ((Test-VibeObjectHasProperty -InputObject $skill -PropertyName 'why_now') -and -not [string]::IsNullOrWhiteSpace([string]$skill.why_now)) { [string]$skill.why_now } else { 'no additional rationale recorded' }
        $segmentLines += ('- {0} [{1}] from {2}' -f $skillId, $state, $entrypoint)
        $segmentLines += ('  Why: {0}' -f $whyNow)
        if ((Test-VibeObjectHasProperty -InputObject $skill -PropertyName 'summary') -and -not [string]::IsNullOrWhiteSpace([string]$skill.summary)) {
            $segmentLines += ('  Summary: {0}' -f [string]$skill.summary)
        }
    }

    return [pscustomobject]@{
        segment_id = $segmentId
        stage = if ((Test-VibeObjectHasProperty -InputObject $LifecycleLayer -PropertyName 'stage') -and -not [string]::IsNullOrWhiteSpace([string]$LifecycleLayer.stage)) { [string]$LifecycleLayer.stage } else { $null }
        category = 'consultation'
        truth_layer = if ((Test-VibeObjectHasProperty -InputObject $LifecycleLayer -PropertyName 'truth_layer') -and -not [string]::IsNullOrWhiteSpace([string]$LifecycleLayer.truth_layer)) { [string]$LifecycleLayer.truth_layer } else { 'consultation' }
        status = $status
        gate_status = $gateStatus
        skill_count = if ((Test-VibeObjectHasProperty -InputObject $LifecycleLayer -PropertyName 'skill_count')) { [int]$LifecycleLayer.skill_count } else { @($LifecycleLayer.skills).Count }
        skills = @($LifecycleLayer.skills)
        rendered_text = (@($segmentLines) -join "`n")
    }
}

function Get-VibeRetiredHostStageDisclosureEventId {
    param(
        [Parameter(Mandatory)] [string]$SegmentId,
        [AllowNull()] [object[]]$Skills = @()
    )

    if ($SegmentId -notin @('discussion_consultation', 'planning_consultation')) {
        return $null
    }

    $hasRoutedConsultation = $false
    $hasCompletedConsultation = $false
    foreach ($skill in @($Skills)) {
        if ($null -eq $skill -or -not (Test-VibeObjectHasProperty -InputObject $skill -PropertyName 'state')) {
            continue
        }
        $state = [string]$skill.state
        if ($state -match '(^|_)routed($|_)') {
            $hasRoutedConsultation = $true
        }
        if ($state -in @('completed', 'completed_with_notes', 'consulted')) {
            $hasCompletedConsultation = $true
        }
    }

    if ($SegmentId -eq 'discussion_consultation') {
        if ($hasCompletedConsultation) {
            return 'discussion_consultation_completed'
        }
        if ($hasRoutedConsultation) {
            return 'discussion_consultation_routed'
        }
        return 'discussion_consultation_reported'
    }

    if ($hasCompletedConsultation) {
        return 'planning_consultation_completed'
    }
    if ($hasRoutedConsultation) {
        return 'planning_consultation_routed'
    }
    return 'planning_consultation_reported'
}
