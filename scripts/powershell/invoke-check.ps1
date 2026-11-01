param([string]$RepoRoot = ".", [Parameter(Mandatory)][string]$Kind, [switch]$Json)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath $RepoRoot).Path
$python = if ($env:CODEX_SPEC_PYTHON) { $env:CODEX_SPEC_PYTHON }
          elseif (Test-Path -LiteralPath (Join-Path $root '.venv/Scripts/python.exe')) { Join-Path $root '.venv/Scripts/python.exe' }
          elseif (Test-Path -LiteralPath (Join-Path $root '.venv/bin/python')) { Join-Path $root '.venv/bin/python' }
          else { (Get-Command python -ErrorAction Stop).Source }
$previous = $env:PYTHONPATH
try {
    $env:PYTHONPATH = Join-Path $root 'src'
    $arguments = @('-m', 'codex_spec', 'check', '--kind', $Kind, '--project-dir', $root, '--repo-root', $root)
    if ($Json) { $arguments += '--json' }
    & $python @arguments
    $code = $LASTEXITCODE
} finally { $env:PYTHONPATH = $previous }
exit $code
