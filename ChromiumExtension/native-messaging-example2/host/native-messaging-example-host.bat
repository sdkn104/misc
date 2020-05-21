@echo off
:: Copyright (c) 2013 The Chromium Authors. All rights reserved.
:: Use of this source code is governed by a BSD-style license that can be
:: found in the LICENSE file.

time /t >> "%~dp0\\log.txt"

REM cscript /nologo "%~dp0/host.js" %*
REM set /p a = "sdfdsaf"
REM echo {"text":"abcde"}

"%~dp0\node.exe" "%~dp0\host.js" 

echo exiting >> "%~dp0\\log.txt"
time /t >> "%~dp0\\log.txt"
