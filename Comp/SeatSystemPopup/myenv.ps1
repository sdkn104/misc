

set INTERPRETER_MODEL=gpt-4


Set-Location -Path $PSScriptRoot
#Start-Process  ".\myenv\Scripts\Activate.ps1"

#& ./secret.ps1

Start-Process powershell -ArgumentList '-NoExit', '-Command', '.\myenv\Scripts\Activate.ps1'
