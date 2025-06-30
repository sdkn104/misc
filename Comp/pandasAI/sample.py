import pandasai as pai
from pandasai_openai import AzureOpenAI
import os

#api_key = os.environ.get("AZURE_OPENAI_API_KEY")
dep_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
llm = AzureOpenAI(
    deployment_name=dep_name,
)  # no need to pass the API key, endpoint and API version. They are read from the environment variable
print(f"Using Azure OpenAI deployment: {dep_name}"  )

pai.config.set({
    "llm": llm,
    "verbose": True,
})
print(llm)

# Sample DataFrame
df = pai.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "revenue": [5000, 3200, 2900, 4100, 2300, 2100, 2500, 2600, 4500, 7000]
})
print(df)
response = df.chat('Which are the top 5 countries by sales?')
print("response", response)

print("Done")

