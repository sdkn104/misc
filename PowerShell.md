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
"abc.txt" -replace '(.)\.txt$','$1.log'
if( "abc.txt" -match '([abc])\.txt$' ) { $Matches[1] }
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

IP SCAN
```
# IP scanして応答あったもののNetBIOS名取得
ForEach($i in 1..2) {
  $ip = "192.168.1.$i"
  $w = Get-WmiObject Win32_PingStatus -Filter "Address='$ip' and Timeout=100 and ResolveAddressNames='true' and StatusCode=0" | select ProtocolAddress*
  #$w
  if( $w -ne $null ) {
    #$w.GetType()
    $s = nbtstat -a $ip | Select-String "一意" | ForEach-Object { $l = -split $_; $l[0] } | Get-Unique
    $ad = $w.ProtocolAddress
    #リモートのcomputernameを取得
    $host = Invoke-Command -comp $ip -script {$env:computername} -cred $cred

    "$ad $s $host"
  }
}


#ブロードキャストでNetBIOS名を取得し、そのIPアドレスを取得
$names = nbtstat -r | Select-String "<[0-9 ]*>" | foreach { $t = -split $_; $t[0] } | sort | Get-Unique
$names
foreach( $n in $names) {
  nbtstat -a $n > $null
}
nbtstat -c | Select-String "一意" | foreach { $t = -split $_; $t[3]+" "+$t[0] } | sort | Get-Unique 
```