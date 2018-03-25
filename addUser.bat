
REM ＊＊＊ユーザをリモートグループに追加する＊＊＊
@REM Usage: psexec \\COMPNAME -u USER -p PASS -h -c thisfile networkPassword

@set scr=\\192.168.1.100\share\sadakane\t\addUser.js
@set usr=usersadakane
@set pw=%1

REM スクリプトフォルダに接続
@for %%A in (%scr%) do @set scrDir=%%~dpA
@for %%A in (%scr%) do @set scrFile=%%~nxA
@set scrDir=%scrDir:~0,-1%
net use M: %scrDir% %pw% /user:%usr% /persistent:NO
net use

REM スクリプトを実行
net localgroup Administrators
cscript M:\%scrFile% //nologo
net localgroup Administrators



