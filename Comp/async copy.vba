TODO:
- limit number of parallel tasks
- re-register when prompt changes


Function AskGPT(prompt As String) As String
    Application.Volatile

    Dim v As Variant
    v = GetResultForCell(Application.Caller)

    If IsError(v) Then
        ' まだ結果がない → タスク登録して "Loading..."
        RegisterAskGPT Application.Caller, prompt
        AskGPT = "Loading..."
    Else
        ' 結果がある → それを返す
        AskGPT = v
    End If
End Function


' Module: modAskGPTParallel


Option Explicit

Private Type AskTask
    SheetName As String
    CellAddress As String
    Prompt As String
    Http As Object
    Done As Boolean
End Type

Private Tasks() As AskTask
Private TaskCount As Long
Private Polling As Boolean

Public ResultDict As Object ' CellKey → Result(JSON or text)

Private Const API_URL As String = "https://api.openai.com/v1/chat/completions"
Private Const API_KEY As String = "YOUR_API_KEY"
Private Const MODEL As String = "gpt-4o-mini"

'===========================
' 初期化
'===========================
Private Sub Init()
    If ResultDict Is Nothing Then
        Set ResultDict = CreateObject("Scripting.Dictionary")
    End If
End Sub

Private Function CellKey(ws As Worksheet, addr As String) As String
    CellKey = ws.Parent.Name & "!" & ws.Name & "!" & addr
End Function

'===========================
' AskGPT から呼ばれる登録処理
'===========================
Public Sub RegisterAskGPT(cell As Range, prompt As String)
    Init

    Dim t As AskTask
    Dim ws As Worksheet
    Set ws = cell.Worksheet

    TaskCount = TaskCount + 1
    ReDim Preserve Tasks(1 To TaskCount)

    t.SheetName = ws.Name
    t.CellAddress = cell.Address
    t.Prompt = prompt
    t.Done = False

    Set t.Http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    Tasks(TaskCount) = t

    SendRequest TaskCount
    StartPolling
End Sub

'===========================
' HTTP リクエスト送信
'===========================
Private Sub SendRequest(i As Long)
    Dim body As String
    body = "{""model"":""" & MODEL & """,""messages"":[{""role"":""user"",""content"":""" & EscapeJson(Tasks(i).Prompt) & """}]}"

    With Tasks(i).Http
        .Open "POST", API_URL, True
        .setRequestHeader "Content-Type", "application/json"
        .setRequestHeader "Authorization", "Bearer " & API_KEY
        .send body
    End With
End Sub

'===========================
' JSON エスケープ
'===========================
Private Function EscapeJson(s As String) As String
    s = Replace(s, "\", "\\")
    s = Replace(s, """", "\""")
    s = Replace(s, vbCrLf, "\n")
    s = Replace(s, vbCr, "\n")
    s = Replace(s, vbLf, "\n")
    EscapeJson = s
End Function

'===========================
' ポーリング開始
'===========================
Private Sub StartPolling()
    If Not Polling Then
        Polling = True
        Application.OnTime Now + TimeSerial(0, 0, 1), "PollAskGPT"
    End If
End Sub

'===========================
' ポーリング処理
'===========================
Public Sub PollAskGPT()
    On Error GoTo SafeExit

    Dim i As Long
    Dim allDone As Boolean
    Dim resp As String
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim key As String

    If Not Polling Then Exit Sub

    Set wb = ThisWorkbook
    allDone = True

    For i = 1 To TaskCount
        If Not Tasks(i).Done Then
            allDone = False

            If Tasks(i).Http.readyState = 4 Then
                resp = Tasks(i).Http.responseText
                Tasks(i).Done = True

                ' 結果を辞書に保存（セルは書き換えない）
                Set ws = wb.Worksheets(Tasks(i).SheetName)
                key = CellKey(ws, Tasks(i).CellAddress)
                ResultDict(key) = resp

                ' そのセルだけ UDF を再計算させる
                With ws.Range(Tasks(i).CellAddress)
                    .Formula = .Formula
                End With
            End If
        End If
    Next i

    If allDone Then
        Polling = False
    Else
        Application.OnTime Now + TimeSerial(0, 0, 1), "PollAskGPT"
    End If

    Exit Sub

SafeExit:
    Application.OnTime Now + TimeSerial(0, 0, 2), "PollAskGPT"
End Sub

'===========================
' 結果取得ヘルパー
'===========================
Public Function GetResultForCell(cell As Range) As Variant
    Init
    Dim k As String
    k = CellKey(cell.Worksheet, cell.Address)
    If ResultDict.Exists(k) Then
        GetResultForCell = ResultDict(k)
    Else
        GetResultForCell = CVErr(xlErrNA)
    End If
End Function
