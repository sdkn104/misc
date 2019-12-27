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
#### String
```
"abc"            # string
'abc $a'         # string
"abc ${a}"       # embedded var.
"abc $($a+1)"    # embedded expr.
"{0} {1}" -f 1,"ab" # format operator
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
foreach ($key in $hash.Keys) { $hash[$key] }
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
#### Function
```
function add($a, $b) { $a + $b }
$v = add 1 2
```
#### Pileline
```
$d = Get-ChildItem | sort | where { $_.Name -like "*D*" } | Select-Object Length,Name,Mode -Last 5
$d | foreach { "name: " + $_.Name }
dir | Group-Object Extension
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
   $emsg = $_ | Out-String  # 長いデフォルトのメッセージ
   Out-Host "error: $($_|Out-String)"
   $emsg = $_.Exception.Message　   # 短いメッセージ
   $emsg = $_.InvocationInfo.PositionMessage  # 発生場所
   $emsg = $_.ScriptStackTrace #短い発生場所
   $emsg = $_.CategoryInfo.ToString() #エラーカテゴリ名
   Write-Host $_                                                 # 簡略表示
   Out-Host -InputObject $_                                      # メッセージを表示
   Out-String -InputObject $_ | Write-Host -ForegroundColor Red　# メッセージを赤色で表示
   throw $_    　    # terminating errorを発生
   exit 1            # default exit code = 0
} finally {
}
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
```
* PowerShellでオブジェクトは原則　Format-* により表示の書式を設定、Out-* により最終出力、の手順を踏み何らかの表示や出力がなされます。
* Out-Host,File,String.. は、input streamまたは-inputObjectから入力をとり、それぞれに出力する。
#### File I/O
```
$c = "あいうえお定兼ｻﾀﾞ＠©"
Set-Content t.txt $c -ENcoding UTF8  # write
echo xxx | Set-Content t.txt
echo xxx | Out-File t.txt -Encoding UTF8
$raw = Get-Content t.txt -Raw  # string
$lines = @(Get-Content t.txt)  # array of line strings
```
ーーーーーーーーーーーーーーーー
* Get-Content xxx.txt -Encoding xxx
   日本語PowerShellの場合、Get-ContentはUTF16、SJIS、UTF8(BOMあり）のテキストファイルを読み取れる。
   それら以外のファイルを読み込むには-Encodingオプションで文字コードを指定する。PS6未満ではUTF8Nは読めない。
   -Encoding Defaultと指定するとSJISを指定する事になる。

* Set-Content xxx.txt -Encoding xxx :  デフォルトはDefault (=SJIS)
* Out-File xxx.txt -Encoding xxx : デフォルトはDefault (=UTF16)
* redirect ">"  : UTF16。文字コード指定不可。

•Set-Contentはデフォルトの文字コードであるSJISで書き出される。
•Out-Fileは内部文字コードであるUTF16で書き出される。

#### File System
```
pwd (Get-Location)
cd (Set-Location)
dir (Get-ChildItem)
Get-ChildItem -Include *.txt -Recurse | foreach { $_.FullName }
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
#### 外部コマンド
```
$log = & "C:\program file.exe" "arg 1" "arg2" arg3
if( -not $? ) { throw "ERROR in external command." } 
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
CMD> powershell -ExecutionPolicy ByPass -NoProfile -NoLogo -File .\無題1.ps1
```
```
PS> Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser  #管理者として実行したPowershellで。
# -> ps1ファイルを右クリックし「Powershellで実行」で実行できる
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
#### MS Office
```
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $true
$excel.DisplayAlerts = $true
$book = $excel.Workbooks.Add()
$book.ActiveSheet.Name
$book.Close()
$excel.Quit()
# to kill process
[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($book)
[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel)  
```
#### BATファイル内にPowerShellスクリプトを埋め込む
本スクリプトは.batフィアルとして保存して実行できる。
```
@(echo ' ) >nul
@set f="%TEMP%\tmp.batps.%DATE:/=%%TIME::=%%RANDOM%.ps1"
@set /p d=$PSCommandPath="%~fp0";<nul  > "%f%"
@type "%~fp0"                         >> "%f%"
@powershell -ExecutionPolicy Unrestricted -NoProfile -NoLogo -File "%f%" %*
@set c=%errorlevel% & del "%f%" 
@exit /b %c%
') > $null
#--------- 上のスクリプトはここから下のPowershellコードを実行する（起動引数は渡される）-------------
# 制限事項：
#   自身のスクリプトパス名は $PSCommandPath で参照する（$PSScriptRoot, $MyInvocationは使えない）。
#   自身のスクリプトパス名に`および$を含まないこと。このスクリプトはShiftJIS(cp932)で保存すること。
#---------------------------------------------------------------------------------------------------

function MyExit($code) { Read-Host "終了するにはEnterキーを押してください"; exit $code }
trap { Write-Host "【想定外のエラーが発生したので終了します】"; Out-Host -InputObject $_; MyExit 1 }

cd (Split-Path $PSCommandPath -Parent)
Write-Host $args[0]
Write-Host $args[1]
Write-Host $args[2]

#throw "error...."
MyExit 0
```
* PowerShellからのリターンコード(exit nで指定)はBATの戻り値となる。
* 本スクリプトはBATファイルとしてもpowerShellスクリプトとしても正しいコード。(ファイル名は.batでも.ps1でも実行可)
* 上記３行目を以下で置き換えれば、スクリプトをUTF8(BOM付)で保存しても実行可。ただし先頭行のBAT実行時にエラーメッセージがでる。
`@powershell -ExecutionPolicy Unrestricted -NoProfile -NoLogo -Command "$t='%TEMP%\tmp.batps.ps1'; $a=(gc $t)+(gc '%~fp0' -Raw); sc $t $a -Encoding UTF8"`
* cmd.exeは先頭から@exitまでを実行して終了。本スクリプト自身の先頭行を修正したものを.ps1ファイルとして保存してpowershell.exeで実行。
* powershell.exeは、先頭から') > $nullまでをnullへのechoとして実行する(読み飛ばすのに等しい)。
* powershellはshiftjis(cp932), utf8(bom付), (とunicode??)のスクリプトを許す。IDE, VS codeはデフォルトutf8(bom)のはず。
* BATスクリプトは、shiftjis(cp932)のみ許す。utf8(bom)では先頭のBOMのところでエラー、メッセージを出すが処理は続行。
 ---------------------------------------------
 
 
#### JScriptファイル内にPowerShellスクリプトを埋め込む
本スクリプトは.jsフィアルとして保存して実行できる。
```
"\" >$null <# "
var SH = new ActiveXObject("WScript.Shell"); var FSO = new ActiveXObject("Scripting.FileSystemObject");
SH.Environment("Process").Item("_PSCommandPath_") = WScript.ScriptFullName;
var arg = ""; for(var i=0; i<WScript.Arguments.length; i++) { arg += ' "' + WScript.Arguments(i).replace(/\\$/,"\\\\") + '"' }
var tf = FSO.GetSpecialFolder(2).Path+"\\tmp.jsps" + (new Date).getTime() + Math.floor(Math.random()*100) + ".ps1"
FSO.CopyFile(WScript.ScriptFullName, tf, true);
var r = SH.Run("cmd /c powershell -ExecutionPolicy ByPass -NoProfile -File " + tf + arg, 1, true)
FSO.DeleteFile(tf, true); WScript.Quit(r);
/* #>; $PSCommandPath = $env:_PSCommandPath_;
#--------- 上のスクリプトはここから下のPowershellコードを実行する（起動引数は渡される）-------------
# 制限事項：
#   自身のスクリプトパス名は $PSCommandPath で参照する（$PSScriptRoot, $MyInvocationは使えない）。
#   このスクリプトはShiftJIS(cp932)で保存すること。引数に'"'、引数末尾に'\\' を含まないこと。
#---------------------------------------------------------------------------------------------------

function MyExit($code) { Read-Host "終了するにはEnterキーを押してください"; exit $code }
trap { Write-Host "【想定外のエラーが発生したので終了します】"; Out-Host -InputObject $_; MyExit 1 }

cd (Split-Path $PSCommandPath -Parent)
Write-Host $args[0]
Write-Host $args[1]
Write-Host $args[2]

throw "error...."
MyExit 0
# --------- PowrShellスクリプトの終わり ----------- */
```
* PowerShellからのリターンコード(exit nで指定)はJScriptの戻り値となる。
* 本スクリプトはJScriptファイルとしてもpowerShellスクリプトとしても正しいコード。(ファイル名は.jsでも.ps1でも実行可)
* JScriptスクリプトは、shiftjis(cp932)のみ許す。utf8は不可。
* ウィンドウ非表示にしたいときは、Shell.Runの第二引数を0とする。
* バックグラウンド（Powershell起動後するにJScriptを終了）とするには、Shell.Runの第3引数をfalseとする。
  (このときexitコードは常に０となる)
* wscript/cscript.exeは先頭からWScript.Quit(r)までを実行して終了（そこから後ろはコメントと解釈）。
　本スクリプト自身を.ps1ファイルにコピーしてpowershell.exeで実行。
* powershell.exeは、先頭の<#から#>までをコメントと解釈。スクリプト自身のパス名は環境変数を介して引き渡される。
* powershellはshiftjis(cp932), utf8(bom付), (とunicode??)のスクリプトを許す。IDE, VS codeはデフォルトutf8(bom)のはず。

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


