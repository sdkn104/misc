
'PC管理用スタートアップスクリプト　(作成：定兼)

On Error Resume Next

'5分ほど待つ
Wscript.Sleep 300000

'共有フォルダのスクリプトを起動する
Set objWShell = CreateObject("Wscript.Shell") 
objWShell.run "cmd /c \\LS-YLA23\share\sadakane\t\test.bat" , vbHide 

