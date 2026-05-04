Attribute VB_Name = "AsyncGPTClient"
' ================================================================
' AsyncGPT VBA Client
' 対象API: asyncGPTserver (app.py)
'
' 使い方 (VBAコードから):
'   Dim id As String
'   id = SendAsync("Pythonとは？")                              ' 送信してrequest_idを取得
'   id = SendAsync("Pythonとは？", "gpt-5-mini", 500)           ' max_completion_tokens指定
'   id = SendAsync("Pythonとは？", , 500, "high", "low")        ' reasoning_effort/verbosity指定
'   id = SendAsync("Pythonとは？", , , , , "my-id-001")         ' request_id指定
'
'   ' あとでGetResultで結果を取得 (生成テキスト / "PROCESSING" / "ERROR:...")
'   MsgBox GetResult(id)
'
' 送信されるJSON:
'   {
'     "request_id": "...",           ' 省略可
'     "azure_openai_body": {
'       "model": "gpt-4.1-azure",
'       "messages": [{"role": "user", "content": "..."}],
'       "max_completion_tokens": 500  ' 省略可
'     }
'   }
'
' 依存ライブラリ:
'   VBA-JSON (JsonConverter.bas) https://github.com/VBA-tools/VBA-JSON
'   VBEditor でインポートして使用すること
'
' 取り込み方法:
'   VBEditor > ファイル > ファイルのインポート > AsyncGPTClient.bas
' ================================================================
Option Explicit

Private Const API_BASE_URL As String = "http://localhost:8000"


' ================================================================
' Public API
' ================================================================
' リクエストを送信してrequest_idだけ返す
' 戻り値: request_id文字列 / "ERROR:..."
Public Function SendAsync(prompt As String, _
                          Optional model As String = "gpt-4.1-azure", _
                          Optional maxCompletionTokens As Variant = Null, _
                          Optional reasoningEffort As Variant = Null, _
                          Optional verbosity As Variant = Null, _
                          Optional requestId As Variant = Null) As String
    Dim innerBody As String
    Dim outerBody As String
    Dim response  As String
    Dim rid       As String
    Dim detail    As String

    innerBody = CreateRequestBody(prompt, model, maxCompletionTokens, reasoningEffort, verbosity)

    If Not IsNull(requestId) Then
        outerBody = "{""request_id"":" & EscapeJson(CStr(requestId)) & _
                    ",""azure_openai_body"":" & innerBody & "}"
    Else
        outerBody = "{""azure_openai_body"":" & innerBody & "}"
    End If

    response = HttpPost(API_BASE_URL & "/generate", outerBody)
    If Left(response, 6) = "ERROR:" Then
        SendAsync = response
        Exit Function
    End If

    rid = ExtractEscapeJsoning(response, "request_id")
    If rid = "" Then
        detail = ExtractEscapeJsoning(response, "detail")
        If detail = "" Then detail = response
        SendAsync = "ERROR: " & detail
        Exit Function
    End If
    SendAsync = rid
End Function


' request_idで結果をポーリングせず1回だけ取得する
' 戻り値: 生成テキスト / "PROCESSING" / "ERROR(status):..." / "ERROR:..."
Public Function GetResult(requestId As String) As String
    Dim response    As String
    Dim status      As String
    Dim azureStatus As Long
    response = HttpGet(API_BASE_URL & "/result/" & requestId)
    If Left(response, 6) = "ERROR:" Then
        GetResult = response
        Exit Function
    End If
    status = ExtractEscapeJsoning(response, "status")
    Select Case status
        Case "completed", "failed":
            azureStatus = CLng(ExtractEscapeJsoning(response, "azure_response_status"))
            GetResult = GetResponseText(azureStatus, response)
        Case "processing": GetResult = "PROCESSING"
        Case "":           GetResult = "ERROR: 指定のIDが見つかりません"
        Case Else:         GetResult = "ERROR: 不明なステータス (" & status & ")"
    End Select
End Function

' 処理履歴を全件取得する (新しい順)
' 戻り値: Collection of Dictionary (VBA-JSON形式) / Nothing (エラー時)
' 使い方:
'   Dim history As Object, entry As Object
'   Set history = GetHistory()
'   If Not history Is Nothing Then
'       For Each entry In history
'           Debug.Print entry("request_id"), entry("status"), entry("created_at")
'       Next
'   End If
Public Function GetHistory() As Object
    Dim response As String
    response = HttpGet(API_BASE_URL & "/history")
    If Left(response, 6) = "ERROR:" Then Exit Function
    On Error Resume Next
    Set GetHistory = ParseJson(response)
    On Error GoTo 0
End Function

' ================================================================
' Azure OpenAI APIのプロトコル処理
' ================================================================

' Azure OpenAI APIリクエストボディ (azure_openai_body) を生成する
' 戻り値: JSON文字列 例) {"model":"gpt-4.1-azure","messages":[...],...}
Private Function CreateRequestBody(prompt As String, _
                                  Optional model As String = "gpt-4.1-azure", _
                                  Optional maxCompletionTokens As Variant = Null, _
                                  Optional reasoningEffort As Variant = Null, _
                                  Optional verbosity As Variant = Null) As String
    Dim parts(4) As String
    Dim n        As Integer
    n = 0
    parts(n) = """model"":" & EscapeJson(model) : n = n + 1
    parts(n) = """messages"":[{""role"":""user"",""content"":" & EscapeJson(prompt) & "}]" : n = n + 1
    If Not IsNull(maxCompletionTokens) Then
        parts(n) = """max_completion_tokens"":" & CLng(maxCompletionTokens) : n = n + 1
    End If
    If Not IsNull(reasoningEffort) Then
            parts(n) = """reasoning_effort"":" & EscapeJson(CStr(reasoningEffort)) : n = n + 1
    End If
    If Not IsNull(verbosity) Then
            parts(n) = """verbosity"":" & EscapeJson(CStr(verbosity)) : n = n + 1
    End If
    CreateRequestBody = "{" & Join(parts, ",", n) & "}"
End Function

' Azure OpenAI APIレスポンスbodyからテキストを取り出す (VBA-JSON使用)
' 引数: azureStatus       = azure_response_status (HTTPステータスコード)
'       azureResponseBody = /result エンドポイントのレスポンスJSON文字列
' 戻り値: 200時は choices[0].message.content / エラー時は "ERROR(status): message"
Private Function GetResponseText(azureStatus As Long, azureResponseBody As String) As String
    On Error GoTo Fallback
    Dim parsed As Object
    Set parsed = ParseJson(azureResponseBody)
    If azureStatus = 200 Then
        GetResponseText = parsed("azure_openai_body")("choices")(1)("message")("content")
    Else
        GetResponseText = "ERROR(" & azureStatus & "): " & _
                          parsed("azure_openai_body")("error")("message")
    End If
    Exit Function
Fallback:
    GetResponseText = "ERROR(" & azureStatus & "): " & azureResponseBody
End Function


' 配列の先頭n要素をデリミタで結合する
Private Function Join(arr() As String, delim As String, count As Integer) As String
    Dim i   As Integer
    Dim buf As String
    For i = 0 To count - 1
        If i > 0 Then buf = buf & delim
        buf = buf & arr(i)
    Next i
    Join = buf
End Function

' ================================================================
' Private: HTTP
' ================================================================
Private Function HttpPost(url As String, body As String) As String
    Dim http As Object
    On Error GoTo Err_

    Set http = CreateObject("WinHttp.WinHttpRequest.5.1")
    http.Open "POST", url, False
    http.setRequestHeader "Content-Type", "application/json"
    http.Send body
    HttpPost = http.responseText  ' エラー判定はSendAsync側でrequest_idの有無を確認
    Exit Function
Err_:
    HttpPost = "ERROR: サーバーに接続できません (" & Err.Description & ")"
End Function

Private Function HttpGet(url As String) As String
    Dim http As Object
    On Error GoTo Err_

    Set http = CreateObject("WinHttp.WinHttpRequest.5.1")
    http.Open "GET", url, False
    http.Send
    HttpGet = http.responseText  ' Azure転送時は4xx/5xxでもbodyにJSONが入る
    Exit Function
Err_:
    HttpGet = "ERROR: サーバーに接続できません (" & Err.Description & ")"
End Function

' ================================================================
' Private: JSON ユーティリティ
' ================================================================

' JSONからキーに対応する値を文字列で取り出す (VBA-JSON使用)
' キー不在・パース失敗時は "" を返す
Private Function ExtractEscapeJsoning(json As String, key As String) As String
    On Error Resume Next
    ExtractEscapeJsoning = CStr(ParseJson(json)(key))
    On Error GoTo 0
End Function

' 文字列をJSON文字列リテラルに変換する ("..." 付き)
Private Function EscapeJson(s As String) As String
    s = Replace(s, "\", "\\")
    s = Replace(s, """", "\""")
    s = Replace(s, vbCr, "\r")
    s = Replace(s, vbLf, "\n")
    s = Replace(s, vbTab, "\t")
    EscapeJson = """" & s & """"
End Function
