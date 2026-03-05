# LIDA

- https://github.com/microsoft/lida

## install
```powershell
pip install -U lida
python test.py
lida ui  --port=8080 --docs
```

## setting Azure OpenAI

```python
from lida import Manager, TextGenerationConfig, llm
api_key=os.environ["AZURE_OPENAI_API_KEY"]
azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"] 
deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
api_version=os.environ["AZURE_OPENAI_API_VERSION"]
text_gen = llm(
    provider="openai",
    api_type="azure",
    azure_endpoint=azure_endpoint, # ex. "https://xxxxx.openai.azure.com/openai/deployments/gpt-4.1-azure/chat/completions?api-version=2025-01-01-preview"
    api_key=api_key,
    api_version=api_version,
)
lida = Manager(text_gen=text_gen)
```

### setting for web ui
- modify myenv/Lib/site-packages/lida/web/app.py
    ```python
    #textgen = llm()
    api_key=os.environ["AZURE_OPENAI_API_KEY"]
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"] 
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
    api_version=os.environ["AZURE_OPENAI_API_VERSION"]
    textgen = llm(
        provider="openai",
        api_type="azure",
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )
    ```
## Japanize Vizual
```python
import matplotlib
matplotlib.rcParams['font.family'] = 'MS Gothic'  # または 'Yu Gothic'
```

## Access log
- add code to myenv/Lib/site-packages/lida/web/app.py
    ```python
    # === アクセスログ ===
    from fastapi import Request
    import time
    custom_logger = logging.getLogger("custom")
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler =  logging.FileHandler(filename='log/custom.log')
    handler.setFormatter(formatter)
    custom_logger.addHandler(handler)
    custom_logger.setLevel(logging.INFO)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        custom_logger.info(f"{request.client.host}:{request.client.port} {request.method} {request.url.path} status={response.status_code} time={process_time:.3f}s")
        return response
    ```

llmx - datamodel.py
@dataclass
class TextGenerationConfig:
    n: int = 1
    temperature: float = 0.1
    #max_tokens: Union[int, None] = None
    max_completion_tokens: Union[int, None] = None
    top_p: float = 1.0

llmx generator text/openai_textgen.py
oai_config = {
            "model": model,
            "temperature": config.temperature,
            #"max_tokens": max_tokens,
            "max_completion_tokens": max_tokens,
            "top_p": config.top_p,