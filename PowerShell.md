- TOP: https://docs.microsoft.com/en-us/powershell/?view=powershell-5.0
- SDK TOP: https://docs.microsoft.com/en-us/powershell/developer/windows-powershell
  - Cmdlet: https://docs.microsoft.com/en-us/powershell/developer/cmdlet/writing-a-windows-powershell-cmdlet
- Ref TOP: https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-5.0
  - Learning PS: https://docs.microsoft.com/en-us/powershell/scripting/learn/understanding-important-powershell-concepts?view=powershell-5.0
  - Core Ref: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/?view=powershell-5.0
  - about Ref (構文）: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/?view=powershell-5.0
- Language Spec. 3.0 (5.0も同じはず)
   https://www.microsoft.com/en-us/download/confirmation.aspx?id=36389

#### Cheat Sheet
- https://cdn.comparitech.com/wp-content/uploads/2018/08/Comparitech-Powershell-cheatsheet.pdf
- https://download.microsoft.com/download/2/1/2/2122F0B9-0EE6-4E6D-BFD6-F9DCD27C07F9/WS12_QuickRef_Download_Files/PowerShell_LangRef_v3.pdf
- 

#### Array
```
$a = 1, 2, 3
$a = @(1)
$a.Count
```
#### Hash
```
$hash = @{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash = [orderd]@{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash.Keys
$hash.Color
$hash["Color"]
$hash[0]
```

#### String
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

#### Location
```
pwd
dir
Get-Item C:\Users\*
```

#### Type
```
$text = [String]123
$number = [int]$a
(get-date) -is [DateTime]
(get-date).GetType()
```
#### Control
```
If(){} Elseif(){ } Else{ }
while(){}
For($i=0; $i -lt 10; $i++){}
Foreach($i in 1..10){$i}
1..10 | foreach{$_}
```

#### File I/O
```
$c = "あいうえお定兼ｻﾀﾞ＠©"
Set-Content t.txt $c  # write
$raw = Get-Content t.txt -Raw  # string
$lines = @(Get-Content t.txt)  # array of line strings
```

#### etc
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
```Read-Host```
```Out-Host```
```Format-Table```
```Format-List```

呼び出し：
```
powershell -ExecutionPolicy ByPass -NoProfile -NoLogo -File .\無題1.ps1
```

#### ダイアログ表示：
```
Add-Type -AssemblyName System.Windows.Forms;
[System.Windows.Forms.MessageBox]::Show("xxxx");
```
```
$WSH = New-Object -ComObject Wscript.Shell
$WSH.Popup("xxxx")
```

#### Powershellスクリプトを起動するVBScript
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

#### BAT内に埋め込んだPSスクリプトを実行
```
@REM <# PowerShellコメントの始まり。@REMを取り除くと全体がPSスクリプトとなる。
@echo off
setlocal enabledelayedexpansion
for %%f in (%*) do ( set ARGS=!ARGS! %%f )
type "%~fp0" | powershell -ExecutionPolicy Unrestricted -NoProfile -NoLogo -Command "'<#'; $input | Select-Object -Skip 1" > %TEMP%\tmp.batps.ps1
powershell -ExecutionPolicy Unrestricted -NoProfile -NoLogo -File %TEMP%\tmp.batps.ps1 %ARGS%
del %TEMP%\tmp.batps.ps1
exit /b
#>
#------- 上のコードは編集しないこと --------------------------------------------------------
#------- ここから下のPowerShellスクリプトが実行される（起動引数は渡される） -------------------

Write-Host $args[0]
```

#### IP SCAN
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

#Nmap使用
$outnmap = nmap 192.168.1.1-100 -sU --script .\nbstat.nse -p137
#$outnmap = nmap 192.168.1.1-10 -sn
$ip = ""
$hosts = foreach( $line in $outnmap) {
  if( $line -match "(Nmap scan report for |Nmap done:)" -and $ip -ne "" ) {    
      "$ip,$mac,$nbname"
  }
  if( $line -match "Nmap scan report for *([0-9.]+)" ) { $ip = $Matches[1]; $mac = $nbname = $dnsname = "" }
  if( $line -match "MAC Address: *([0-9A-Fa-f:]+)" ) { $mac = $Matches[1] }
  if( $line -match "NetBIOS name: *([^ ,]+)" ) { $nbname = $Matches[1]; }
}
```


