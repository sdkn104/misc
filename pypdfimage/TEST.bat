
%echo off

setlocal enabledelayedexpansion
for %%f in (%*) do (
  echo %%~nxf Çì«Ç›çûÇÒÇ≈Ç¢Ç‹Ç∑
  for /f "usebackq delims=" %%a in (`python registerFileOCR.py %%f`) do set INO=%%a

  echo !INO!
  copy "%%f" "!INO!.pdf"
)

pause
