
REM 名前と日付をクリップボードにコピーする

echo 部評> %TEMP%\tmp.stamp.txt
echo %DATE:/=.%>> %TEMP%\tmp.stamp.txt
echo 定兼>> %TEMP%\tmp.stamp.txt

clip < %TEMP%\tmp.stamp.txt
