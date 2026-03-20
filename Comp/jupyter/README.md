# Jupyter AI
- Jupyter: https://docs.jupyter.org/en/latest/
- Jupyter AI: https://jupyter-ai.readthedocs.io/en/latest/index.html#

### Setup
https://github.com/jupyterlab/jupyterlab

* use python 3.13 (due to jupyter ai, 2026.3)
    ```powershell
    # install
    #pip cache purge
    pip install jupyterlab
    #pip install "jupyter-ai[all]"
    pip install "jupyter-ai[azure-chat-openai]"
    pip install langchain-openai==0.3.35
    #pip install langchain-ollama
    pip freeze > requirements.txt

    # launch
    jupyter lab
    ```
### Setting LLM
- https://jupyter-ai.readthedocs.io/en/latest/users/index.html#model-providers
- To use Model, install its Python packages (ex. "jupyter-ai[azure-chat-openai]") and 
    1. set its API key in your environment
        * Set environment variable:
        ```
        $env:OPENAI_KEY = "openAI API key"  
        ```

    2. set it in the chat interface setting GUI
        1. open chat interface by clicking Chat icon in left bar,
        2. open setting panel
        3. set model, key, other parameters 
            - Azure OpenAI::*
            - gpt-4.1-sada
            - https://test-openai-999.openai.azure.com/openai/deployments/gpt-4.1-azure/chat/completions?api-version=2025-01-01-preview
            - 2024-10-21
            - API key
        4. save
        * Alternatively, setting in config file:
            * C:\Users\QP48568\AppData\Roaming\jupyter\jupyter_ai\config.json

- To use in magic command (%%ai), must set by 1 but not 2.
- To use in chat interface, must set by 2 but not 1
- Failed to setup %ai magic command for azure openai (ok for openai)

- Successed history
    - successed to set Azure OpenAI LLM for chat interface
    - successed to set OpenAI::gpt-4 LLM
    - successed to set OpenAI compatible custom API using OpenAI::gpt-4 I/F
    - failed to set OpenAI compatible custom API using Azure OpenAI I/F

### Custom LLM
- https://jupyter-ai.readthedocs.io/en/latest/developers/entry_points_api/model_providers_group.html#how-to-define-a-custom-model-provider
    1. create python package code for custom LLM
    2. install the package
    3. restart jupyter
- custom LLM setting effects on both magic command and chat interface.

### Usage (magic command)
- https://jupyter-ai.readthedocs.io/en/latest/examples/magics.html
- load ext
    ```
    [1]: %load_ext jupyter_ai
    ```
- help of %%ai
    ```
    [1]: %ai help
    [2]: %ai list
    ```
- chat
    ```
    [1]: %%ai gpt4
         世界一高い山は
    [1]: %%ai azure-chat-openai:gpt-4.1
         世界一高い山は 　　→★エラー
    ```
    ```
    [1]: %%ai my_provider:model_a
         世界一高い山は
    ```
- generate code
    ```
    [1]: %%ai gpt4 -f code
         120の約数を列挙して
    ```

### Run
- To install python module (to current environment)
    - in jupyter cell,
    ```
    %pip install <module>
    ```

