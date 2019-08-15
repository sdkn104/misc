function MyExit($code) { Read-Host "終了するにはEnterキーを押してください"; exit $code }
trap { Write-Host "【想定外のエラーが発生したので終了します】"; Out-Host -InputObject $_; MyExit 1 }

#証明書の登録
$kt = "C:\Program Files (x86)\Java\jre1.8.0_221\bin\keytool.exe"
$st = "C:\Users\sdkn1\AppData\LocalLow\Sun\Java\Deployment\security\trusted.cacerts" #（ユーザ：署名者のCA）
$ft = "D4:DE:20:D0:5E:66:FC:53:FE:1A:50:88:2C:78:DB:28:52:CA:E4:74"
$cert = ".\aaa"


$existFile = Test-Path $st
$alredyExist = $false
$aliases = @()
if( $existFile ) {
  $alredyExist = Write-Output "" | & $kt -list -keystore $st 2>$null | Select-String $ft -Quiet
  $aliases = Write-Output "" | & $kt -list -keystore $st -v 2>$null | Select-String "^\s*別名"
  # get password ...
  $storepass = ""
}
if( $existFile ) {
  Copy-Item $st $st+".bkup" -Force
}

if( -not $alredyExist) {
  if( $storepass -eq "" -and $aliases.Count -eq 0  ) {
    Remove-Item $st -Force
    $storepass = "changeit"
  }
  if( $storepass -eq "" ) {
    throw "エラー：keystoreに他のエントリが格納されていて、パスワードが不明です"
  }

  & $kt -importcert -keystore $st -file $cert -alias ca -storepass $storepass -noprompt 2> $null
  if( -not $? ) { throw "エラー：証明書を登録できませんでした" }
} else {
  Write-Host "すでに登録されています"
}

