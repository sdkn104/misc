
Set Fso = CreateObject( "Scripting.FileSystemObject" )
strCurPath = Fso.GetFile( WScript.ScriptFullName ).ParentFolder.Path
FileName = strCurPath & "\" & "Book1.xlsx"
FileName = strCurPath & "\" & "test.xls"


'outArr = ReadExcelFile( FileName, "[TABLE]") 'Named Range
'outArr = ReadExcelFile( FileName, "[Sheet1$]") 'Used Range of the Sheet
outArr = ReadExcelFile( FileName, "[Sheet1$A1:C4]") 'Specified Range


'表示
out = ""
For r = LBound(outArr,1) To UBound(outArr,1)
    For c = LBound(outArr,2) To UBound(outArr,2)
      out = out & outArr(r,c) & " "
    Next
    out = out & vbCrLf
Next
msgbox out


'*******************************************
' エクセルファイル読み込み関数
'*******************************************
' Requirement: "Microsoft Access Database Engine 2010(2016) Redistributable" installed
'   https://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=13255
Function ReadExcelFile(FileName, TableSpec)
  Set Cn = CreateObject( "ADODB.Connection" )
  Set Rs = CreateObject( "ADODB.Recordset" )

  '*******************************************
  ' 接続と取得
  '*******************************************
  ConnectionString = _
    "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" &  FileName & ";" & _
    "Extended Properties=""Excel 12.0 Xml;HDR=NO;IMEX=1"""
  On Error Resume Next
  Cn.Open ConnectionString
  If Err.Number <> 0 then
    ReadExcelFile = "Error: (" & Err.Number & ") " & Err.Description
    Wscript.Quit
  End If
  On Error Goto 0

  Query = "select * from " & TableSpec
  On Error Resume Next
  Rs.Open Query, Cn
  If Err.Number <> 0 then
    ReadExcelFile = "Error: (" & Err.Number & ") " & Err.Description
    Wscript.Quit
  End If
  On Error Goto 0

  '*******************************************
  ' 配列出力
  '*******************************************
  RowCount = 0
  Do While not Rs.EOF
    RowCount = RowCount + 1
    Rs.MoveNext
  Loop

  Dim outArr()
  ReDim outArr(RowCount - 1, Rs.Fields.Count - 1)

  Rs.MoveFirst
  For r = 0 to RowCount - 1
    For c = 0 to Rs.Fields.Count - 1
      outArr(r, c) = Rs.Fields(c).Value
    Next
    Rs.MoveNext
  Next

  ReadExcelFile = outArr

  '*******************************************
  ' クローズ
  '*******************************************
  Rs.Close
  Cn.Close
End Function

