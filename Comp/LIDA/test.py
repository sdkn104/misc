
import os
from lida import Manager, TextGenerationConfig, llm
from pprint import pprint

# === Azure OpenAI Service の設定よみこみ ===
api_key=os.environ["AZURE_OPENAI_API_KEY"]
azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"] # "https://xxxxx.openai.azure.com/openai/deployments/gpt-4.1-azure/chat/completions?api-version=2025-01-01-preview"
deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
api_version=os.environ["AZURE_OPENAI_API_VERSION"]


# === 日本語化 ===
class CustomLLM:
    def __init__(self, *args, **kwargs):
        print("=== custom LLM init ===")
        pprint(args)
        pprint(kwargs)
        self._base = llm(*args, **kwargs)
    def generate(self, *args, **kwargs):
        print("=== custom generate start ===")
        pprint(args)
        pprint(kwargs)
        kwargs["messages"] = kwargs["messages"] + [
            {
                "role": "system",
                #"content": "You must output everything in Japanese, except for code snippets and data labels which must be in original language.",    
                "content": "You must output everything in Japanese.",    
            }
        ]
        response = self._base.generate(*args, **kwargs)
        print("=== custom generate end ===")
        return response
    def __getattr__(self, name):
        return getattr(self._base, name)

#text_gen = llm(
text_gen = CustomLLM(
    provider="openai",
    api_type="azure",
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version,
    model=deployment_name,
)
lida = Manager(text_gen=text_gen)
textgen_config = TextGenerationConfig(n=1, temperature=1, use_cache=False)

# === サマリーとゴールの生成 ===
summary = lida.summarize(
    "holidays_events.csv", 
    summary_method="default", 
    textgen_config=textgen_config,
)  
persona = (
    "a Japanese data analyst who must output everything in Japanese and "
    "only generate goals about time-series trend analysis."
)
goals = lida.goals(summary, n=2, textgen_config=textgen_config,
    #persona=persona,
)
pprint(summary)
pprint(goals)

# === 可視化 ===
import matplotlib
matplotlib.rcParams['font.family'] = 'MS Gothic'  # または 'Yu Gothic'
charts = lida.visualize(summary=summary, goal=goals[0], textgen_config=textgen_config, library="matplotlib")
print(charts[0].code)

import base64
from PIL import Image
from io import BytesIO

chart = charts[0]
img_bytes = base64.b64decode(chart.raster)
img = Image.open(BytesIO(img_bytes))
img.show()
