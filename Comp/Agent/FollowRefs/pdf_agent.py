import asyncio
import io
import os
import xml.etree.ElementTree as ET
from typing import Annotated

import pypdf
import requests
from dotenv import load_dotenv
from pydantic import Field

from agent_framework import MCPStdioTool, tool
from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import AzureCliCredential

load_dotenv()

MAX_CHARS = 20_000


@tool(approval_mode="never_require")
def search_paper_pdf(
    title: Annotated[str, Field(description="検索する論文タイトル")],
) -> str:
    """論文タイトルからPDF URLを検索する。Semantic Scholar → arXiv の順に試みる。"""
    # 1. Semantic Scholar API (優先)
    try:
        resp = requests.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params={"query": title, "fields": "title,openAccessPdf", "limit": 3},
            timeout=15,
        )
        resp.raise_for_status()
        for paper in resp.json().get("data", []):
            pdf_info = paper.get("openAccessPdf")
            if pdf_info and pdf_info.get("url"):
                return pdf_info["url"]
    except requests.RequestException:
        pass

    # 2. arXiv API (フォールバック)
    try:
        resp = requests.get(
            "https://export.arxiv.org/api/query",
            params={"search_query": f"ti:{title}", "max_results": 3},
            timeout=15,
        )
        resp.raise_for_status()
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(resp.text)
        for entry in root.findall("atom:entry", ns):
            for link in entry.findall("atom:link", ns):
                if link.get("title") == "pdf":
                    return link.get("href", "")
    except (requests.RequestException, ET.ParseError):
        pass

    return f"PDF URLが見つかりませんでした: '{title}'"


@tool(approval_mode="never_require")
def read_pdf_from_url(
    url: Annotated[str, Field(description="読み込むPDFファイルのURL")],
    max_pages: Annotated[int, Field(description="最大読み込みページ数。0=全ページ")] = 0,
) -> str:
    """指定URLのPDFをダウンロードしてテキストを抽出する。"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.Timeout:
        return f"エラー: タイムアウト (30秒) — URL: {url}"
    except requests.HTTPError as e:
        return f"エラー: HTTPエラー {e.response.status_code} — URL: {url}"
    except requests.RequestException as e:
        return f"エラー: ダウンロード失敗 — {e}"

    try:
        reader = pypdf.PdfReader(io.BytesIO(response.content))
    except pypdf.errors.PdfReadError as e:
        return f"エラー: PDFの読み込みに失敗しました — {e}"

    pages = reader.pages
    if max_pages > 0:
        pages = pages[:max_pages]

    parts = []
    for i, page in enumerate(pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            parts.append(f"--- ページ {i} ---\n{text}")

    if not parts:
        return "テキストを抽出できませんでした（画像PDFの可能性があります）。"

    full_text = "\n\n".join(parts)
    clipped = len(full_text) > MAX_CHARS
    if clipped:
        full_text = full_text[:MAX_CHARS] + f"\n\n[... 残り {len(full_text) - MAX_CHARS} 文字は省略されました]"

    return full_text


def _trunc(s: str, n: int) -> str:
    s = str(s)
    return s[:n] + "..." if len(s) > n else s


def _display_content(content) -> None:
    """蓄積済み content を type ごとにまとめて表示する。"""
    match content.type:
        case "text":
            if content.text:
                print(content.text, flush=True)
        case "text_reasoning":
            if content.text:
                print(f"[Thinking] {content.text}", flush=True)
        case "function_call":
            print(f"\n[Tool] {content.name}({_trunc(content.arguments, 120)})", flush=True)
        case "function_result":
            print(f"  → {_trunc(content.result, 80)}", flush=True)
        case "mcp_server_tool_call":
            print(f"\n[Browser] {content.name}({_trunc(content.arguments, 120)})", flush=True)
        case "mcp_server_tool_result":
            print(f"  → {_trunc(content.result, 80)}", flush=True)


def build_client() -> OpenAIChatCompletionClient:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    model = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.environ.get("OPENAI_API_VERSION")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")

    if not endpoint or not model:
        raise RuntimeError(
            "AZURE_OPENAI_ENDPOINT と AZURE_OPENAI_DEPLOYMENT_NAME を .env または環境変数に設定してください。"
        )

    kwargs: dict = dict(
        model=model,
        azure_endpoint=endpoint,
        api_version=api_version,
    )
    if api_key:
        kwargs["api_key"] = api_key
    else:
        kwargs["credential"] = AzureCliCredential()

    return OpenAIChatCompletionClient(**kwargs)


async def main() -> None:
    client = build_client()
    agent = client.as_agent(
        name="PDFAgent",
        instructions=(
            "あなたはPDF論文を読み込んで内容を解説・回答するアシスタントです。"
            "論文タイトルが与えられた場合は search_paper_pdf でPDF URLを探し、"
            "見つかったURLを read_pdf_from_url で読み込んでください。"
            "URLが直接与えられた場合は read_pdf_from_url で直接読み込んでください。"
            "ブラウザ操作が必要な場合は playwright ツール群を使用してください。"
        ),
        tools=[search_paper_pdf, read_pdf_from_url],
    )

    print("PDF Agent 起動中。論文タイトルまたはURLを含む質問を入力してください。")
    print("例1: Attention Is All You Need を要約して")
    print("例2: https://arxiv.org/abs/1706.03762 をブラウザで開いて要約して")
    print("終了するには 'quit' または 'exit' を入力してください。\n")

    async with MCPStdioTool(
        name="playwright",
        command="npx",
        args=["@playwright/mcp", "--browser=msedge"],
    ) as playwright_mcp:
        session = agent.create_session()

        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit"):
                break

            print("\nAgent:", flush=True)
            acc = None
            async for update in agent.run(user_input, stream=True, tools=playwright_mcp, session=session):
                for content in update.contents:
                    if acc is None:
                        acc = content
                    elif acc.type == content.type:
                        try:
                            acc = acc + content
                        except Exception:
                            _display_content(acc)
                            acc = content
                    else:
                        _display_content(acc)
                        acc = content
            if acc is not None:
                _display_content(acc)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
