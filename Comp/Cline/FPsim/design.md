# 資産見える化Webアプリ 詳細設計書

---

## 1. システム全体構成

- フロントエンド：Next.js（TypeScript, Tailwind CSS）
- バックエンド：Firebase Functions（Node.js）
- データベース：Firestore
- 認証：Firebase Auth（Googleアカウント等）
- AI連携：OpenAI API
- CI/CD：GitHub Actions

---

## 2. ディレクトリ構成（例）

```
asset-visualizer/
├── src/
│   ├── app/                # Next.js App Router
│   │   ├── page.tsx        # トップページ
│   │   ├── dashboard/      # ダッシュボード（資産グラフ）
│   │   ├── survey/         # アンケート入力
│   │   ├── auth/           # 認証関連
│   │   └── api/            # APIルート
│   ├── components/         # UIコンポーネント
│   ├── hooks/              # カスタムフック
│   ├── lib/                # Firebase/AI連携等のライブラリ
│   ├── styles/             # Tailwind等スタイル
│   └── types/              # 型定義
├── public/                 # 静的ファイル
├── .github/                # GitHub Actions等
├── .env.local              # 環境変数
├── package.json
└── README.md
```

---

## 3. 画面設計・画面遷移

### 主要ページ
- `/`（トップ）：サービス紹介・ログイン
- `/dashboard`：資産推移グラフ・サマリー
- `/survey`：資産アンケート入力
- `/edit/[id]`：資産データ編集
- `/auth/login`：ログイン画面

### UI要素
- ヘッダー：ロゴ、ナビゲーション、ユーザーメニュー
- メイン：各ページ固有のコンテンツ
- フッター：利用規約等
- モバイル対応：ハンバーガーメニュー、レスポンシブグリッド

---

## 4. API設計

### エンドポイント例（Next.js API Routes or Firebase Functions）

| メソッド | パス                | 概要                       | 入力例/パラメータ         | 出力例/レスポンス         |
|----------|---------------------|----------------------------|---------------------------|---------------------------|
| POST     | /api/assets         | 資産データ新規登録         | { year, totalAssets... }  | { id, ... }               |
| GET      | /api/assets         | 資産データ一覧取得         | なし                      | [{...}, {...}]            |
| GET      | /api/assets/[id]    | 資産データ詳細取得         | id                        | {...}                     |
| PUT      | /api/assets/[id]    | 資産データ更新             | id, 更新内容              | { success: true }         |
| DELETE   | /api/assets/[id]    | 資産データ削除             | id                        | { success: true }         |
| POST     | /api/ai/advice      | AIアドバイス生成           | { 資産データ }            | { adviceText }            |

---

## 5. データベース設計

### users
| フィールド      | 型       | 説明           |
|----------------|----------|----------------|
| uid            | string   | ユーザーID     |
| email          | string   | メールアドレス |
| displayName    | string   | 表示名         |
| createdAt      | timestamp| 登録日時       |

### user_assets
| フィールド      | 型       | 説明           |
|----------------|----------|----------------|
| id             | string   | 資産データID   |
| uid            | string   | ユーザーID     |
| year           | number   | 年             |
| totalAssets    | number   | 資産総額       |
| income         | number   | 年間収入       |
| expenses       | number   | 年間支出       |
| memo           | string   | メモ           |
| createdAt      | timestamp| 登録日時       |

### ai_advice
| フィールド      | 型       | 説明           |
|----------------|----------|----------------|
| id             | string   | アドバイスID   |
| assetId        | string   | 資産データID   |
| adviceText     | string   | AIアドバイス   |
| createdAt      | timestamp| 登録日時       |

---

## 6. 認証・認可設計

- Firebase AuthによるGoogleアカウント等での認証
- Firestoreセキュリティルールでユーザー自身のデータのみアクセス可能に制御

---

## 7. 非機能要件・運用設計

- パフォーマンス：初回表示2秒以内、グラフ描画0.5秒以内
- セキュリティ：XSS/CSRF対策、認証必須ページのガード
- アクセシビリティ：キーボード操作、色覚対応
- テスト：Jest/React Testing Library/Playwright
- CI/CD：GitHub Actionsによる自動テスト・デプロイ

---

## 8. 将来的な拡張設計

- チャットボット連携、ランキング表示、外部API連携（Yahoo Finance, Google News等）
- マルチアカウント対応、通知機能、ダークモード

---
