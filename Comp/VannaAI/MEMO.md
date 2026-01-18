# Vanna AI

## install Open source version

- https://vanna.ai/docs/configure

1. prepare DB (SQLite)
    - install sqlite3.exe
    - python preapre_sqlie.py (create db and copy csv to db)

1. install vanna and start
```powershell
pip install 'vanna[openai]'
#pip install 'vanna[openai,oracle]'
#$env:TNS_ADMIN="path/to/admin"

$env:AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4.1-azure"
$env:AZURE_OPENAI_ENDPOINT = "https://test-openai-999.openai.azure.com/"
$env:AZURE_OPENAI_API_KEY = ""
$env:OPENAI_API_VERSION = "2024-10-21"

python start.py
```
2. Open localhost:8000 in browser

3. chat で以下を指示できる
    使用可能なツールの一覧を教えて
    DBのテーブル名を教えてください
    テーブルTESTのスキーマを教えて
    study_hours列のヒストグラムを表示して
