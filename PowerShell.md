#### References
- Ref TOP: https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-5.0
  - Learning PS: https://docs.microsoft.com/en-us/powershell/scripting/learn/understanding-important-powershell-concepts?view=powershell-5.0
  - Core Ref: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/?view=powershell-5.0
  - about Ref (構文）: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/?view=powershell-5.0
- Language Spec. 3.0 (5.0も同じはず)
   https://www.microsoft.com/en-us/download/confirmation.aspx?id=36389
- SDK TOP: https://docs.microsoft.com/en-us/powershell/developer/windows-powershell
  - Cmdlet: https://docs.microsoft.com/en-us/powershell/developer/cmdlet/writing-a-windows-powershell-cmdlet

#### Cheat Sheet
- https://cdn.comparitech.com/wp-content/uploads/2018/08/Comparitech-Powershell-cheatsheet.pdf
- https://download.microsoft.com/download/2/1/2/2122F0B9-0EE6-4E6D-BFD6-F9DCD27C07F9/WS12_QuickRef_Download_Files/PowerShell_LangRef_v3.pdf
- 

#### Basic litral
```
$true, $false    # Boolean constant
$null            # default value of all the variable
```
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
"abc"            # string
'abc $a'         # string
"abc ${a}"  # embedded var.
"abc $($a+1)"    # embedded expr.
"`r`n"           # CRLF
"a" + "b"
"abcde".Substring(3,4)
"abc.txt".Replace("txt","log")
"abc.txt" -replace '(.)\.txt$','$1.log'
if( "abc.txt" -match '([abc])\.txt$' ) { $Matches[1] }
if( "abc.txt" -like '*txt' ) { "ok" }
ipconfig | Select-String "イーサネット"
-split "a b c d"
"a:b:c" -split ":"
```
#### Type
```
$text = [String]123    # cast
$number = [int]$a      # cast
[string]$string = 123  # type declaration
(get-date) -is [DateTime]
(get-date).GetType()
```
#### Control
```
if() {} elseif() { } else { }
for($i=0; $i -lt 10; $i++) { continue; break; }
foreach($i in 1..10) { $i }
1..10 | foreach{$_}
while() {}
do {} while()
do {} until()
```
#### 例外処理
```
$ErrorActionPreference = "Stop"  # non-terminatig errorでも実行停止しcatchする。
trap { # 処理されなかったすべてのterminating errorに対して
  Write-Host "想定外のエラーが発生しました。終了します。"
  Out-Host -InputObject $_
  exit 1 
}
try {
   dir "asdfaf"  # non-terminating error
   dasfdasfsa    # terminating error
   throw "this is an error."  # terminating error
} catch {
   Write-Host $_                                                 # 簡略表示
   Out-Host -InputObject $_                                      # メッセージを表示
   Out-String -InputObject $_ | Write-Host -ForegroundColor Red　# メッセージを赤色で表示
   throw $_    　    # terminating errorを発生
   exit 1            # default exit code = 0
} finally {
}
```
#### Function
```
function add($a, $b) { $a + $b }
$v = add 1 2
```
#### Script Args, Path
```
echo $PSCommandPath  # full path of this script
echo $args[0]        # the first argument 
echo $args[1]        # the second
```
#### 入出力 (Host, Stream)
```
$age = Read-host "Please enter your age: "
Write-Host "abc"   # console terminalへの出力
Write-Output "abc" # standard output streamへの出力（パイプできる、object streamである）
Write-Error "abc"  # non-terminating errorを発生し、error output streamへ出力
# PowerShellでオブジェクトは原則　Format-* により表示の書式を設定、Out-* により最終出力、の手順を踏み何らかの表示や出力がなされます。
```
#### Pileline
```
$d = Get-ChildItem | sort | where { $_.Name -like "*D*" } | Select-Object Length,Name,Mode -Last 5
$d | foreach { "name: " + $_.Name }
dir | Group-Object Extension
```
#### File I/O
```
$c = "あいうえお定兼ｻﾀﾞ＠©"
Set-Content t.txt $c  # write
$raw = Get-Content t.txt -Raw  # string
$lines = @(Get-Content t.txt)  # array of line strings
```
#### File System
```
pwd (Get-Location)
cd (Set-Location)
dir (Get-ChildItem)
Get-ChildItem -Recurse -Include *.txt
Get-Item C:\Users\*
cp (Copy-Item)
mv (Move-Item)
rm (Remove-Item)
mkdir xxx (New-Item xxx -ItemType Directory)
if( Test-Path ".\a\b.*" ) { rm ".\a\b.*" }
```
#### File Path
```
Split-Path "C:\aaa\bbb\ccc" -Parent
Split-Path "C:\aaa\bbb\ccc" -Leaf
Convert-Path ".\abc.txt"     # --> C:\Users\xxx\Desktop\abc.txt
Convert-Path .\*.txt         # list up matched files in full path
```
#### Help
```
Update-Help  # download and install help files, 管理者権限で実行
Get-Command *-Host*
Get-ChildItem -?
Get-Help Get-ChildItem -Online
alias (Get-Alias)
```
#### Custom Object
```
# create object
$obj1 = New-Object PSCustomObject
$obj1 | Add-Member -MemberType NoteProperty -Name "Name" -Value "Tom"
$obj1 | Add-Member -MemberType NoteProperty -Name "Age" -Value 29
# create by hash
$props1 = @{ "Name" = "Tom"; "Age" = 29; }
$obj1 = New-Object PSCustomObject -Property $props1
$obj1 = [PSCustomObject] $props1
# object array
$hashArray1 = (
    @{ "Name" = "Tom"; "Age" = 29; },
    @{ "Name" = "Jack"; "Age" = 19; }
)
$objArray = $hashArray1 | foreach { [PSCustomObject]$_ }
```

#### 外部コマンド
```
$log = & "C:\program file.exe" "arg 1" "arg2" arg3
if( -not #? ) { throw "ERROR in external command." } 
$success = $?            # 外部コマンドの場合、戻り値非０のときFalse、外部コマンド内でWindowsコマンドエラー発生もFalse。
$code = $LastExitCode    # 戻り値（外部コマンドの場合のみ）
# Exception: 戻り値０でもExceptionは発生しない。
#            外部コマンド内で実行されたWindowsコマンドのエラーについてはNon terminatingまたはTerminating errorが発生する場合あり。
```
#### Format
```
Format-Table
Format-List
```
#### 起動
```
powershell -ExecutionPolicy ByPass -NoProfile -NoLogo -File .\無題1.ps1
```
#### ダイアログ表示
```
Add-Type -AssemblyName System.Windows.Forms;
[System.Windows.Forms.MessageBox]::Show("xxxx");
```
```
$WSH = New-Object -ComObject Wscript.Shell
$WSH.Popup("xxxx")
```
#### DATE
```
Get-Date
[DateTime]"2013/02/09 13:59:50"
[DateTime]::ParseExact("20130209","yyyyMMdd",$null)
(Get-Date).ToString("yyyyMMdd-HH:mm:ss")
(Get-Date).Day
(Get-Date).AddMonths(2)
$span = (Get-Date) - [DateTime]"2019/06/09"
$span.TotalDays
```
#### MS Office
```
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $true
$excel.DisplayAlerts = $true
$book = $excel.Workbooks.Add()
$book.ActiveSheet.Name
$book.Close()
$excel.Quit()   #???
```
#### BAT内に埋め込んだPSスクリプトを実行
(スクリプトファイル名.batでも.ps1でも実行可)
```
@(echo ' ) >nul
@set /p d=$PSCommandPath="%~fp0";<nul  > %TEMP%\tmp.batps.ps1
@type "%~fp0"                         >> %TEMP%\tmp.batps.ps1
@powershell -ExecutionPolicy Unrestricted -NoProfile -NoLogo -File %TEMP%\tmp.batps.ps1 %*
@set c=%errorlevel% & del %TEMP%\tmp.batps.ps1
@exit /b %c%
') > $null
#--------- 上のスクリプトはここから下のPowershellコードを実行する（起動引数は渡される）-------------
# 制限事項：
#   自身のスクリプトパス名は $PSCommandPath で参照する（$PSScriptRoot, $MyInvocationは使えない）。
#   自身のスクリプトパス名に`および$を含まないこと。
#---------------------------------------------------------------------------------------------

function MyExit($code) { Read-Host "終了するにはEnterキーを押してください"; exit $code }
trap { Write-Host "【想定外のエラーが発生したので終了します】"; Out-Host -InputObject $_; MyExit 1 }

Write-Host $PSCommandPath
Write-Host $args[0]
Write-Host $args[1]
Write-Host $args[2]

throw "error...."
MyExit 0
```
 
 ---------------------------------------------
 
 
#### Powershellスクリプトを起動するVBScript
```
' Powershellスクリプト起動
'   このファイルのファイル名+'.ps1'　のファイルを起動する
`
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


