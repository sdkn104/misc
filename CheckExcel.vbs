
Set Fso = CreateObject( "Scripting.FileSystemObject" )
strCurPath = Fso.GetFile( WScript.ScriptFullName ).ParentFolder.Path
FileName = strCurPath & "\" & "test.xls"

On Error Resume Next

Set XLS = CreateObject("Excel.Application")
XLS.Visible = False
XLS.DisplayAlerts = False
Set BK = XLS.Workbooks.Open(FileName, 0, False)
If Err.Number <> 0 Then MsgBox "ERROR:" & Err.Description
XLS.Run "CheckAndMail"
If Err.Number <> 0 Then MsgBox "ERROR1:" & Err.Description
BK.Save
If Err.Number <> 0 Then MsgBox "ERROR2:" & Err.Description
BK.Close
XLS.Quit
