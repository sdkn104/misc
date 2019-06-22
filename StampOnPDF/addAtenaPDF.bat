
@echo off

set TORIHIKISAKI=三菱電機株式会社
set MAKER=ルネサステクノロジ 株式会社
set INPDF=250_information.pdf
set OUTPDF=out.pdf


REM 宛名HTMLを生成する
del temp.htm
setlocal enabledelayedexpansion
for /f "delims=" %%A in (AtenaTemplate.htm) do (
    set x=%%A
　　if !x! equ TORIHIKISAKI set x=%TORIHIKISAKI%
　　if !x! equ MAKER        set x=%MAKER%
    echo !x!
) >> temp.htm

REM 宛名HTMLをPDFに変換する
bin\wkhtmltopdf temp.htm stamp.pdf

REM 宛名をPDFに追加する
pdftk %INPDF% stamp stamp.pdf output %OUTPDF%

del /F temp.htm stamp.pdf

pause
