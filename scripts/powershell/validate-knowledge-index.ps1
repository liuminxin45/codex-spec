param([string]$RepoRoot = ".", [switch]$Json)
& "$PSScriptRoot/invoke-check.ps1" -RepoRoot $RepoRoot -Kind knowledge-index -Json:$Json
exit $LASTEXITCODE
