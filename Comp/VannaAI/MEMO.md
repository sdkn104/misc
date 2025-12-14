# Vanna AI

## install Open source version

- https://vanna.ai/docs/configure

1. do the following
```
pip install 'vanna[openai,oracle]'
$env:TNS_ADMIN="path/to/admin"
python start.py
```
2. Open localhost:8000 in browser

3. chat で以下を指示できる
　　　Oracle DBのテーブル名を教えてください
　　　テーブルTESTのスキーマを教えて
　　　使用可能なツールを教えて
