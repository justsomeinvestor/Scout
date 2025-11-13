Param(
  [string]$Output = '..\data\history\mp-archive-summary.jsonl'
)

function Parse-FrontMatterJson($path) {
  $lines = Get-Content -LiteralPath $path
  if ($lines.Count -lt 3 -or $lines[0] -ne '---') { return $null }
  $endIdx = ($lines | Select-String -Pattern '^---$' | Select-Object -Skip 1 -First 1).LineNumber
  if (-not $endIdx) { return $null }
  $json = ($lines[1..($endIdx-2)] -join "`n")
  try { return $json | ConvertFrom-Json } catch { return $null }
}

try {
  $root = Join-Path $PSScriptRoot '..\master-plan\archive'
  $files = Get-ChildItem -LiteralPath $root -Recurse -Filter '*_master-plan.md' | Sort-Object FullName
  if ($files.Count -eq 0) { Write-Host 'No archives found.'; exit 0 }

  $outPath = Join-Path $PSScriptRoot $Output
  $outDir = Split-Path -Parent $outPath
  if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
  if (Test-Path -LiteralPath $outPath) { Remove-Item -LiteralPath $outPath -Force }

  foreach ($f in $files) {
    $fm = Parse-FrontMatterJson $f.FullName
    if (-not $fm) { continue }
    $row = [ordered]@{}
    $row.date = [IO.Path]::GetFileNameWithoutExtension($f.Name).Split('_')[0]
    $row.file = $f.FullName.Replace($pwd.Path + '\\','')
    $row.pageTitle = $fm.dashboard.pageTitle
    $row.signalComposite = $fm.dashboard.dailyPlanner.signalData.composite
    $row.signalTier = $fm.dashboard.dailyPlanner.signalData.tier
    $row.xSentiment = $fm.dashboard.dailyPlanner.signalData.xSentiment
    $row.sentimentCards = $fm.dashboard.sentimentCards
    ($row | ConvertTo-Json -Compress) | Add-Content -LiteralPath $outPath -Encoding UTF8
  }
  Write-Host "Summary written -> $outPath"
}
catch {
  Write-Error $_
  exit 1
}

