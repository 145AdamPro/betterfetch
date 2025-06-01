Write-Host "🚀 Starting BetterFetch Installer" -ForegroundColor Cyan

$asciiDir = "ascii"
$configFile = "bfetch_config.txt"

# List available logos
Write-Host "`n📁 Available ASCII logos:"
Get-ChildItem "$asciiDir\*.txt" | ForEach-Object {
    Write-Host (" - " + $_.Name)
}

# Ask for input
$logo = Read-Host "`n🎨 Enter the name of the logo file (e.g., windows.txt)"

# Validate and write to config
if (Test-Path "$asciiDir\$logo") {
    Set-Content -Path $configFile -Value $logo
    Write-Host "✅ Logo set to $logo" -ForegroundColor Green
} else {
    $default = "$($env:OS -replace '^Windows_NT$', 'windows').txt"
    Set-Content -Path $configFile -Value $default
    Write-Host "⚠️ Logo not found. Using default: $default" -ForegroundColor Yellow
}

# Install dependencies
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "📦 Installing Python dependencies..."
    python -m pip install -r requirements.txt
    Write-Host "✅ Python packages installed." -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Pytho
