import pandasai as pai
from pandasai_openai import AzureOpenAI
import os


api_key = os.environ.get("AZURE_OPENAI_API_KEY")
dep_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
llm = AzureOpenAI(api_key=api_key, deployment_name=dep_name)  # The name of your deployed model
print(api_key)
print(f"Using Azure OpenAI deployment: {dep_name}"  )

pai.config.set({
    "llm": llm
})

# Sample DataFrame
df = pai.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "revenue": [5000, 3200, 2900, 4100, 2300, 2100, 2500, 2600, 4500, 7000]
})

response = df.chat('Which are the top 5 countries by sales?')
print("response", response)

print("Done")

