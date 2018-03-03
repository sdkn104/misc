
FOR /F "delims=^^^" %%i in ('ver') do set V=%%i
echo %DATE%,%TIME%,%COMPUTERNAME%,%USERNAME%,OSVERSION,%V%

REM --- install -----------
net use
net use /PERSISTENT:NO
net use N: \\192.168.1.100\share\sadakane\HOKAN\その他
net use
cd /d N:\
install.bat

REM --- user account ----
net user
net user Toshiyuki
net localgroup
net localgroup Administrators
net localgroup Administrators Toshiyuki /add

REM --- WiFi -------- https://blog.cles.jp/item/7660
netsh wlan show profiles
netsh wlan show profiles name=HomeSSID key=clear
netsh wlan export profile HomeSSID

netsh wlan add profile filename="\\FILSVR\Share\Wi-Fi-HomeSSID.xml" user=all
netsh wlan set profileparameter name=HomeSSID keymaterial=12345678abc

REM -------------
SET F=0
if %COMPUTERNAME%==LENOVO-PC SET F=1
if %COMPUTERNAME%==LENOVO-PC SET F=1
if %COMPUTERNAME%==LENOVO-PC SET F=1
if %F%==1 (
   date /t
)
