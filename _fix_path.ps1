$ErrorActionPreference = "Stop"

# 讀取使用者 PATH
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$machinePath = [Environment]::GetEnvironmentVariable("PATH", "Machine")

Write-Host "=== 使用者 PATH 中 Python 相關條目 ==="
$userPath -split ";" | Where-Object { $_ -like "*python*" -or $_ -like "*Python*" }

Write-Host ""
Write-Host "=== 系統 PATH 中 Python 相關條目 ==="
$machinePath -split ";" | Where-Object { $_ -like "*python*" -or $_ -like "*Python*" }

Write-Host ""
Write-Host "=== 完整 PATH 順序 (Python 相關) ==="
$fullPath = [Environment]::GetEnvironmentVariable("PATH", "Process")
$entries = $fullPath -split ";"
for ($i = 0; $i -lt $entries.Count; $i++) {
    if ($entries[$i] -like "*python*" -or $entries[$i] -like "*Python*") {
        Write-Host "[$i] $($entries[$i])"
    }
}
