# Open interpreter
https://docs.openinterpreter.com/getting-started/introduction

### Install
- install Visual Studio C++ Build tools
  - https://qiita.com/mk-tool/items/0a602ce3d5eae428c308
https://www.rust-lang.org/ja/tools/install
  - 最新版でよさそう　C++をチェック
- install rust
- Use Python 3.10 or 3.11 (公式ドキュメントにあり)
- pip install open-interpreter


### Usage
- show profile YAML file
    ```
    interpreter --profiles
    ```
- start interactive mode
    ```powershell
    interpreter
    ```
- Setting language model
  - setting language model section in profile YAML file
  - For custom openAI-compatible model,
    - https://docs.openinterpreter.com/language-models/local-models/custom-endpoint
    ```yaml
    llm:
        # The URL where an OpenAI-compatible server is running to handle LLM API requests
        api_base: "http://desktop-dlmkcpa:5000/v1"  
    ```