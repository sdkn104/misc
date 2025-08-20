# Jupyter AI
- Jupyter: https://docs.jupyter.org/en/latest/
- Jupyter AI: https://jupyter-ai.readthedocs.io/en/latest/index.html#

### Setup
* use python 3.12
    ```powershell
    # install
    pip install jupyterlab~=4.0
    pip install jupyter-ai
    pip install langchain-openai
    pip install langchain-ollama
    # launch
    jupyter lab
    ```
- load jupyter-AI extension
    - https://jupyter-ai.readthedocs.io/en/latest/examples/magics.html
    ```
    [1]: %load_ext jupyter_ai
    ```

### Setting LLM
- https://jupyter-ai.readthedocs.io/en/latest/users/index.html#model-providers
- To use Model, install its Python packages and 
    1. set its API key in your environment or 
        * Set environment variable:  $env:OPENAI_KEY = "openAI API key"
    2. set it in the chat interface setting GUI
        1. open chat interface by clicking Chat icon in left bar,
        2. open setting panel
        3. set model, key, other parameters
        4. save
        * Alternatively, setting in config file:
            * C:\Users\QP48568\AppData\Roaming\jupyter\jupyter_ai\config.json

- To use in magic command (%%ai), must set by 1 but not 2.
- To use in chat interface, must set by 2 but not 1

- Successed history
    - successed to set Azure OpenAI LLM
    - successed to set OpenAI::gpt-4 LLM
    - successed to set OpenAI compatible custom API using OpenAI::gpt-4 I/F
    - failed to set OpenAI compatible custom API using Azure OpenAI I/F

### Custom LLM
- https://jupyter-ai.readthedocs.io/en/latest/developers/entry_points_api/model_providers_group.html#how-to-define-a-custom-model-provider
    1. create python package code for custom LLM
    2. install the package
    3. restart jupyter
- custom LLM setting effects on both magic command and chat interface.

### Usage
- help of %%ai
    ```
    [1]: %ai help
    ```
- chat
    ```
    [1]: %%ai gpt4
         世界一高い山は
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

