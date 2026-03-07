# Documents

- https://data-formulator.ai/
- https://github.com/microsoft/data-formulator


# code Structure

- Web UI is created using React-Redux 
    - in src/*
- Web API that is called by view of React-Redux
    - in py-src/data_formulator/app.py, *_route.py
- agent classes that is used in Web API
    - in py-src/data_formulator/agents/*
- LLM model config is setting in UI, and used body of API call by UI
    - config is stored in redux df

- LLM model (wrapper) is defined in py-src/data_formulator/agents/client_utils.py  
    ```python
    class OpenAIClientAdapter(object): --> Not Used
    class Client(object):
    ```


# a

