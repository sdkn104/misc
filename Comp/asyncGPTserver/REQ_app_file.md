REQ_app_file.md

app_file.pyファイルに以下のコードを生成して。

## 処理
- 一秒ごとにinput_queueフォルダをチェックし、ファイルがあれば一つファイルを読み込みファイルを削除する。ファイルにはEntryIDとmessageIDがコンマ区切りで格納されている。
- 読み込んだら、win32 outlookにてEntryIDからメールを取得、messageID, subject, sent, to, from, cc, bodyを取得する。
- ファイルから読み込んだmessage-idと、Outlookから取得したmessage-idが一致するか照合する。一致しなければerror.txtと標準出力にエラー（件名・送信日時を含む）を出力してそのファイルの処理を終了する。
- 以下の条件をチェックし、満たさなければそのファイルの処理を終了、満たせばＡＰＩを叩く。
    - Fromのinternet mail addressが、MitsubishiElectric.co.jpを含む
    - Toに自分自身のinternet mail addressがある。
    - Toが、８個以下。
- APIは別スレッドのイベントループで非同期実行する。APIの内容は、@app.py　ファイルのgenerate_text()と同じ。
- APIの呼び出し結果は、output_storeフォルダ内に、{internet message-id}.jsonの名前のファイルを作成して書き込む。ファイル名に使えない文字はエスケープする。

## その他
- "自分自身のメールアドレス（Toの条件チェック用）はどこから取得しますか？"="Outlookのカレントユーザーから自動取得（推奨）"
- "Azure OpenAI APIに送るリクエストbodyの内容はどうしますか？"="メール内容から自動構成"
