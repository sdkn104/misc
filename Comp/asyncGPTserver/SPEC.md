# FastAPI Async GPT Server 仕様書

## 1. 概要

この仕様書は、REQ.mdに記載された要件に基づいて、FastAPIフレームワークを使用したWeb APIの実装を定義します。
本APIは、非同期でAzure OpenAI APIを呼び出し、その結果をSQLiteデータベースに保存し、クライアントからの問い合わせに対して結果を返却する機能を備えます。

## 2. システム概要

- **フレームワーク**: FastAPI (Python)
- **データベース**: SQLite (WALモード)
- **外部API**: Azure OpenAI API
- **処理方式**: 非同期処理 (async/awaitを使用)

システムは以下の主要コンポーネントから構成されます：
- Web APIサーバー (FastAPI)
- 非同期タスク処理モジュール
- データベース管理モジュール
- Azure OpenAI API連携モジュール

## 3. 機能要件

### 3.1 主要機能

1. **テキスト生成リクエスト受付**
   - クライアントからテキスト生成リクエストを受け付ける
   - リクエストパラメータ: プロンプト、モデル設定、オプション
   - `request_id`をクライアントから指定可能。指定がない場合はサーバーが自動生成し、即時返却

2. **非同期処理**
   - Azure OpenAI APIを非同期で呼び出して即応答
   - 処理結果をSQLiteデータベースに保存

3. **結果取得**
   - リクエストIDを指定して処理結果を取得
   - 処理中、完了、失敗のステータスを返却

### 3.2 APIエンドポイント

#### POST /generate
- **説明**: テキスト生成リクエストを送信
- **リクエストボディ**:
  ```json
  {
    "request_id": "id-string",          // オプション
    "azure_openai_body": {
      "model": "gpt-4.1",
      "messages": [{"role": "user", "content": "..."}],
      "max_completion_tokens": 500,     // オプション
      "reasoning_effort": "high"        // オプション
    }
  }
  ```
- **備考**: `azure_openai_body` の内容は型チェックを行わず、そのまま Azure OpenAI API へ渡す
- **レスポンス**:
  ```json
  {
    "request_id": "id-string",
    "status": "processing"
  }
  ```

#### GET /history
- **説明**: 全リクエストの処理履歴を取得
- **レスポンス**: 新しい順の配列
  ```json
  [
    {
      "request_id": "uuid-string",
      "model": "gpt-4.1",
      "status": "completed|processing|failed",
      "created_at": "2026-05-04 12:34:56.789000",
      "updated_at": "2026-05-04 12:35:01.123000",
      "azure_response_status": 200,
      "azure_openai_body": { ... }
    }
  ]
  ```
- **備考**: `azure_openai_body` は処理中（results未登録）の場合 `null`

#### GET /result/{request_id}
- **説明**: 生成結果を取得
- **HTTPステータス**: processing時は200。completed/failed時はAzure OpenAI APIのレスポンスステータスと同じ値を返す
- **レスポンス**:
  ```json
  {
    "request_id": "uuid-string",
    "status": "completed|processing|failed",
    "azure_openai_body": { ... }   // statusがcompleted/failedの場合。Azure OpenAI APIのレスポンスbodyをそのまま格納
  }
  ```

## 4. 非機能要件

### 4.1 パフォーマンス
- 同時リクエスト数: 最大10件
- 応答時間: 結果取得APIは即時返却、生成処理は非同期

### 4.2 信頼性
- エラーハンドリング: Azure OpenAI APIのエラーを適切に処理
- データ永続性: SQLite WALモードを使用し、データ損失を最小化

### 4.3 セキュリティ
- APIキー管理: Azure OpenAI APIキーを環境変数で管理

## 5. データモデル

### 5.1 リクエストテーブル
- request_id (TEXT, PRIMARY KEY): UUID形式
- prompt (TEXT): azure_openai_body の JSON 文字列
- model (TEXT): azure_openai_body から抽出したモデル名
- status (TEXT): processing|completed|failed
- created_at (TIMESTAMP): リクエスト受付時刻 (`datetime.now()` によるローカル時刻)
- updated_at (TIMESTAMP): ステータス更新時刻 (`datetime.now()` によるローカル時刻)

### 5.2 結果テーブル
- request_id (TEXT, PRIMARY KEY, FOREIGN KEY): リクエストID
- azure_response_status (INTEGER): Azure OpenAI APIのHTTPステータスコード
- azure_response_body (TEXT): Azure OpenAI APIのレスポンスbody JSON文字列

## 6. 技術仕様

### 6.1 環境
- Python 3.8+
- FastAPI 0.111+
- Uvicorn 0.24+
- azure-openai 1.0+
- sqlite3 (標準ライブラリ)

### 6.2 データベース設定
- SQLite WALモード有効化
- 自動マイグレーション (初回実行時)

### 6.3 非同期処理
- async/awaitを使用した非同期タスク実行
- バックグラウンドワーカーによるAzure OpenAI API呼び出し

## 7. 実装ガイドライン

### 7.1 コーディング標準
- PEP 8準拠
- 型ヒントの使用
- 適切なエラーハンドリング

### 7.2 テスト
- ユニットテスト: pytest使用
- APIテスト: requestsライブラリ使用

## 8. デプロイメント

- 単一プロセスでの実行を想定
- GunicornまたはuWSGIを使用した本番環境対応
- Dockerコンテナ化推奨

## 9. 変更履歴

- v1.6: `/history` エンドポイント追加。`created_at`/`updated_at` を SQLite デフォルトから Python `datetime.now()` によるローカル時刻記録に変更 (2026-05-04)
- v1.5: レスポンス形式変更 — `/result` のレスポンスボディを `{ request_id, status, azure_openai_body }` に変更。HTTPステータスをAzure OpenAI APIのステータスと一致させる。結果テーブルを `azure_response_status/azure_response_body` に変更 (2026-05-04)
- v1.4: リクエスト形式変更 — `/generate` のリクエストボディを `{ request_id, azure_openai_body }` に変更。azure_openai_body は型チェックなしで Azure OpenAI API に直接渡す (2026-05-04)
- v1.3: パラメータ変更 — `max_tokens`/`temperature` を廃止し `max_completion_tokens`/`reasoning_effort`/`verbosity` を追加。None 指定時は API リクエストに含めない (2026-05-04)
- v1.2: FastAPIへの移行 (2026-05-03)
- v1.1: 非同期処理の明確化 (async/await使用) (2026-05-02)
- v1.0: 初回仕様書作成 (2026-05-02)