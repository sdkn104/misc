# Registry configuration for Edge extension internal distribution
# This script must be run as Administrator

$extensionId = 'Sample-Extension-ID-Placeholder'
$updateUrl = 'https://localhost:8443/update.xml'

# Registry path for Edge extensions
$regPath = 'HKLM:\SOFTWARE\Microsoft\Edge\Extensions'

Write-Host 'Configuring Windows Registry for Edge extension...' -ForegroundColor Cyan

# Create extension registry entry
if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
    Write-Host "Created registry path: $regPath"
}

$extPath = Join-Path $regPath $extensionId
if (-not (Test-Path $extPath)) {
    New-Item -Path $extPath -Force | Out-Null
}

# Set registry values
New-ItemProperty -Path $extPath -Name 'update_url' -Value $updateUrl -PropertyType String -Force | Out-Null
Write-Host "Set update URL: $updateUrl"

Write-Host 'Registry configuration completed successfully' -ForegroundColor Green
Write-Host "Extension ID: $extensionId"
Write-Host "Update URL: $updateUrl"
