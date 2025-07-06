## Gemma

- [紹介](https://gigazine.net/news/20250627-google-gemma-3n-full-release/)

- [公式](https://developers.googleblog.com/en/introducing-gemma-3n-developer-guide/?_gl=1*xzeajg*_up*MQ..*_ga*MTk4NzQ2MjMzNi4xNzUxNzI0NzAx*_ga_H733Y2BZES*czE3NTE3MjQ3MDEkbzEkZzEkdDE3NTE3MjU1MjMkajYwJGwwJGgw)

- Gemma 3nが2025年6月26日に正式リリースされ、Hugging FaceとKaggleでモデルデータをダウンロードできるようになりました。
- 「Gemma 3n E2B」はパラメーター数5Bながら従来の2Bモデルと同等のメモリ消費量を実現しており、最小2GBのメモリ使用量で動作可能。また、「Gemma 3n E4B」のパラメーター数は8Bですが、従来の4Bモデルと同等のメモリフットプリントで動作し、3GBのメモリ使用量で実行できます。

### Build with Ollama
https://ollama.com/library/gemma3n

1. install Ollama for windows
   https://ollama.com/download/windows

2. download and register
    ```
    ollama pull gemma3n:e4b
    ollama run gemma3n:e4b
    >>> /bye

    ollama list
    ollama ps
    ollama stop gemma3n:e4b
    ```
3. select ollama/gennma in applications

### Open Web UI
https://qiita.com/Yuzpomz/items/35965a44c958aafbde53
https://github.com/open-webui/open-webui
https://openwebui.com/

```
python -m pip install --upgrade pip
pip install open-webui
open-webui serve
http://localhost:8080
```
