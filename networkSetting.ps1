$interface = "イーサネット"

#----- IPv6無効化
Disable-NetAdapterBinding -Name $interface -ComponentID ms_tcpip6
#Enable-NetAdapterBinding -Name $interface -ComponentID ms_tcpip6
Get-NetAdapterBinding -Name $interface -ComponentID ms_tcpip,ms_tcpip6

#----- IPアドレスの設定(address,netmask,gateway)
Remove-NetIPAddress -InterfaceAlias $interface  -Confirm:$false
#Get-NetRoute
Remove-NetRoute –DestinationPrefix 0.0.0.0/0 –InterfaceAlias $interface –NextHop 192.168.1.1 -Confirm:$false #default gateway削除
Set-NetIPInterface -InterfaceAlias $interface -Dhcp Enable
Set-NetIPInterface -InterfaceAlias $interface -Dhcp Disable
New-NetIPAddress -InterfaceAlias $interface -IPAddress "192.168.1.233"  -PrefixLength 24 -DefaultGateway "192.168.1.1"
Get-NetIPInterface -InterfaceAlias $interface -AddressFamily IPv4 | format-table InterfaceAlias,AddressFamily,Dhcp
Get-NetIPAddress -InterfaceAlias $interface -AddressFamily IPv4 | ft InterfaceAlias,IPAddress,PrefixLength

#----- DNS server
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
#wmic /interactive:off nicconfig get index,description,DNSDomain,DNSDomainSuffixSearchOrder
#$class= [wmiclass]'Win32_NetworkAdapterConfiguration'
#$class.SetDNSSuffixSearchOrder()
#reg add HKLM\SYSTEM\CurrentControlSet\services\Tcpip\Parameters /V SearchList /D "ad.melco.co.jp,mei.ad.melco.co.jp" /F
# 以下の設定により、「以下のDNSサフィックス・・」「プライマリ及び・・」が切り替わる
Set-DnsClientGlobalSetting -SuffixSearchList @("ad.melco.co.jp", "mei.ad.melco.co.jp") 
Set-DnsClientGlobalSetting -SuffixSearchList @() # ->suffix削除
Get-DnsClientGlobalSetting | format-table SuffixSearchList

#------ プライマリDNSサフィックスの親サフィックスを追加する
# ???

#--------- この接続(固有)のDNSサフィックス
#wmic /interactive:off nicconfig where index=1 call SetDNSDomain "ad.melco.co.jp"
Get-DnsClient -InterfaceAlias $interface | format-table InterfaceAlias,ConnectionSpecificSuffix
Set-DnsClient -InterfaceAlias $interface -ResetConnectionSpecificSuffix
Set-DnsClient -InterfaceAlias $interface -ConnectionSpecificSuffix "ad.melco.co.jp"

#---------- この接続のアドレスをDNSに登録する
#---------- この接続のDNSサフィックスをDNS登録に使う
Get-DnsClient -InterfaceAlias $interface | format-table InterfaceAlias,*Register*
#Select-Object -InputObject $nic Description, FullDNSRegistrationEnabled, DomainDNSRegistrationEnabled | Write-Output
Set-DnsClient -InterfaceAlias $interface -RegisterThisConnectionsAddress $false -UseSuffixWhenRegistering $false

#----- WINS server
netsh interface ip set wins $interface static 192.168.1.1
netsh interface ip add wins $interface 8.8.8.8
netsh interface ip set wins $interface dhcp
#$nic.SetWINSServer("192.168.1.1", "8.8.8.8")
#$nic.SetWINSServer("", "") ##DHCP有効ならWINS serverは自動取得となる、無効ならWINS server無しとなる）
netsh interface ip show wins

#------ lmhostsの参照を有効にする（アダプタによらず共通）
$nicClass = Get-WmiObject -list Win32_NetworkAdapterConfiguration
$nicClass.enablewins($false,$true)
Get-WmiObject -Class win32_NetworkAdapterConfiguration | ft Description,DNSEnabledForWINSResolution,WINSEnableLMHostsLookup

#---------- netBIOS over TCP/IP
$a = Get-NetAdapter -Name $interface
$nic = Get-WmiObject -Class win32_NetworkAdapterConfiguration | Where-Object {$_.Description -eq $a.InterfaceDescription}
$r = $nic.SetTcpipNetbios(1)
$r = $nic.SetTcpipNetbios(0)
#SetTcpopNetbios option:
# 0 - Use NetBIOS setting from the DHCP server
# 1 - Enable NetBIOS over TCP/IP
# 2 - Disable NetBIOS over TCP/IP
#wmic nicconfig get description,index,TcpipNetbiosOptions
#wmic nicconfig where (IPEnabled=TRUE) call SetTcpipNetbios 1


#----------- ネットワークの場所（プロファイル）
Set-NetConnectionProfile -InterfaceAlias $interface -NetworkCategory Private
Get-NetConnectionProfile -InterfaceAlias $interface | Format-Table InterfaceAlias,NetworkCategory
