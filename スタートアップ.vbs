

Wscript.Sleep 10000

On Error Resume Next
Set objWShell = CreateObject("Wscript.Shell") 
objWShell.run "cmd /c \\LS-YLA23\share\sadakane\t\test.bat" , vbHide 

