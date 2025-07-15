

set INTERPRETER_MODEL=gpt-4.1


Set-Location -Path $PSScriptRoot
#Start-Process  ".\myenv\Scripts\Activate.ps1"

& ./secret.ps1

# RUSTC path
$env:PATH=$HOME + "\.cargo\bin;" + $env:PATH

Start-Process powershell -ArgumentList '-NoExit', '-Command', '.\myenv\Scripts\Activate.ps1; echo "Dump-Versions to_save"'

