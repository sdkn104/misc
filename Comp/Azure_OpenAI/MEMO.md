# Azure OpenAI Service

* 公式ドキュメント(https://learn.microsoft.com/ja-jp/azure/ai-services/openai/)

## setup
1. [Azure Portal](https://portal.azure.com/#home) にログイン

1. サブスクリプションを作成しておく。

1. 「Azure OpenAI」リソースの作成 [ref](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
    1. Azure Portal の「リソースの作成」ボタンをクリックし、検索ボックスに「Azure OpenAI」と入力します。Azure OpenAIのCreateをクリック。
        1. リソースグループを作成する
        1. 名前、region（japaneast, eastus）を入力する
        1. networkアクセス制限設定で一旦以下を選択：「すべてのネットワークを許可する」
    1. networkの設定をする [ref](https://learn.microsoft.com/en-us/azure/ai-services/cognitive-services-virtual-networks?tabs=portal
    )
        1. Azure Portal で対象の OpenAI リソースを開き、「Networking（ネットワーク）」→「Firewalls and virtual networks」を選択
        1. Virtual Networkは設定しない
        1. Firewall設定で、アクセス元のIPアドレス範囲を指定


1. モデルをデプロイする[ref](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
    1. Azure AI Foundry ポータルにサインイン(https://ai.azure.com/?cid=learnDocs)
    1. 使用するサブスクリプションと Azure OpenAI リソースを選択
    1. [管理] で [デプロイ]  -- [新しいデプロイを作成する]
    1. モデル選択、デプロイ名(任意文字列、APIの呼び出しに必要)の入力
    1. デプロイの種類: 「グローバル標準」を選択。(データは国外に出るので個人情報禁止)
    1. 詳細オプションで、コンテンツフィルタ、quotaを設定可能
       - コンテンツフィルタはデフォルト内容のままにしておく
    * 一部の Azure OpenAI モデルまたは機能にアクセスするには、制限付きアクセス登録が必要です。例：modified content filters and/or abuse monitoring
    [ref](https://learn.microsoft.com/ja-jp/legal/cognitive-services/openai/limited-access)
    * Azure AI Foundry ポータルのプレイグラウンドで試使用可能

1. API キーとエンドポイントの取得
    * Azure AI Foundry ポータルの「デプロイ」から確認できます。
    * リソースの「Keys and Endpoint（キーとエンドポイント）」セクションで、API キーとエンドポイント URL を確認できます。
    * キーとエンドポイントのroot部分はリソースで同一と思われる

1. APIバージョン
    * 使用するとき、利用可能なバージョンを指定すればよい。[最新バージョン](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/api-version-lifecycle?tabs=key#updating-api-versions)

## データセキュリティ
- https://learn.microsoft.com/ja-jp/azure/ai-foundry/responsible-ai/openai/data-privacy?tabs=azure-portal
- 不正利用監視のためのデータ保存のオプトアウト
    - https://learn.microsoft.com/ja-jp/azure/ai-foundry/openai/concepts/abuse-monitoring
    - https://www.genspark.ai/spark/azure-openai%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E3%82%AA%E3%83%97%E3%83%88%E3%82%A2%E3%82%A6%E3%83%88%E5%BE%8C%E3%81%AE%E3%83%AD%E3%82%B0%E7%9B%A3%E8%A6%96/e3258a3a-86dd-4fea-9eb7-c141608a4cdc
    - https://zenn.dev/microsoft/articles/azure-openai-faq
    - 入力や出力データは特に何も構成されない場合、最大30日間は不正利用監視のために限られたメンバーのみが閲覧できる状態でMicrosoftが保存します、この不正監視のためのデータ保存はオプトアウトを申請することができます。
- データ処理の場所
    - デプロイ時にDataZoneで日本を指定すると、データ処理は日本国内にとどまる。
- 設定
    - アクセス元IPアドレス範囲指定
    - API KEYの管理
    - データの一時保存のオプトアウト
    - HTTPSを強制（HTTPはできないので設定不要）
    - Azure PortalのID, PW管理    

## 使用量・ログ
- Azure Portal - コストの管理と請求 - コスト管理 - コスト分析
    - タグ毎に集計可能
- Azure Portal - 監視 - メトリック
    - リクエスト数など
- ログ取得
    - LLMアクセスログを取得するには、Azure API Managementサービスを使う必要がある（データの一時保存をオプトアウトした場合）が、このサービスは有料。


# OpenAI API
* API Key: https://platform.openai.com/settings/organization/api-keys
