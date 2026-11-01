[CmdletBinding()]
param([string]$RepoRoot = ".", [string]$Remote = 'origin', [switch]$ConfirmHumanPush, [switch]$Json)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $RepoRoot).Path
$problems = @()
if (-not $ConfirmHumanPush) { $problems += 'This publication requires the human push request.' }
$branch = & git -C $root branch --show-current
if ($LASTEXITCODE -ne 0 -or -not $branch) { $problems += 'No current Git branch.' }
$url = & git -C $root remote get-url $Remote
if ($LASTEXITCODE -ne 0) { $problems += 'Remote is unavailable.' }
$result = [ordered]@{
    status = if ($problems.Count) {'error'} else {'ok'}
    branch = $branch
    remote = $Remote
    remote_url = $url
    human_request_confirmed = [bool]$ConfirmHumanPush
    problems = $problems
    note = 'Read-only release preflight. No branch, dirty-tree, active-Spec or concurrency policy.'
}
if ($Json) { $result | ConvertTo-Json -Depth 5 } else { $result }
if ($problems.Count) { exit 1 }
exit 0
