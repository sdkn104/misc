# LIDA

- https://github.com/microsoft/lida

## setting Azure OpenAI
```powershell
pip install -U lida

```

```python
from lida import Manager, TextGenerationConfig, llm
text_gen = llm(
    provider="openai",
    api_type="azure",
    azure_endpoint=azure_endpoint, # ex. "https://xxxxx.openai.azure.com/openai/deployments/gpt-4.1-azure/chat/completions?api-version=2025-01-01-preview"
    api_key=api_key,
    api_version=api_version,
)
lida = Manager(text_gen=text_gen)
```
