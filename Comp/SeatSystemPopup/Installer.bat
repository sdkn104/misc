
@echo ------------------------------------------------------------------------------------

@REM ????????????????????

@schtasks.exe /create /tn "���ȊǗ��V�X�e���x��" /sc DAILY /st 08:02 /ri 10 /du 14:00 ^
  /tr "cscript //B //H:CScript \"D:\NoSync\misc\Comp\SeatSystemPopup\dist\seatSystemPopup.exe\"" ^
  /it /k /f  

@echo .

@if errorlevel 0 (
  @echo �������܂���
) else ( 
  @echo ���s���܂���
)

@echo .
@echo to uninstall, schtasks.exe /delete /tn "���ȊǗ��V�X�e���x��" /f
@echo .

pause

