
WScript.echo("*** START "+WScript.ScriptName+" **************************************");

var strHostName = "Kaori-PC";
var strUserName = "Guest";
var strGroup= "Administrators";

var objDomain = GetObject("WinNT://" + strHostName);
var objGroup = objDomain.GetObject("group", strGroup);
objGroup.Add ("WinNT://" + strHostName + "/" + strUserName);

WScript.echo("ÉÜÅ[ÉUÅ["+strUserName+"Ç"+strHostName+"ÇÃ"+strGroup+"Ç÷í«â¡ÇµÇ‹ÇµÇΩ");
WScript.echo("*** END "+WScript.ScriptName+"   **************************************");
