$interface = "イーサネット"

#----- IPv6無効化
#Get-NetAdapterBinding
Disable-NetAdapterBinding -Name $interface -ComponentID ms_tcpip6
#Enable-NetAdapterBinding -Name $interface -ComponentID ms_tcpip6

#----- IPアドレスの設定
Get-NetIPInterface -InterfaceAlias $interface | format-table InterfaceAlias,Dhcp
Get-NetIPAddress -InterfaceAlias $interface

Remove-NetIPAddress -InterfaceAlias $interface  -Confirm:$false
#Get-NetRoute
Remove-NetRoute –DestinationPrefix 0.0.0.0/0 –InterfaceAlias $interface –NextHop 192.168.1.1 -Confirm:$false
Set-NetIPInterface -InterfaceAlias $interface -Dhcp Enable
Set-NetIPInterface -InterfaceAlias $interface -Dhcp Disable
New-NetIPAddress -InterfaceAlias $interface -IPAddress "192.168.1.233"  -PrefixLength 24 -DefaultGateway "192.168.1.1"

#----- DNS server
Get-DnsClientServerAddress -InterfaceAlias $interface
Set-DnsClientServerAddress -InterfaceAlias $interface -ServerAddresses @("192.168.1.1", "8.8.8.8")
Set-DnsClientServerAddress -InterfaceAlias $interface -ResetServerAddresses #IPがDHCPなら自動取得となる

#----- WINS server
netsh interface ip set wins $interface static 192.168.1.1
netsh interface ip add wins $interface 8.8.8.8
netsh interface ip set wins $interface dhcp

#--------- DNSサフィックス
#  - 「プライマリDNSサフィックス」：マシン固有。コンピュータ名の変更⇒詳細　で設定する。
#  - 「接続専用のDNSサフィックス（この接続のDNSサフィックス）」：アダプタ毎。アダプタのプロパティで設定。
#  - 「以下のサフィックスを順に追加する」：任意数を順番に指定可能。アダプタ毎。
#wmic /interactive:off nicconfig get index,description,DNSDomain,DNSDomainSuffixSearchOrder
#$class= [wmiclass]'Win32_NetworkAdapterConfiguration'
#$class.SetDNSSuffixSearchOrder()
Get-DnsClientGlobalSetting | format-table SuffixSearchList
# 以下の設定により、「以下のDNSサフィックス・・」「プライマリ及び・・」が切り替わる
Set-DnsClientGlobalSetting -SuffixSearchList @("ad.melco.co.jp", "mei.ad.melco.co.jp") 
Set-DnsClientGlobalSetting -SuffixSearchList @() # ->suffix削除

#--------- この接続(固有)のDNSサフィックス
#wmic /interactive:off nicconfig where index=1 call SetDNSDomain "ad.melco.co.jp"
Get-DnsClient -InterfaceAlias $interface | format-table ConnectionSpecificSuffix
Set-DnsClient -InterfaceAlias $interface -ResetConnectionSpecificSuffix
Set-DnsClient -InterfaceAlias $interface -ConnectionSpecificSuffix "ad.melco.co.jp"


#---------- netBIOS over TCP/IP
$r = $nic.SetTcpipNetbios(1)
$r = $nic.SetTcpipNetbios(0)
#SetTcpopNetbios option:
# 0 - Use NetBIOS setting from the DHCP server
# 1 - Enable NetBIOS over TCP/IP
# 2 - Disable NetBIOS over TCP/IP
#wmic nicconfig get description,index,TcpipNetbiosOptions
#wmic nicconfig where (IPEnabled=TRUE) call SetTcpipNetbios 1

#---------- DNSへの登録
Get-DnsClient -InterfaceAlias $interface | format-table *Register*
#$a = Get-NetAdapter -Name $interface
#$nic = Get-WmiObject -Class win32_networkadapterconfiguration | Where-Object {$_.Description -eq $a.InterfaceDescription}
#Select-Object -InputObject $nic Description, FullDNSRegistrationEnabled, DomainDNSRegistrationEnabled | Write-Output
Set-DnsClient -InterfaceAlias $interface -RegisterThisConnectionsAddress $false -UseSuffixWhenRegistering $false

