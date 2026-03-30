# Cline

## Official
- https://cline.bot/
- https://github.com/cline/cline

## Example
- FPsim: https://note.com/sharelab/n/n65e8544a9412
- HDR: https://note.com/habatakurikei/n/nf833c058d99d
- 花粉症: https://qiita.com/makishy/items/4dd3662a52851a2c5ddc
- BeerLog: https://dackdive.hateblo.jp/entry/2025/02/17/184850
- HumbergerOrder: https://www.moonmile.net/blog/archives/10889

## Install and Setup
1. Install VS Code Extension "Cline" 
1. Select Cline Icon on left sidebar
1. Click "Use Your Own API Key" to avoid connecting Cline cloud
1. Set LLM ("OpenAI Compatible", etc)
    - Cline icon in left sidebar, Setting icon on top bar
    - To set Acure OpenAI, select OpenAI Compaible
    - To set cline service, select Cline
    - ex Azure OpenAI
        - Provider: OpenAI Compatible
        - BASE URL: https://bx22001zz-openai.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview
        - KEY: key
        - Model ID: gpt4.1
        - gpt-5xxx is not supported officially,  https://docs.cline.bot/provider-config/openai-compatible
        - for supported models, see https://docs.cline.bot/provider-config/openai-compatible#openai-compatible

## Setup using LiteLLM xxx -> failed...
- For using Azure OpenAI gpt-5, that is not suported by Cline, use LiteLLM proxy, that convert from Azure OpenAI gpt-4 to gpt-5, etc.

### installation
- https://docs.litellm.ai/docs/proxy/docker_quick_start#pre-requisites
```powershell
pip install litellm[proxy]
notepad LiteLLM/config.yaml
litellm --config LiteLLM/config.yaml --detailed_debug
```

## Usage

### Context Window max size
* cannot control by user
* code: cline/src/core/context/context-management/context-window-utils.ts
