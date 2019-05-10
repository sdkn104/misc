
https://docs.microsoft.com/ja-jp/powershell/scripting/learn/understanding-important-powershell-concepts?view=powershell-5.0

https://msdn.microsoft.com/ja-JP/Library/dd835506(VS.85).aspx

about(構文のリファレンス）
https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/?view=powershell-5.0

Language Spec. 3.0 (5.0も同じはず)
https://www.microsoft.com/en-us/download/confirmation.aspx?id=36389


```dir```
```cat```
```ps```

```Get-Command -Verb Get ```

```Get-ChildItem -?```   HELP

```Get-Help Get-ChildItem```   HELP

```Get-Alias```


```$files = dir```

```
$d = Get-ChildItem | Where-Object { $_.Name -like "*D*" } | Select-Object Length,Name,Mode
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

