## 要件定義書

### 1. プロジェクト概要

**プロジェクト名:** オンラインPDF販売ECサイト

**概要:** 
本プロジェクトは、PDF形式のファイルを販売するオンラインECサイトを構築するものです。ユーザーはサイト上で販売されているPDFファイルを閲覧、購入し、ダウンロードすることができます。

**システムの種類:** Webアプリケーション

**対象ユーザー:** 一般ユーザー

**開発環境:** python flaskによるWebアプリ。データベースはMySQL

### 2. 目的と背景

**目的:** 
AI駆動開発の実践例として、実際に運用可能なECサイトを構築することを目的とします。

**背景:** 
AI技術を活用した開発手法の有効性を検証し、今後の開発プロジェクトへの適用可能性を検討します。小規模ながらも、本番環境で運用できるレベルのECサイトを構築することで、AI駆動開発のメリットと課題を明確化します。

### 3. スコープ

**MVP (Minimum Viable Product):**

* 初期リリース段階では、販売するPDFファイル（書籍）の数は10程度とします。
* 基本的なECサイト機能（商品閲覧、購入、ダウンロード）を実装します。
* ユーザー登録、ログイン機能は必須とします。
* 決済機能は簡易的なもの（例：クレジットカード決済のみ）とします。
* 高度な機能（例：レコメンド機能、レビュー機能）は後回しとします。

### 4-1. 機能一覧

| 機能名 | 機能の概要説明 | 主な利用者 | 入力情報 | 出力情報 | 処理の流れ |
|---|---|---|---|---|---|
| 商品一覧表示 | 販売中のPDFファイルの一覧を表示する | 一般ユーザー | - | PDFファイル名、価格、表紙画像 | データベースから商品情報を取得し、一覧表示する |
| 商品詳細表示 | 選択したPDFファイルの詳細情報を表示する | 一般ユーザー | PDFファイルID | PDFファイル名、価格、表紙画像、詳細説明 | データベースから指定されたIDの商品情報を取得し、表示する |
| ユーザー登録 | 新規ユーザーがアカウントを作成する | 一般ユーザー | ユーザー名、メールアドレス、パスワード | 登録完了メッセージ | 入力された情報をデータベースに登録する |
| ログイン | 登録済みのユーザーがログインする | 一般ユーザー | メールアドレス、パスワード | ログイン成功/失敗メッセージ | 入力された情報とデータベースの情報を照合し、認証する |
| カートに追加 | 選択したPDFファイルをカートに入れる | 一般ユーザー | PDFファイルID | カートに追加完了メッセージ | ユーザーのカート情報にPDFファイルIDを追加する |
| カート内容表示 | カートに入っている商品の一覧を表示する | 一般ユーザー | - | カート内の商品一覧、合計金額 | ユーザーのカート情報から商品情報を取得し、表示する |
| 購入手続き | カート内の商品を購入する | 一般ユーザー | 決済情報 | 購入完了メッセージ、ダウンロードURL | 決済処理を行い、購入履歴をデータベースに登録する。ダウンロードURLを生成する |
| PDFファイルダウンロード | 購入したPDFファイルをダウンロードする | 一般ユーザー | ダウンロードURL | PDFファイル | ダウンロードURLに対応するPDFファイルをユーザーに提供する |

### 4-2. 画面一覧

| 画面名 | 画面の目的 | 主な利用者 | 表示する主な情報 | 主な操作項目 | 遷移先の画面 |
|---|---|---|---|---|---|
| トップページ | サイトの入り口、商品一覧への導線 | 一般ユーザー | サイトロゴ、おすすめ商品、新着商品 | 商品一覧へのリンク、ログイン/ユーザー登録へのリンク | 商品一覧画面、ログイン画面、ユーザー登録画面 |
| 商品一覧画面 | 販売中のPDFファイルの一覧を表示 | 一般ユーザー | PDFファイル名、価格、表紙画像 | 商品詳細へのリンク、カートに追加ボタン、並び替え/絞り込み | 商品詳細画面、カート内容表示画面 |
| 商品詳細画面 | 選択したPDFファイルの詳細情報を表示 | 一般ユーザー | PDFファイル名、価格、表紙画像、詳細説明 | カートに追加ボタン、購入手続きへ進むボタン | カート内容表示画面、購入手続き画面 |
| ユーザー登録画面 | 新規ユーザー登録 | 一般ユーザー | ユーザー名、メールアドレス、パスワード入力欄 | 登録ボタン | トップページ |
| ログイン画面 | 登録済みユーザーのログイン | 一般ユーザー | メールアドレス、パスワード入力欄 | ログインボタン | トップページ |
| カート内容表示画面 | カートに入っている商品の一覧を表示 | 一般ユーザー | カート内の商品一覧、合計金額 | 数量変更、削除、購入手続きへ進むボタン | 購入手続き画面 |
| 購入手続き画面 | 購入情報の入力と決済 | 一般ユーザー | 購入商品一覧、合計金額、決済情報入力欄 | 決済方法選択、注文確定ボタン | 購入完了画面 |
| 購入完了画面 | 購入完了の通知とダウンロードURLの表示 | 一般ユーザー | 購入完了メッセージ、ダウンロードURL | ダウンロードボタン | - |


**備考:**

* 上記は初期リリースにおける必要最低限の機能と画面です。
* 今後の開発フェーズで、機能追加や画面改修を行う可能性があります。
* 詳細な画面設計やUI/UXデザインは別途実施します。