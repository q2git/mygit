Dim falg_End
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("Wscript.Shell")

'------------------------Create SAPPart.txt-------------------------
Set objConn = CreateObject("ADODB.Connection")
Set objRST = CreateObject("ADODB.Recordset")
strConn = "Provider = SQLOLEDB; Data Source = xxx;Initial Catalog =xxx;User ID =xxx;Password =xxx;"
strSQL = "Select  SAPPart, Max(TestDataId) as TID from TestData Where  " &_
	"  (xxx) Group By SAPPart Order By TID Desc "
objConn.Open strConn
objRST.open strSQL,objConn,1,1
Set objSAPPart = objFSO.OpenTextFile("D:\01_GuiXT\VBA\SAPPart.txt",2,1)
Do While Not objRST.EOF
	objSAPPart.WriteLine objRST.Fields(0).value
	flag_End = objRST.Fields(0).value
	objRST.movenext
Loop
objRST.Close
objConn.Close
objSAPPart.Close

'-------------------------Create Script.txt--------------------------
Set objSAPPart = objFSO.OpenTextFile("D:\01_GuiXT\VBA\SAPPart.txt",1)
Set objScript = objFSO.OpenTextFile("D:\01_GuiXT\VBA\Script.txt",2,1)
Do Until objSAPPart.AtEndOfStream
         str1 = objSAPPart.ReadLine
         Set objTemplet = objFSO.OpenTextFile("D:\01_GuiXT\VBA\Script_Templet.txt",1)
         Do Until objTemplet.AtEndOfStream
	str2 = objTemplet.ReadLine
	str3 = Replace(str2,"999999999",str1)
	objScript.WriteLine str3
         Loop
         objTemplet.Close
Loop
objSAPPart.Close
objScript.Close

'-------------------------Terminate SAP--------------------------
objShell.Run "Taskkill /F /IM  SAP* /T",,True

'-------------------------Launch SAP--------------------------
param = "\SAP\FrontEnd\SAPgui\sapshcut.exe "" -sysname=""P27: Production PDM [Public]"""&_
	" -client=011 -user=xxx -password=xxx -Language=E "
objShell.Run ("""C:/Program Files (x86)" & param)

'-------------------------Wait 30 Sec for starting SAP--------------------------
Wscript.Sleep 30000

'-------------------------Excute T-Code--------------------------
param = "C:\progra~2\sap\frontend\sapgui\guixt.exe" & _
	" Input=" & Chr(34) & "OK: process=D:\01_GuiXT\VBA\Script.txt " & Chr(34)
objShell.Run param

'-------------------------Check if Complete by Every 60 Sec--------------------------
Do While Not (objFSO.FileExists("D:\02_BOMs\"+flag_End+".HTM"))
	Wscript.Sleep 60000
Loop

'-------------------------Terminate SAP--------------------------
objShell.Run "Taskkill /F /IM  SAP* /T"

'-------------------------Upload BOMs to Server-------------------------
objShell.Run "D:\02_BOMs\CopyToServer.BAT"
'objShell.Run "Shutdown.exe /s"

Set objShell = Nothing
Set objFSO = Nothing
