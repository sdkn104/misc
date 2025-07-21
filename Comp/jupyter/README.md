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
- To use Model, install its Python packages and set its API key in your environment or in the chat interface.
    * Set environment variable:  $env:OPENAI_KEY = "openAI API key"
    * Set by GUI:
        1. open chat interface by clicking Chat icon in left bar,
        2. open setting panel
        3. set model, key, other parameters
        4. save

### Custom LLM
- https://jupyter-ai.readthedocs.io/en/latest/developers/entry_points_api/model_providers_group.html#how-to-define-a-custom-model-provider


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
- generate code
    ```
    [1]: %%ai gpt4 -f code
         120の約数を列挙して
    ```

### Run

