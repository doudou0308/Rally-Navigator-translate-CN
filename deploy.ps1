<#
.SYNOPSIS
    Rally Navigator 中文汉化 - 一键部署脚本
.DESCRIPTION
    此脚本将生成的中文翻译文件部署到 Rally Navigator 的立陶宛语目录中。
    使用前请修改 $RallyPath 为实际安装路径。
#>

# ========== 请根据实际情况修改 ==========
$RallyPath = "C:\Program Files\Rally Navigator"
# =====================================

$ZhPath = Join-Path $PSScriptRoot "resources\locales\zh-Hans-CN\translation.json"
$LtPath = Join-Path $RallyPath "resources\locales\lt\translation.json"
$BakPath = Join-Path $RallyPath "resources\locales\lt\translation.json.lt.bak"

# 检查文件存在
if (-not (Test-Path $RallyPath)) {
    Write-Host "[错误] 找不到 Rally Navigator 安装目录: $RallyPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $ZhPath)) {
    Write-Host "[错误] 找不到中文翻译文件。请先运行 python translate.py 生成翻译。" -ForegroundColor Red
    exit 1
}

# 检查是否正在运行
$procs = Get-Process -Name "Rally Navigator" -ErrorAction SilentlyContinue
if ($procs) {
    Write-Host "[警告] Rally Navigator 正在运行，建议先关闭。" -ForegroundColor Yellow
    $choice = Read-Host "是否继续? (y/N)"
    if ($choice -ne "y") { exit }
}

# 备份立陶宛语原文
if (Test-Path $LtPath) {
    if (-not (Test-Path $BakPath)) {
        Copy-Item $LtPath $BakPath -Force
        Write-Host "[备份] 立陶宛语原文 → translation.json.lt.bak" -ForegroundColor Green
    } else {
        Write-Host "[跳过] 备份已存在: translation.json.lt.bak" -ForegroundColor Yellow
    }
}

# 部署中文翻译
Copy-Item $ZhPath $LtPath -Force
Write-Host "[部署] 中文翻译已部署到: $LtPath" -ForegroundColor Green
Write-Host ""
Write-Host "现在启动 Rally Navigator，在 System and Menu Language 中选择:" -ForegroundColor Cyan
Write-Host "  Lietuviškai（立陶宛语）" -ForegroundColor White -BackgroundColor DarkGreen
Write-Host ""
Write-Host "还原方法: 删除 translation.json，将 .bak 重命名回去" -ForegroundColor Gray
