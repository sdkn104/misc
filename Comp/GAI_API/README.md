
# OpenAI API
- API spec: https://platform.openai.com/docs/api-reference/introduction
  - chat completion: https://platform.openai.com/docs/api-reference/chat/create
- openapi.yaml for OpenAI API is available, not official
- https://spec.openapis.org/oas/v3.1.0
- text/event-stream: https://developer.mozilla.org/ja/docs/Web/API/Server-sent_events/Using_server-sent_events
- research protocol by checking HTTP using Fiddler Classic

# OpenAPI Generator (failed)
### Install
* https://github.com/OpenAPITools/openapi-generator-cli
* https://openapi-generator.tech/docs/installation
```bash
curl https://raw.githubusercontent.com/openai/openai-openapi/refs/heads/manual_spec/openapi.yaml -OutFile openapi.yaml
# https://github.com/openai/openai-openapi/tree/manual_spec
#npm install @openapitools/openapi-generator-cli -g
pip install openapi-generator-cli
openapi-generator-cli generate -i openapi.yaml -g python-fastapi -o ./generated-fastapi
```
* install JDK 11 or later
  * installer: https://jdk.java.net/24/
  * `$Env:Path += ";C:\xxx\java\bin"`

* python-fastapi work only on linux (uvloop dont support windows)
* 動かなかった


# OpenAI-comaptible API Server

### How created
1. openapi.yamlから使わないendpointを削除
2. delcomp.pyを使って呼ばれないcomponentを削除
3. openAPI Generatorで生成したhtmlを生成
4. web serviceでhtmlをmdに変換
5. mdを使ってcompatible_server.pyを生成

* SSE: https://developer.mozilla.org/ja/docs/Web/API/Server-sent_events/Using_server-sent_events

### Flask production server
- https://flask.palletsprojects.com/en/stable/deploying/
-  waitress
    - https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html
    - https://jp-seemore.com/iot/python/29417/
    ```python
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
    ```

### Run in background
```
pythonw compatible_server.py
```

### Network setting
* Listen 0.0.0.0 instead of localhost, since cannnot access to localhost(127.0.0.1) of host from docker
  * docker (Dify) access to IP-address-of-host or hostname
    * `http://IPaddress_of_host_or_hostname:5000/`
* Firewall Setting (Windows Defender Firewall)
    ```powershell
    # set firewall
    netsh advfirewall firewall add rule name="★FlaskApp TCP 5000" dir=in action=allow protocol=TCP localport=5000 profile=private,domain
    # show firewall
    netsh advfirewall firewall show rule name="★FlaskApp TCP 5000"
    # delete firewall
    netsh advfirewall firewall delete rule name="★FlaskApp TCP 5000"
    ```

# Open WebUI
- https://github.com/open-webui/open-webui
- https://docs.openwebui.com/

### install
* python 3.11 is recommended
  ```
  pip install open-webui
  open-webui serve
  # --> http://localhost:8080
  ```
* admin user: sadakane, ka〇〇〇〇〇〇3

### setting LLM
https://docs.openwebui.com/getting-started/quick-start/starting-with-openai-compatible
- OpenAI LLM connected.
- compatible_server.py connected.
- Azure OpenAI cannot be connected.
