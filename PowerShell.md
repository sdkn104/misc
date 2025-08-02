## References
- Ref TOP: https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-5.0
  - Learning PS: https://docs.microsoft.com/en-us/powershell/scripting/learn/understanding-important-powershell-concepts?view=powershell-5.0
  - Core Ref: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/?view=powershell-5.0
  - about Ref (構文）: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/?view=powershell-5.0
- Language Spec. 3.0 (5.0も同じはず)
   https://www.microsoft.com/en-us/download/confirmation.aspx?id=36389
- SDK TOP: https://docs.microsoft.com/en-us/powershell/developer/windows-powershell
  - Cmdlet: https://docs.microsoft.com/en-us/powershell/developer/cmdlet/writing-a-windows-powershell-cmdlet

## Cheat Sheet
- https://cdn.comparitech.com/wp-content/uploads/2018/08/Comparitech-Powershell-cheatsheet.pdf
- https://download.microsoft.com/download/2/1/2/2122F0B9-0EE6-4E6D-BFD6-F9DCD27C07F9/WS12_QuickRef_Download_Files/PowerShell_LangRef_v3.pdf
- 

## Basic litral
```Powershell
$true, $false    # Boolean constant
$null            # default value of all the variable
```
## String
```Powershell
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
## Array
```Powershell
$a = 1, 2, 3
$a = @(1)
$a.Count
```
## Hash
```Powershell
$hash = @{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash = [orderd]@{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash.Keys
$hash.Color
$hash["Color"]
$hash[0]
foreach ($key in $hash.Keys) { $hash[$key] }
```
## Custom Object
```Powershell
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
## DATE
```Powershell
Get-Date
[DateTime]"2013/02/09 13:59:50"
[DateTime]::ParseExact("20130209","yyyyMMdd",$null)
(Get-Date).ToString("yyyyMMdd-HH:mm:ss")
(Get-Date).Day
(Get-Date).AddMonths(2)
$span = (Get-Date) - [DateTime]"2019/06/09"
$span.TotalDays
```

## Type
```Powershell
$text = [String]123    # cast
$number = [int]$a      # cast
[string]$string = 123  # type declaration
(get-date) -is [DateTime]
(get-date).GetType()
```
## Format, Property
```Powershell
dir | Select-Object [-Property] Name,Length
dir | Select-Object [-Property] *
dir | Format-Table -AutoSize [-Property] Name,Length
dir | Format-List [-Property] Name,Length
```

## Control
```Powershell
if() {} elseif() { } else { }
for($i=0; $i -lt 10; $i++) { continue; break; }
foreach($i in 1..10) { $i }
1..10 | foreach{$_}
while() {}
do {} while()
do {} until()
```
## Function
```Powershell
function add($a, $b) { $a + $b }
$v = add 1 2
```
## Pileline
```Powershell
$d = Get-ChildItem | sort | where { $_.Name -like "*D*" } | Select-Object Length,Name,Mode -Last 5
$d | foreach { "name: " + $_.Name }
dir | Group-Object Extension
```
## Exception
```Powershell
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
## Script Args, Path
```Powershell
echo $PSCommandPath  # full path of this script
echo $args[0]        # the first argument 
echo $args[1]        # the second
```
## I/O (Host, Stream)
```Powershell
$age = Read-host "Please enter your age: "
Write-Host "abc"   # console terminalへの出力
Write-Output "abc" # standard output streamへの出力（パイプできる、object streamである）
Write-Error "abc"  # non-terminating errorを発生し、error output streamへ出力
```
* PowerShellでオブジェクトは原則　Format-* により表示の書式を設定、Out-* により最終出力、の手順を踏み何らかの表示や出力がなされます。
* Out-Host,File,String.. は、input streamまたは-inputObjectから入力をとり、それぞれに出力する。
## File I/O

```Powershell
$c = "あいうえおABC＠©"
Set-Content t.txt $c -ENcoding UTF8  # write
echo xxx | Set-Content t.txt
echo xxx | Out-File t.txt -Encoding UTF8
$raw = Get-Content t.txt -Raw  # string
$lines = @(Get-Content t.txt)  # array of line strings
```
* Get-Content xxx.txt -Encoding xxx
   日本語PowerShellの場合、Get-ContentはUTF16、SJIS、UTF8(BOMあり）のテキストファイルを読み取れる。
   それら以外のファイルを読み込むには-Encodingオプションで文字コードを指定する。PS6未満ではUTF8Nは読めない。
   -Encoding Defaultと指定するとSJISを指定する事になる。

* Set-Content xxx.txt -Encoding xxx :  デフォルトはDefault (=SJIS)
* Out-File xxx.txt -Encoding xxx : デフォルトはDefault (=UTF16)
* redirect ">"  : UTF16。文字コード指定不可。

* utf8nでファイル出力　ただし、ps6.0以降では不要。

```Powershell
  … | Out-String `
    | % { [Text.Encoding]::UTF8.GetBytes($_) } `
    | Set-Content -Path ".\BOMlessUTF8.txt" -Encoding Byte
```

    
## File System
```Powershell
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
## File Path
```Powershell
Split-Path "C:\aaa\bbb\ccc" -Parent
Split-Path "C:\aaa\bbb\ccc" -Leaf
Convert-Path ".\abc.txt"     # --> C:\Users\xxx\Desktop\abc.txt
Convert-Path .\*.txt         # list up matched files in full path
```
## Startup
```Powershell
CMD> powershell -ExecutionPolicy ByPass -NoProfile -NoLogo -File .\無題1.ps1
```
```
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser  #管理者として実行したPowershellで。
# -> ps1ファイルを右クリックし「Powershellで実行」で実行できる
```

## Profile (init file)
#### Create profile File (first time)
```Powershell
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}
notepad $PROFILE
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
#### Sample Profile File
```powershell
function wc( [string]$Path ) {
  <#
  .SYNOPSIS
  wc <File Path>
  cat <File Path> | wc
  .DESCRIPTION
  Print number of lines, words and charactors.
  Equivalent to:
    cat <FilePath> | Measure-Object -Line -Word -Character
  #>
   if( $Path ) {
     Get-Content $Path | Measure-Object -Line -Word -Character
   } else {
     $input | Measure-Object -Line -Word -Character
   }
}
function head( [string]$Path ) {
  <#
	.SYNOPSIS
	head <File Path>
	cat <File Path> | head
  .DESCRIPTION
  Print the first 10 lines/objects.
  Equivalent to:
    cat <File Path> -Head 10
    cat <File Path> | Select-Object -First 10
  #>
   if( $Path ) {
     Get-Content $Path -Head 10
   } else {
     $input | Select-Object -First 10
   }
}
function tail( [string]$Path ) {
  <#
	.SYNOPSIS
	tail <File Path>
	cat <File Path> | tail
  .DESCRIPTION
  Print the last 10 lines/objects.
  Equivalent to:
    cat <File Path> -Tail 10 [-Wait]
    cat <File Path> | Select-Object -Last 10 [-Wait]
  #>
  if( $Path ) {
    Get-Content $Path -Head 10
  } else {
    $input | Select-Object -First 10
  }
}
function difff( [string]$file1, [string]$file2 ) {
  <#
	.SYNOPSIS
	difff file1 file2
  .DESCRIPTION
  Compare two files.
  Equivalent to:
    diff (cat file1) (cat file2)
  #>
  Compare-Object (cat $file1) (cat $file2)
}

function printenv() {
  <#
  .SYNOPSIS
  Print environment variables.  
  .DESCRIPTION
  Equivalent to:
    ls env:
  #>
  Get-ChildItem env:
}  

Set-Alias grep Select-String
Set-Alias uniq Group-Object

# 出力表示時、要素が多くても省略しない
$FormatEnumerationLimit = -1

# windowのバッファ幅変更（画面表示、リダイレクトで折り返さない）
$bufferSize = (Get-Host).UI.RawUI.BufferSize
$bufferSize.Width = 1999
##$bufferSize.Height = 1000
#(Get-Host).UI.RawUI.BufferSize = $bufferSize
```


## Help
```Powershell
Update-Help  # download and install help files, 管理者権限で実行
Get-Command *-Host*
Get-ChildItem -?
Get-Help Get-ChildItem -Online
alias (Get-Alias)
```
## 外部コマンド
```Powershell
$log = & "C:\program file.exe" "arg 1" "arg2" arg3
if( -not $? ) { throw "ERROR in external command." } 
$success = $?            # 外部コマンドの場合、戻り値非０のときFalse、外部コマンド内でWindowsコマンドエラー発生もFalse。
$code = $LastExitCode    # 戻り値（外部コマンドの場合のみ）
# Exception: 戻り値０でもExceptionは発生しない。
#            外部コマンド内で実行されたWindowsコマンドのエラーについてはNon terminatingまたはTerminating errorが発生する場合あり。
```


## ダイアログ表示 dialog
```Powershell
Add-Type -AssemblyName System.Windows.Forms;
[System.Windows.Forms.MessageBox]::Show("xxxx");
```
```Powershell
$WSH = New-Object -ComObject Wscript.Shell
$WSH.Popup("xxxx")
```
```Powershell
[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.VisualBasic')
$No= [Microsoft.VisualBasic.Interaction]::InputBox("番号を入力してください", "タイトル", "初期値")
```

## HTTP Request
```Powershell
$response = Invoke-WebRequest [-Method GET] http://localhost/index.htm [-OutFile out.htm]
$response.StatusCode
$response.Header
$response.Content
```

## MS Office
```Powershell
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
## BATファイル内にPowerShellスクリプトを埋め込む
本スクリプトは.batフィアルとして保存して実行できる。
```bat
@(echo ' ) >nul
@for %%i in (%TEMP%) do @set f="%%~fpi\tmp.batps.%DATE:/=%%TIME::=%%RANDOM%.ps1"
@set /p d=$PSCommandPath="%~fp0";<nul  > %f% & @type "%~fp0" >> %f%
@powershell -ExecutionPolicy Unrestricted -NoProfile -NoLogo -File %f% %*
@set c=%errorlevel% & del %f%
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
* 仕様
  * BATの引数はPowerShellの引数となる。
  * PowerShellからのリターンコード(exit nで指定)はBATの戻り値となる。
  * 本スクリプトはBATファイルとしてもpowerShellスクリプトとしても正しいコード。(ファイル名は.batでも.ps1でも実行可)
  * スクリプトファイルはShift_JISとすること。
  * スクリプトファイルパス名は、空白、全角文字、特殊文字を含んでも可。ただし$, `などPowershellの""引用内での特殊文字は不可。
  * %TEMP%は、空白、非ASCII、特殊文字を含んでもよいが、Powershellのファイルパスの[ワイルドカード](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_wildcards)として使用される文字({}`$)は不可。
  * 引数は、空白、非ASCII、特殊文字を含んでよい(ASCII printable, SPACEは可)。

* 上記３行目を以下で置き換えれば、スクリプトをUTF8(BOM付)で保存しても実行可。ただし先頭行のBAT実行時にエラーメッセージがでる。
`@powershell -ExecutionPolicy Unrestricted -NoProfile -NoLogo -Command "$t='%TEMP%\tmp.batps.ps1'; $a=(gc $t)+(gc '%~fp0' -Raw); sc $t $a -Encoding UTF8"`

* 情報
  * cmd.exeは先頭から@exitまでを実行して終了。本スクリプト自身の先頭行を修正したものを.ps1ファイルとして保存してpowershell.exeで実行。
  * powershell.exeは、先頭から') > $nullまでをnullへのechoとして実行する(読み飛ばすのに等しい)。
  * powershellはshiftjis(cp932), utf8(bom付), (とunicode??)のスクリプトを許す。IDE, VS codeはデフォルトutf8(bom)のはず。
  * BATスクリプトは、shiftjis(cp932)のみ許す。utf8(bom)では先頭のBOMのところでエラー、メッセージを出すが処理は続行。
  * powershell.exe -File - とすると、スクリプト内で標準入力の機能が使えなくなる。
  * powershell.exe -Command とすると、引数の"a b"が扱えない。
  * ASCII printable chars: !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
  * Windows File Naming: https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
 
```bat
@powershell -c '$PSCommandPath=\"%~fp0\" #'+(Get-Content \"%~f0\" -Raw) ^| Invoke-Expression & exit /b
#--------- 上のスクリプトはここから下のPowershellコードを実行する ------------------------------------
# 制約：実行引数は渡らない、exitコードは返らない、$PSScriptRoot, $MyInvocationは使えない。
#       自身のスクリプトパス名に特殊文字を含まないこと。このスクリプトはShiftJIS(cp932)で保存すること。
#-----------------------------------------------------------------------------------------------------

"Time: $([DateTime]::Now)"
"Guid: $([guid]::NewGuid())"
```
* 制約事項
  * BATのコマンドライン引数はpowershellに渡らない
  * $PSCommandPath, $PSScriptRoot, $MyInvocationは使用不可
  * powershellのexit codeはBATのexit codeに戻らない
  * BATのスクリプトファイルのパス名に特殊文字を含んではならない。（特殊文字：%など？？？）

## IP SCAN
```Powershell
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


