
net use
net use /PERSISTENT:NO
net use Y: \\192.168.1.100\share\sadakane\HOKAN\その他
net use
dir Y:


FOR /F "delims=^^^" %%i in ('ver') do set VVV=%%i
echo %VVV%

net user
net user Toshiyuki
net localgroup
net localgroup Administrators
net localgroup Administrators Toshiyuki /add

netsh wlan show profiles
netsh wlan show profiles name=SSID
netsh wlan show profiles name=SSID key=clear #key表示


REM https://blog.cles.jp/item/7660
netsh wlan show profiles name=HomeSSID key=clear
netsh wlan export profile HomeSSID

netsh wlan add profile filename="\\FILSVR\Share\Wi-Fi-HomeSSID.xml" user=all
netsh wlan set profileparameter name=HomeSSID keymaterial=12345678abc
