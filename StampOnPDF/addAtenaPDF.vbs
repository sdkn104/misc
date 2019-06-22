
INPDF="250_information.pdf"
OUTPDF="out.pdf"

pathPdftk = "C:\Program Files (x86)\PDFtk\bin\pdftk.exe"
pathWkthml = "bin\wkhtmltopdf.exe"
pathTemplateFile = "AtenaTemplate.htm"

Set FSO = CreateObject("Scripting.FileSystemObject")
Set WShell = CreateObject("WScript.Shell")

'--- 宛名情報を取得
strDairiten="三菱電機株式会社"
strMaker="ルネサステクノロジ 株式会社"

'--- 宛名HTMLを生成する
Set MyFile = FSO.OpenTextFile(pathTemplateFile)
myRec = MyFile.ReadAll
myRec = replace(myRec,"%%TORIHIKISAKI%%", strDairiten)
myRec = replace(myRec,"%%MAKER%%", strMaker)
MyFile.Close
Set MyFile = FSO.CreateTextFile("temp.htm")
MyFile.WriteLine(myRec)
MyFile.Close

'--- 宛名HTMLをPDFに変換する
status = WShell.Run("""" & pathWkthml & """ temp.htm stamp.pdf", 1, True)
If status <> 0 Then Err.Raise 20000, "", "実行中にエラーが発生しました： " & pathWkthml

'--- 宛名をPDFに追加する
status = WShell.Run("""" &  pathPdftk & """ """ &  INPDF & """ stamp stamp.pdf output """ & OUTPDF & """", 1, True)
If status <> 0 Then Err.Raise 20000, "", "実行中にエラーが発生しました： "&  pathPdftk

'--- 中間ファイルを削除
WShell.Run "cmd /c ""del /F temp.htm stamp.pdf""", 1, True

