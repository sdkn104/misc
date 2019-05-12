TOP: https://docs.microsoft.com/en-us/powershell/?view=powershell-5.0

SDK TOP: https://docs.microsoft.com/en-us/powershell/developer/windows-powershell

- Cmdlet: https://docs.microsoft.com/en-us/powershell/developer/cmdlet/writing-a-windows-powershell-cmdlet

Ref TOP: https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-5.0

- Learning PS: https://docs.microsoft.com/en-us/powershell/scripting/learn/understanding-important-powershell-concepts?view=powershell-5.0

- Core Ref: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/?view=powershell-5.0

- about Ref (構文）: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/?view=powershell-5.0


Language Spec. 3.0 (5.0も同じはず)
https://www.microsoft.com/en-us/download/confirmation.aspx?id=36389

Array
```
$a = 1, 2, 3
$a = @(1)
$a.Count
```
Hash:
```
$hash = @{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash = [orderd]@{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash.Keys
$hash.Color
$hash["Color"]
$hash[0]
```

Location:
```
pwd
dir
Get-Item C:\Users\*
```

String
```
"a" + "b"
"abc.txt".Replace("txt","log")
"abc.txt" -replace '\.txt$','.log'
if( "abc.txt" -match '\.txt$' ) { "ok" }
if( "abc.txt" -like '*txt' ) { "ok" }
ipconfig | Select-String "イーサネット"
-split "a b c d"
"a:b:c" -split ":"
```

Type
```
(get-date) -is [DateTime]
(get-date).GetType()
```

File I/O
```
$c = "あいうえお定兼ｻﾀﾞ＠©"
Set-Content t.txt $c  # write
$raw = Get-Content t.txt -Raw  # string
$lines = @(Get-Content t.txt)  # array of line strings
```

```cat```
```ps```

```Get-Command -Verb Get ```

```Get-ChildItem -?```   HELP

```Get-Help Get-ChildItem```   HELP

```Get-Alias```


```$files = dir```

```
$d = Get-ChildItem | sort | Where-Object { $_.Name -like "*D*" } | Select-Object Length,Name,Mode
foreach( $i in $d ) { $i }
```
```Select-Object```
```Group-Object```
```Write-Host```
```Out-Host```
```Format-Table```
```Format-List```

呼び出し：
```
powershell -ExecutionPolicy ByPass -NoProfile -File .\無題1.ps1
```

ダイアログ：
```
Add-Type -AssemblyName System.Windows.Forms;
[System.Windows.Forms.MessageBox]::Show("xxxx");
```


Powershellスクリプトを起動するVBScript
```
'
' Powershellスクリプト起動
'   このファイルのファイル名+'.ps1'　のファイルを起動する
'

'引数を取得
args_string = ""
For Each arg In WScript.Arguments
  args_string = args_string & " """ & arg & """"
Next

'ファイル名を取得（このファイルのファイル名+.ps1）
file = WScript.ScriptFullName + ".ps1"

'ＰＳ起動コマンドラインを作成
cmd = "cmd /c powershell -ExecutionPolicy ByPass -NoProfile -File "
cmdall = cmd & """" & file & """" & args_string ' & " > C:\Users\sdkn1\Desktop\o.txt"
'Wscript.echo cmdall

'実行
Set SH = WScript.CreateObject("WScript.Shell")
SH.Run cmdall, 0, True
```

