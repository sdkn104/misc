$interface = "イーサネット"

#----- IPv6無効化
Disable-NetAdapterBinding -Name $interface -ComponentID ms_tcpip6
#Enable-NetAdapterBinding -Name $interface -ComponentID ms_tcpip6
Get-NetAdapterBinding -Name $interface -ComponentID ms_tcpip,ms_tcpip6


#----- IPアドレスの設定(address,netmask,gateway)
#netsh interface ip set address "$interface" static $ip 255.255.255.0 192.168..29.1
#netsh interface ip set address "$interface" dhcp 
#netsh interface ip show address "$interface"
Remove-NetIPAddress -InterfaceAlias $interface  -Confirm:$false
#Get-NetRoute
Remove-NetRoute –DestinationPrefix 0.0.0.0/0 –InterfaceAlias $interface –NextHop 192.168.1.1 -Confirm:$false #default gateway削除
Set-NetIPInterface -InterfaceAlias $interface -Dhcp Enable
Set-NetIPInterface -InterfaceAlias $interface -Dhcp Disable
New-NetIPAddress -InterfaceAlias $interface -IPAddress "192.168.1.233"  -PrefixLength 24 -DefaultGateway "192.168.1.1"
Get-NetIPInterface -InterfaceAlias $interface -AddressFamily IPv4 | format-table InterfaceAlias,AddressFamily,Dhcp
Get-NetIPAddress -InterfaceAlias $interface -AddressFamily IPv4 | ft InterfaceAlias,IPAddress,PrefixLength

#----- DNS server
#netsh interface ip set dns "$interface" static 192.168.1.1 register=none
#netsh interface ip add dns "$interface" 192.168.1.122
#netsh interface ip set dns "$interface" dhcp register=none
#netsh interface ip show dns "$interface"
Set-DnsClientServerAddress -InterfaceAlias $interface -ServerAddresses @("192.168.1.1", "8.8.8.8")
Set-DnsClientServerAddress -InterfaceAlias $interface -ResetServerAddresses #DHCP有効ならDNS serverは自動取得となる、無効ならDNS server無しとなる）
Get-DnsClientServerAddress -InterfaceAlias $interface

#------ 終了時に設定を検証する
# ???

#------ インターフェースメトリックを自動に設定する（自動メトリック）
Set-NetIPInterface -InterfaceAlias $interface -AutomaticMetric Enabled
Get-NetIPInterface | ft InterfaceAlias,AutomaticMetric


#--------- DNSサフィックス
#  - 「プライマリDNSサフィックス」：マシン固有。コンピュータ名の変更⇒詳細　で設定する。
#  - 「接続専用のDNSサフィックス（この接続のDNSサフィックス）」：アダプタ毎。アダプタのプロパティで設定。
#  - 「以下のサフィックスを順に追加する」：任意数を順番に指定可能。アダプタによらず共通。
$suffixes = "a.org", "b.org"
$class= [wmiclass]'Win32_NetworkAdapterConfiguration'
$class.SetDNSSuffixSearchOrder($suffixes)
$class.SetDNSSuffixSearchOrder() # ->suffix削除
#reg add HKLM\SYSTEM\CurrentControlSet\services\Tcpip\Parameters /V SearchList /D "aaa.org,bbb.org" /F
reg query HKLM\SYSTEM\CurrentControlSet\services\Tcpip\Parameters /V SearchList
#wmic /:off nicconfig get description,DNSDomain,DNSDomainSuffixSearchOrder
#wmic /interactive:off nicconfig call SetDNSSuffixSearchOrder ("a.org", "b.org")
# 以下の設定により、「以下のDNSサフィックス・・」「プライマリ及び・・」が切り替わる
#Set-DnsClientGlobalSetting -SuffixSearchList @("aaa.org", "bbb.org") 
#Set-DnsClientGlobalSetting -SuffixSearchList @() # ->suffix削除
#Get-DnsClientGlobalSetting | format-table SuffixSearchList

#------ プライマリDNSサフィックスの親サフィックスを追加する
# ???

#--------- この接続(固有)のDNSサフィックス
#wmic /interactive:off nicconfig where index=1 call SetDNSDomain "xxx.org"
Set-DnsClient -InterfaceAlias $interface -ResetConnectionSpecificSuffix
Set-DnsClient -InterfaceAlias $interface -ConnectionSpecificSuffix "xxx.org"
Get-DnsClient -InterfaceAlias $interface | format-table InterfaceAlias,ConnectionSpecificSuffix

#---------- この接続のアドレスをDNSに登録する、この接続のDNSサフィックスをDNS登録に使う
#  ※早めに設定したほうがよい（ＤＮＳにご登録されないため）
#Select-Object -InputObject $nic Description, FullDNSRegistrationEnabled, DomainDNSRegistrationEnabled | Write-Output
Set-DnsClient -InterfaceAlias $interface -RegisterThisConnectionsAddress $false -UseSuffixWhenRegistering $false
Get-DnsClient -InterfaceAlias $interface | format-table InterfaceAlias,*Register*


#----- WINS server
#netsh interface ip set wins "$interface" static 192.168.1.1
#netsh interface ip add wins "$interface" 8.8.8.8
#netsh interface ip set wins "$interface" dhcp
$nic.SetWINSServer("192.168.1.1", "8.8.8.8")
$nic.SetWINSServer("", "") ##DHCP有効ならWINS serverは自動取得となる、無効ならWINS server無しとなる）
netsh interface ip show wins "$interface"

#------ lmhostsの参照を有効にする（アダプタによらず共通）
$nicClass = Get-WmiObject -list Win32_NetworkAdapterConfiguration
$nicClass.enablewins($false,$true)
Get-WmiObject -Class win32_NetworkAdapterConfiguration | ft Description,DNSEnabledForWINSResolution,WINSEnableLMHostsLookup

#---------- netBIOS over TCP/IP
#ネットワークが接続していないとエラーとなる。ＧＵＩからの設定は可能。
$a = Get-NetAdapter -Name $interface
$nic = Get-WmiObject -Class win32_NetworkAdapterConfiguration | Where-Object {$_.Description -eq $a.InterfaceDescription}
$r = $nic.SetTcpipNetbios(1)
$r = $nic.SetTcpipNetbios(0)
#SetTcpopNetbios option:
# 0 - Use NetBIOS setting from the DHCP server
# 1 - Enable NetBIOS over TCP/IP
# 2 - Disable NetBIOS over TCP/IP
#wmic nicconfig get description,TcpipNetbiosOptions
#wmic nicconfig where (IPEnabled=TRUE) call SetTcpipNetbios 1
$nic = Get-WmiObject -Class win32_NetworkAdapterConfiguration | Where-Object {$_.Description -eq $a.InterfaceDescription}
$nic | format-table Description,TcpipNetbiosOptions


#----------- ネットワークの場所（プロファイル）
Set-NetConnectionProfile -InterfaceAlias $interface -NetworkCategory Private
Get-NetConnectionProfile -InterfaceAlias $interface | Format-Table InterfaceAlias,NetworkCategory
