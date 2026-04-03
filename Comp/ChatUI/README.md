# Open WebUI
- https://github.com/open-webui/open-webui
- https://docs.openwebui.com/

### install
* python 3.11 is recommended
  ```python
  pip install open-webui
  # at install first time, not set offline, for downloading modules
  open-webui serve --port 3000
  # --> http://localhost:3000
  ```
* admin user: 会社メール、情シスパスワード(2026.3)

* User manegement
- to turn off user management (single user, no admin) :  `$env:WEBUI_AUTH="False"`

* setting offline
  - https://docs.openwebui.com/tutorials/maintenance/offline-mode
  - answer from chatGPT
    ```powershell
    # from official page
    $env:OFFLINE_MODE = "true"
    $env:HF_HUB_OFFLINE="1"
    $env:RAG_EMBEDDING_MODEL_AUTO_UPDATE="false"
    $env:RAG_RERANKING_MODEL_AUTO_UPDATE="false"
    $env:WHISPER_MODEL_AUTO_UPDATE="false"
    # from ChatGPT
    $env:ENABLE_WEB_SEARCH="false"
    $env:USER_PERMISSIONS_FEATURES_WEB_SEARCH="false"
    $env:ENABLE_SEARCH_QUERY_GENERATION="false"
    $env:WEB_SEARCH_TRUST_ENV="false"
    $env:SAFE_MODE="true"
    ```
* Setting No-Embedding in attaching document in prompt
   - Admin Settings → Documents → General →「Bypass Embedding and Retrieval」をON
   - or `$env:BYPASS_EMBEDDING_AND_RETRIEVAL="true"`

* Audit log
  ```powershell
  $env:ENABLE_AUDIT_LOGS_FILE="true"
  $env:AUDIT_LOG_LEVEL="METADATA"
  $env:AUDIT_LOGS_FILE_PATH="logs/audit.log"
  mkdir logs
  ```
* Custom Banner
  ```
  $env:WEBUI_BANNERS='[{"id":"notice1","type":"info","title":"Welcome","content":"社内AIチャットへようこそ","dismissible":true,"timestamp":1000}]'
  ```

* Remove Arena model 
  - 管理パネル→設定→評価→Arena Modelのチェックを外す

### setting LLM
https://docs.openwebui.com/getting-started/quick-start/connect-a-provider/starting-with-openai-compatible
- OpenAI LLM connected.
- compatible_server.py connected.
- Azure OpenAI connected. (gpt-5-mini chat/completion OK, gpt-5.2 NG)
    - 右上のアカウントマーク⇒管理者パネル⇒ 設定 → Connections → OpenAI.
    - Click ➕ Add Connection.
    - URL: https://xxxx.openai.azure.com
    - Bearer: API key
    - Provider type: Azure OpenAI
    - API version: version
    - API type: Chat Completions
    - model ID:  deployment name (gpt-5-mini, etc.) -> click + mark

- Azure OpenAI GPT-5 chat/completion
    - install pipeline function: https://openwebui.com/posts/azure_ai_cc10d97f
      - download json by push Get button in above URL
      - 管理パネル⇒Functions⇒import
    - setting function
      - in functions pannel, push 歯車
      - input API key, URL, deployment name

### invoke URL
- specify MODEL: http://localhost:3000/?model=gpt-4.1
