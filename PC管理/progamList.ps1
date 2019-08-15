$base = "\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
$wow64 = "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
$path = @(("HKLM:" + $base), ("HKCU:" + $base))
if(Test-Path $wow64){
    $path += $wow64
}
Get-ChildItem -Path $path |
    %{Get-ItemProperty $_.PsPath} |
    ?{$_.systemcomponent -ne 1 -and $_.parentkeyname -eq $null} |
    sort displayname |
    select DisplayName,Publisher,DisplayVersion |
    Export-Csv -path .\programList.csv  -Encoding Default -NoTypeInformation
Write-Host ".\programList.csvに出力しました"
