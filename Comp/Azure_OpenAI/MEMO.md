## Azure OpenAI Service

###
* 公式ドキュメント(https://learn.microsoft.com/ja-jp/azure/ai-services/openai/)

### setup
1. [Azure Portal](https://portal.azure.com/#home) にログイン

1. Azure OpenAI リソースの作成 [ref](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
    * Azure Portal の「リソースの作成」ボタンをクリックし、検索ボックスに「Azure OpenAI」と入力します。
    * 名前、region, networkアクセス制限設定 を入力
    * 利用申請について： 一部の Azure OpenAI Service では、利用申請が必要な場合があります。初めて利用する場合は、利用許可の申請手順も確認しておくとよいでしょう。

1. モデルをデプロイする[ref](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
    1. Azure AI Foundry ポータルにサインイン(https://ai.azure.com/?cid=learnDocs)
    1. [管理] で [デプロイ]  -- [新しいデプロイを作成する]
    1. モデル選択、デプロイ名(任意文字列、APIの呼び出しに必要)の入力
    1. 詳細オプションで、コンテンツフィルタ、quotaを設定可能
    * 一部の Azure OpenAI モデルまたは機能にアクセスするには、制限付きアクセス登録が必要です。例：modified content filters and/or abuse monitoring
    [ref](https://learn.microsoft.com/ja-jp/legal/cognitive-services/openai/limited-access)
    * -> Azure AI Foundry ポータルのプレイグラウンドで試使用可能

1. API キーとエンドポイントの取得
    * リソースの「Keys and Endpoint（キーとエンドポイント）」セクションで、API キーとエンドポイント URL を確認できます。

