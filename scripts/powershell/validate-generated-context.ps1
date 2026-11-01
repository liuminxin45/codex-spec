param([string]$RepoRoot = ".", [switch]$Json)
& "$PSScriptRoot/invoke-check.ps1" -RepoRoot $RepoRoot -Kind generated-context -Json:$Json
exit $LASTEXITCODE
