param([string]$RepoRoot = ".", [switch]$Json)
& "$PSScriptRoot/invoke-check.ps1" -RepoRoot $RepoRoot -Kind context-budget -Json:$Json
exit $LASTEXITCODE
