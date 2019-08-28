
$nmapExe = "nmap"
$targets = "192.168.1.1-255"
$tmpXmlFile = ".\tmp.xml"
$csvFile = ".\out.csv"

# scan by nmap
$o = & $nmapExe $targets -sn -oX $tmpXmlFile
$xml = [xml](Get-Content $tmpXmlFile)

# extract results
$NOW = Get-Date
$hosts = $xml.nmaprun.host | foreach { 
    $ip = $_.address | where { $_.addrtype -eq "ipv4" }; 
    $mac = $_.address | where { $_.addrtype -eq "mac" }; 
    @{"IP" = $ip.addr; "MAC" = $mac.addr; "LAST" = $NOW; }; 
}

# output
$objHosts = $hosts | foreach { [PSCustomObject]$_ }
$objHosts
$objHosts | Export-Csv $csvFile
