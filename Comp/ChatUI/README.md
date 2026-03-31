# Open WebUI
- https://github.com/open-webui/open-webui
- https://docs.openwebui.com/

### install
* python 3.11 is recommended
  ```
  pip install open-webui
  # at install first time, not set offline, for downloading modules
  open-webui serve --port 3000
  # --> http://localhost:3000
  ```
* admin user: 会社メール、情シスパスワード(2026.3)

* setting offline
  - https://docs.openwebui.com/tutorials/maintenance/offline-mode
  - answer from chatGPT
    ```
    # from official 
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
