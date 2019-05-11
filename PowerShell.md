TOP: https://docs.microsoft.com/en-us/powershell/?view=powershell-5.0

SDK TOP: https://docs.microsoft.com/en-us/powershell/developer/windows-powershell

- Cmdlet: https://docs.microsoft.com/en-us/powershell/developer/cmdlet/writing-a-windows-powershell-cmdlet

Ref TOP: https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-5.0

- Learning PS: https://docs.microsoft.com/en-us/powershell/scripting/learn/understanding-important-powershell-concepts?view=powershell-5.0

- Core Ref: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/?view=powershell-5.0

- about Ref (構文）: https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/?view=powershell-5.0


Language Spec. 3.0 (5.0も同じはず)
https://www.microsoft.com/en-us/download/confirmation.aspx?id=36389

Array
```
$a = 1, 2, 3
$a = @(1)
$a.Count
```
Hash:
```
$hash = @{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash = [orderd]@{ Number = 1; Shape = "Square"; Color = "Blue"}
$hash.Keys
$hash.Color
$hash["Color"]
$hash[0]
```

Location:
```
pwd
dir
Get-Item C:\Users\*
```

String
```
"a" + "b"
"abc.txt".Replace("txt","log")
"abc.txt" -replace '\.txt$','.log'
if( "abc.txt" -match '\.txt$' ) { "ok" }
if( "abc.txt" -like '*txt' ) { "ok" }
ipconfig | Select-String "イーサネット"
-split "a b c d"
"a:b:c" -split ":"
```

Type
```
(get-date) -is [DateTime]
(get-date).GetType()
```

```cat```
```ps```

```Get-Command -Verb Get ```

```Get-ChildItem -?```   HELP

```Get-Help Get-ChildItem```   HELP

```Get-Alias```


```$files = dir```

```
$d = Get-ChildItem | sort | Where-Object { $_.Name -like "*D*" } | Select-Object Length,Name,Mode
Foreach( $i in $d ){ $i }
```
```Select-Object```
```Group-Object```
```Write-Host```
```Out-Host```
```Format-Table```
```Format-List```
``````
``````
``````

