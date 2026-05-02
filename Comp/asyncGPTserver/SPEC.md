# Async GPT Server 仕様書

## 1. 概要

この仕様書は、REQ.mdに記載された要件に基づいて、Flaskフレームワークを使用したWeb APIの実装を定義します。
本APIは、非同期でAzure OpenAI APIを呼び出し、その結果をSQLiteデータベースに保存し、クライアントからの問い合わせに対して結果を返却する機能を備えます。

## 2. システム概要

- **フレームワーク**: Flask (Python)
- **データベース**: SQLite (WALモード)
- **外部API**: Azure OpenAI API
- **処理方式**: 非同期処理 (async/awaitを使用)

システムは以下の主要コンポーネントから構成されます：
- Web APIサーバー (Flask)
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
   - Azure OpenAI APIを非同期で呼び出し
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
    "request_id": "uuid-string",  // オプション
    "prompt": "生成するテキストのプロンプト",
    "model": "gpt-3.5-turbo",  // オプション
    "max_tokens": 100,         // オプション
    "temperature": 0.7         // オプション
  }
  ```
- **レスポンス**:
  ```json
  {
    "request_id": "uuid-string",
    "status": "processing"
  }
  ```

#### GET /result/{request_id}
- **説明**: 生成結果を取得
- **レスポンス**:
  ```json
  {
    "request_id": "uuid-string",
    "status": "completed|processing|failed",
    "result": "生成されたテキスト",  // statusがcompletedの場合
    "error": "エラーメッセージ"       // statusがfailedの場合
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
- 入力バリデーション: プロンプトの長さ制限、特殊文字チェック

## 5. データモデル

### 5.1 リクエストテーブル
- request_id (TEXT, PRIMARY KEY): UUID形式
- prompt (TEXT): 生成プロンプト
- model (TEXT): 使用モデル
- max_tokens (INTEGER): 最大トークン数
- temperature (REAL): 温度パラメータ
- status (TEXT): processing|completed|failed
- created_at (TIMESTAMP): 作成日時
- updated_at (TIMESTAMP): 更新日時

### 5.2 結果テーブル
- request_id (TEXT, PRIMARY KEY, FOREIGN KEY): リクエストID
- result (TEXT): 生成結果
- error (TEXT): エラーメッセージ (失敗時)

## 6. 技術仕様

### 6.1 環境
- Python 3.8+
- Flask 2.0+
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

- v1.1: 非同期処理の明確化 (async/await使用) (2026-05-02)
- v1.0: 初回仕様書作成 (2026-05-02)