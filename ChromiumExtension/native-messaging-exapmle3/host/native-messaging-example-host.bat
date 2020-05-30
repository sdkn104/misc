@echo off

time /t >> "%~dp0\\log.txt"

"%~dp0\cs\bin\Debug\netcoreapp2.2\win-x64\publish\cons.exe" %*

echo exiting >> "%~dp0\\log.txt"
time /t >> "%~dp0\\log.txt"
