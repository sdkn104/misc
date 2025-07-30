
@echo ------------------------------------------------------------------------------------

@REM ????????????????????

@schtasks.exe /create /tn "座席管理システム警告" /sc DAILY /st 08:02 /ri 10 /du 14:00 ^
  /tr "cscript //B //H:CScript \"D:\NoSync\misc\Comp\SeatSystemPopup\dist\seatSystemPopup.exe\"" ^
  /it /k /f  

@echo .

@if errorlevel 0 (
  @echo 成功しました
) else ( 
  @echo 失敗しました
)

@echo .
@echo to uninstall, schtasks.exe /delete /tn "座席管理システム警告" /f
@echo .

pause

