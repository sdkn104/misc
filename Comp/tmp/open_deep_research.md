このコードは **LangGraph を使った「Deep Researchエージェント」**のメイン実装です。
簡単に言うと、

> **ユーザーの質問 → 調査計画 → 複数リサーチャーで調査 → 結果を圧縮 → 最終レポート生成**

という **マルチエージェント研究システム**を作っています。

構造はかなり大きいので、次の順で説明します。

1. 全体アーキテクチャ
2. メインの4フェーズ
3. Supervisor（研究リーダー）
4. Researcher（実際の調査役）
5. Graph構造（LangGraph）

---

# 1. 全体アーキテクチャ

このエージェントは **3種類のAI役割**で動きます。

```
User
  ↓
Clarifier (質問の確認)
  ↓
Research Planner
  ↓
Supervisor (研究リーダー)
  ↓
Researcher × N (実際の調査)
  ↓
Compressor (調査結果まとめ)
  ↓
Final Report Writer
```

LangGraph的には

```
Agent Graph
   |
   |-- Clarify
   |-- Research Brief
   |-- Supervisor Subgraph
           |
           |-- Researcher Subgraph × parallel
   |
   |-- Final Report
```

---

# 2. メインフェーズ

メインGraphはここで作られています。

```python
deep_researcher_builder = StateGraph(
    AgentState,
    input=AgentInputState,
    config_schema=Configuration
)
```

ノード構成

```python
clarify_with_user
write_research_brief
research_supervisor
final_report_generation
```

フロー

```
START
 ↓
clarify_with_user
 ↓
write_research_brief
 ↓
research_supervisor
 ↓
final_report_generation
 ↓
END
```

---

# 3. clarify_with_user

役割

**ユーザーの質問が曖昧なら追加質問する**

```python
async def clarify_with_user(state, config)
```

処理

### ① 設定確認

```python
configurable.allow_clarification
```

falseならスキップ。

---

### ② LLMに判断させる

```python
clarification_model.with_structured_output(ClarifyWithUser)
```

structured output:

```
need_clarification: bool
question: str
verification: str
```

---

### ③ 分岐

曖昧なら

```
AI: clarification question
END
```

明確なら

```
write_research_brief
```

---

# 4. write_research_brief

役割

**ユーザーの会話 → 調査計画に変換**

```python
async def write_research_brief()
```

LLMに作らせる

```
ResearchQuestion
```

例

```
User:
Explain EV battery market

↓

Research Brief:

Investigate:
- global EV battery market
- major manufacturers
- technology trends
```

---

その後 **Supervisorを初期化**

```python
supervisor_messages = [
 SystemMessage(lead_researcher_prompt),
 HumanMessage(research_brief)
]
```

---

# 5. Supervisor（研究リーダー）

ここが **Deep Researchの中核**。

```python
async def supervisor()
```

Supervisorは **3つのツールを持つ**

```python
lead_researcher_tools = [
 ConductResearch,
 ResearchComplete,
 think_tool
]
```

---

## Supervisorがやること

LLMが

```
think_tool
ConductResearch
ResearchComplete
```

を呼ぶ。

例

```
Thought:
We need market size and competitors

Tool Call:
ConductResearch("EV battery market size")

Tool Call:
ConductResearch("Top EV battery manufacturers")
```

---

# 6. supervisor_tools

ここで **Supervisorのツールを実行**

```python
async def supervisor_tools()
```

処理

### ① 終了条件

```
iteration limit
ResearchComplete
no tool call
```

なら

```
END
```

---

### ② think_tool

ただの思考ログ

```
Reflection recorded: ...
```

---

### ③ ConductResearch

ここが重要。

```python
researcher_subgraph.ainvoke(...)
```

つまり

**Researcher subgraphを並列実行**

```
Researcher 1
Researcher 2
Researcher 3
```

asyncで

```python
asyncio.gather(*research_tasks)
```

並列研究。

---

# 7. Researcher Subgraph

Researcherは **実際の調査役**。

構造

```
researcher
 ↓
researcher_tools
 ↓
compress_research
```

---

# 8. researcher

Researcherは **ツール付きLLM**

```python
tools = await get_all_tools(config)
```

例

```
web_search
tavily
MCP tools
think_tool
```

LLMは

```
search
think
search
```

を繰り返す。

---

# 9. researcher_tools

ツール実行部分

```python
tool_calls = most_recent_message.tool_calls
```

全部並列で実行

```python
asyncio.gather(...)
```

---

終了条件

```
iteration limit
ResearchComplete
```

なら

```
compress_research
```

---

# 10. compress_research

Researcherの結果を **要約**

```python
async def compress_research()
```

入力

```
AI messages
Tool outputs
Search results
```

LLMに

```
compress_research_system_prompt
```

を渡して

```
structured research summary
```

を作る。

出力

```
{
 compressed_research
 raw_notes
}
```

---

# 11. final_report_generation

最後に **最終レポート生成**

```python
async def final_report_generation()
```

入力

```
research_brief
notes
messages
```

LLMに

```
final_report_generation_prompt
```

を渡す。

出力

```
final_report
```

---

# 12. Graph構造（LangGraph）

このコードの一番重要な部分。

LangGraphは **状態マシン型AIエージェント**。

ノード

```
Node = function
```

エッジ

```
add_edge()
```

例

```python
supervisor_builder.add_node("supervisor", supervisor)
supervisor_builder.add_node("supervisor_tools", supervisor_tools)
```

フロー

```
START → supervisor → supervisor_tools → supervisor
```

ループ。

---

# 13. サブグラフ構造

このコードは **Graph inside Graph**。

```
Main Graph
   |
   |-- Supervisor Graph
            |
            |-- Researcher Graph
```

つまり

```
Agent
 ├ Supervisor
 │   ├ Researcher
 │   ├ Researcher
 │   └ Researcher
```

---

# 14. このコードのすごいポイント

### ① マルチエージェント

```
Supervisor
Researcher
Compressor
Writer
```

---

### ② 並列研究

```
asyncio.gather()
```

---

### ③ Tool-based reasoning

```
search
think
research
```

---

### ④ Token limit handling

```
retry
truncate
compress
```

---

### ⑤ LangGraph state machine

```
State → Node → Command → Next Node
```

---

# まとめ

このコードは

**Open Deep Research Agent**

の実装で、

流れは

```
User Query
   ↓
Clarify
   ↓
Research Brief
   ↓
Supervisor (research planner)
   ↓
Researcher × N (parallel research)
   ↓
Compress research
   ↓
Final report
```

つまり

**Perplexity / OpenAI Deep Research系のアーキテクチャ**です。

---

もし興味あればですが、このコードの理解で一番重要な

**LangGraphエージェント設計の核心**

```
State
Command
Subgraph
Tool loop
```

を **図付きで解説**できます。
これ理解すると **自分でDeep Researchエージェント作れるレベル**になります。
