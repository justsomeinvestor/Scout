Param(
  [string]$DateStr,
  [switch]$DryRun
)

function Ensure-Dir($path) {
  if (-not (Test-Path -LiteralPath $path)) {
    New-Item -ItemType Directory -Path $path -Force | Out-Null
  }
}

try {
  $now = if ($DateStr) { [DateTime]::Parse($DateStr) } else { Get-Date }
  $ym = $now.ToString('yyyy-MM')
  $d = $now.ToString('yyyy-MM-dd')
  $t = $now.ToString('HHmm')

  $mpSrc = Join-Path $PSScriptRoot '..\master-plan\master-plan.md' | Resolve-Path -ErrorAction Stop
  $journalSrc = Join-Path $PSScriptRoot '..\Journal\Journal.md' | Resolve-Path -ErrorAction Stop

  $mpDestDir = Join-Path $PSScriptRoot "..\master-plan\archive\$ym"
  $journalDestDir = Join-Path $PSScriptRoot "..\Journal\archive\$ym"
  Ensure-Dir $mpDestDir
  Ensure-Dir $journalDestDir

  $mpBase = "$d`_master-plan.md"
  $journalBase = "$d`_Journal.md"
  $mpDest = Join-Path $mpDestDir $mpBase
  $journalDest = Join-Path $journalDestDir $journalBase

  if (Test-Path -LiteralPath $mpDest) { $mpDest = Join-Path $mpDestDir ("{0}_" -f $d) + $t + '_master-plan.md' }
  if (Test-Path -LiteralPath $journalDest) { $journalDest = Join-Path $journalDestDir ("{0}_" -f $d) + $t + '_Journal.md' }

  if ($DryRun) {
    Write-Host "[DRYRUN] Would archive:`n  MP: $mpSrc -> $mpDest`n  Journal: $journalSrc -> $journalDest"
  } else {
    Copy-Item -LiteralPath $mpSrc -Destination $mpDest -Force
    Copy-Item -LiteralPath $journalSrc -Destination $journalDest -Force
    Write-Host "Archived MP -> $mpDest"
    Write-Host "Archived Journal -> $journalDest"

    $logPath = Join-Path $PSScriptRoot '..\Research\.processing_log.json'
    if (Test-Path -LiteralPath $logPath) {
      $raw = Get-Content -LiteralPath $logPath -Raw
      $obj = $null
      try { $obj = $raw | ConvertFrom-Json } catch { $obj = [ordered]@{} }
    } else {
      $obj = [ordered]@{}
    }

    if (-not $obj.archives) { $obj | Add-Member -Name archives -MemberType NoteProperty -Value (@{}) }
    $obj.archives.last_archived = (Get-Date).ToString('o')
    $obj.archives.files = @{ masterPlan = (Resolve-Path $mpDest).Path.Replace($pwd.Path + '\\',''); journal = (Resolve-Path $journalDest).Path.Replace($pwd.Path + '\\','') }

    ($obj | ConvertTo-Json -Depth 20) | Set-Content -LiteralPath $logPath -Encoding UTF8
    Write-Host "Processing log updated -> $logPath"
  }
}
catch {
  Write-Error $_
  exit 1
}

