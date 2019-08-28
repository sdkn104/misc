

$nmapout = & nmap 192.168.1.1-255 -sn

$ip = ""
$hosts = foreach( $line in $nmapout) {
  if( $line -match "(Nmap scan report for |Nmap done:)" -and $ip -ne "" ) {    
      Write-Host "ERROR: no MAC address reported for $ip"
  }
  if( $line -match "Nmap scan report for *([0-9.]+)" ) { $ip = $Matches[1]; $mac = "" }
  elseif( $line -match "Nmap scan report for .*[(]([0-9.]+)[)]" ) { $ip = $Matches[1]; $mac = "" }
  elseif( $line -match "Nmap scan report for " ) { Write-Host "ERROR: not IP found for: $line" }
  if( $line -match "MAC Address: *([0-9A-Fa-f:]+)" ) {
    $mac = $Matches[1] 
    @{ "IP" = $ip; "MAC" = $mac; }
    $ip = $mac = ""
  }
}
$hosts | foreach { [PSCustomObject]$_ } | ft

