# オンラインPDF販売ECサイト 設計書

## 1. システム構成
- フレームワーク: Flask
- データベース: MySQL
- ORM: SQLAlchemy
- 認証: Flask-Login
- 環境変数管理: python-dotenv

## 2. ディレクトリ構成
```
workspace/
├── app.py                # アプリケーション本体
├── models.py             # DBモデル定義
├── forms.py              # WTForms定義
├── static/               # 静的ファイル（画像・CSS等）
├── templates/            # HTMLテンプレート
├── requirements.txt      # 必要パッケージ
├── .env                  # 環境変数
├── README.md             # 要件定義・概要
├── design.md             # 設計書（本ファイル）
├── user_manual.md        # ユーザマニュアル
└── ...
```

## 3. 主なモデル
- User（ユーザー情報）
- Product（商品情報：PDFファイル）
- Cart（カート情報）
- Order（注文・購入履歴）

## 4. 主な画面・ルート
- `/` トップページ・商品一覧
- `/product/<id>` 商品詳細
- `/register` ユーザー登録
- `/login` ログイン
- `/logout` ログアウト
- `/cart` カート内容表示
- `/cart/add/<id>` カートに追加
- `/checkout` 購入手続き
- `/download/<order_id>/<product_id>` PDFダウンロード

## 5. セキュリティ
- パスワードはハッシュ化して保存
- ファイルダウンロードは認証・購入済みチェック
- SQLインジェクション対策（ORM利用）
- .envでDB接続情報等を管理

## 6. 決済
- MVPではダミーのクレジットカード決済（実際の決済APIは未連携）

## 7. 拡張性
- レコメンド・レビュー等は今後追加可能

---

# ER図（簡易）

```
User ---< Order >--- Product
User ---< Cart >--- Product
```

---

# 各種詳細はコード・README参照
