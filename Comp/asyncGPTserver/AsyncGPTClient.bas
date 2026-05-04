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
'
'   ' あとでGetResultで結果を取得 (PROCESSING/completed/ERROR:...)
'   MsgBox GetResult(id)
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
Public Function SendAsync(prompt As String, _
                          Optional model As String = "gpt-4.1-azure", _
                          Optional maxCompletionTokens As Variant = Null, _
                          Optional reasoningEffort As Variant = Null, _
                          Optional verbosity As Variant = Null) As String
    Dim parts(4)  As String
    Dim n         As Integer
    Dim body      As String
    Dim response  As String

    n = 0
    parts(n) = """prompt"":"  & JsonStr(prompt) : n = n + 1
    parts(n) = """model"":"   & JsonStr(model)  : n = n + 1
    If Not IsNull(maxCompletionTokens) Then
        parts(n) = """max_completion_tokens"":" & CLng(maxCompletionTokens) : n = n + 1
    End If
    If Not IsNull(reasoningEffort) And CStr(reasoningEffort) <> "" Then
        parts(n) = """reasoning_effort"":" & JsonStr(CStr(reasoningEffort)) : n = n + 1
    End If
    If Not IsNull(verbosity) And CStr(verbosity) <> "" Then
        parts(n) = """verbosity"":" & JsonStr(CStr(verbosity)) : n = n + 1
    End If

    body = "{" & Join(parts, ",", n) & "}"

    response = HttpPost(API_BASE_URL & "/generate", body)
    If Left(response, 6) = "ERROR:" Then
        SendAsync = response
        Exit Function
    End If
    SendAsync = ExtractJsonString(response, "request_id")
End Function

' request_idで結果をポーリングせず1回だけ取得する
Public Function GetResult(requestId As String) As String
    Dim response As String
    Dim status As String
    response = HttpGet(API_BASE_URL & "/result/" & requestId)
    If Left(response, 6) = "ERROR:" Then
        GetResult = response
        Exit Function
    End If
    status = ExtractJsonString(response, "status")
    Select Case status
        Case "completed": GetResult = UnescapeJson(ExtractJsonString(response, "result"))
        Case "failed":    GetResult = "ERROR: " & UnescapeJson(ExtractJsonString(response, "error"))
        Case "processing": GetResult = "PROCESSING"
        Case Else:         GetResult = "ERROR: 不明なステータス (" & status & ")"
    End Select
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

    Select Case http.Status
        Case 200:  HttpPost = http.responseText
        Case 400:  HttpPost = "ERROR: 不正なリクエスト (400)"
        Case 409:  HttpPost = "ERROR: Request ID が重複しています (409)"
        Case Else: HttpPost = "ERROR: HTTP " & http.Status
    End Select
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

    Select Case http.Status
        Case 200:  HttpGet = http.responseText
        Case 404:  HttpGet = "ERROR: 指定のIDが見つかりません (404)"
        Case Else: HttpGet = "ERROR: HTTP " & http.Status
    End Select
    Exit Function
Err_:
    HttpGet = "ERROR: サーバーに接続できません (" & Err.Description & ")"
End Function

' ================================================================
' Private: JSON ユーティリティ
' ================================================================

' キーに対応する値を取り出す (文字列・数値・boolean対応)
Private Function ExtractJsonString(json As String, key As String) As String
    Dim pattern   As String
    Dim pos       As Long
    Dim valStart  As Long
    Dim valEnd    As Long

    pattern = """" & key & """:"
    pos = InStr(json, pattern)
    If pos = 0 Then Exit Function

    valStart = pos + Len(pattern)
    ' 先頭の空白をスキップ
    Do While Mid(json, valStart, 1) = " "
        valStart = valStart + 1
    Loop

    If Mid(json, valStart, 1) = """" Then
        ' 文字列値: "..." を取り出す
        valStart = valStart + 1
        valEnd = valStart
        Do
            valEnd = InStr(valEnd, json, """")
            If Mid(json, valEnd - 1, 1) <> "\" Then Exit Do  ' エスケープでない引用符
            valEnd = valEnd + 1
        Loop
        ExtractJsonString = Mid(json, valStart, valEnd - valStart)
    Else
        ' 数値・boolean・null
        valEnd = valStart
        Do While valEnd <= Len(json)
            Dim c As String
            c = Mid(json, valEnd, 1)
            If c = "," Or c = "}" Or c = "]" Then Exit Do
            valEnd = valEnd + 1
        Loop
        ExtractJsonString = Trim(Mid(json, valStart, valEnd - valStart))
    End If
End Function

' JSON文字列をVBAの文字列にアンエスケープする
Private Function UnescapeJson(s As String) As String
    s = Replace(s, "\""", """")
    s = Replace(s, "\\", "\")
    s = Replace(s, "\/", "/")
    s = Replace(s, "\n", vbLf)
    s = Replace(s, "\r", vbCr)
    s = Replace(s, "\t", vbTab)
    UnescapeJson = s
End Function

' 文字列をJSON文字列リテラルに変換する ("..." 付き)
Private Function JsonStr(s As String) As String
    s = Replace(s, "\", "\\")
    s = Replace(s, """", "\""")
    s = Replace(s, vbCr, "\r")
    s = Replace(s, vbLf, "\n")
    s = Replace(s, vbTab, "\t")
    JsonStr = """" & s & """"
End Function

