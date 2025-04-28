

set OPENAI_API_KEY=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
set INTERPRETER_MODEL=gpt-4
# set HTTP_PROXY=http://proxy.mei.melco.co.jp:9515
# set HTTPS_PROXY=http://proxy.mei.melco.co.jp:9515

Set-Location -Path $PSScriptRoot
#Start-Process  ".\myenv\Scripts\Activate.ps1"

Start-Process powershell -ArgumentList '-NoExit', '-Command', '.\myenv\Scripts\Activate.ps1'
