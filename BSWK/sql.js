var conn ;
var rs ; 
//----------------------------------------------------------
//Open SQL sever Connection
//----------------------------------------------------------
function SQL_open(){
	conn = new ActiveXObject("ADODB.Connection");
	rs = new ActiveXObject("ADODB.Recordset"); 
	conn.Open("Driver={SQL server};Server=xxx;DataBase=xxx;UID=xxx;Password=xxx;");
	//conn.ConnectionString="provider=Microsoft.Jet.OLEDB.4.0;data source="+"D:\\xxx.mdb";
	//conn.ConnectionString="data source="+Server.MapPath("bin\\database.mdb");
	//conn.Open(); 
}

//----------------------------------------------------------
//Close SQL server connection
//----------------------------------------------------------
function SQL_close(){

	rs = null;
	conn.close();
	conn = null;
}

//----------------------------------------------------------
//read data form SQL DB and save it to 2-dim array
//----------------------------------------------------------
function SQL_read(sql){

	var arr = new Array;
	var j = 1;

	arr[0] = new Array;

	SQL_open();
	rs.open(sql, conn); 

	for(var i=0;i<rs.Fields.Count;i++){
		arr[0][i] = rs.Fields(i).Name;
	} 

	while(!rs.EOF){ 

		arr[j] = new Array;
		
		for(var i=0;i<rs.Fields.Count;i++){
			var temp = rs.Fields(i).Value;
			if(temp==null){
				arr[j][i] = "";
			}else{
				arr[j][i] = temp ;
			} 
		}
		j++ ;
		rs.moveNext(); 
	} 

	rs.close(); 
	SQL_close();

	return arr;
}

//----------------------------------------------------------
//add new record to SQL DB
//tbl=sql table, idx=index field,arr=[field-name,value]
//----------------------------------------------------------
function SQL_add(tbl,idx,arr){

	var sql="select * from "+tbl+" Where "+idx+" is Null ";

	if(arr.length>0){
		SQL_open();
		rs.open(sql, conn, 1, 3); 
		rs.addNew();

		for(var i=0;i<arr.length;i++){rs.Fields(arr[i][0])=arr[i][1];}	
	
		rs.update();
		rs.close(); 
		SQL_close();
	}
}

//----------------------------------------------------------
//modify a record
//tbl=sql table, idx=index,idx_num=autonumber
//arr=[field-name,value]
//----------------------------------------------------------
function SQL_modify(tbl,idx,idx_num,arr){

	var sql="select * from "+tbl+" Where "+idx+"='"+idx_num+"'";

	if(arr.length>0){
		SQL_open();
		rs.open(sql, conn, 1, 3); 
		if(!rs.EOF){
			for(var i=0;i<arr.length;i++){rs.Fields(arr[i][0])=arr[i][1];}	
			rs.update();
		}
		rs.close(); 
		SQL_close();
	}
}

//----------------------------------------------------------
//delete record from SQL DB
//tbl=sql table, idx=index field,idx_num=autonumber
//----------------------------------------------------------
function SQL_del(tbl,idx,idx_num){
	var sql="select * from "+tbl+" Where "+idx+"='"+idx_num+"'";
	SQL_open();
	rs.open(sql, conn, 1, 3); 

	if(!rs.EOF){rs.Delete();rs.update();}

	rs.close(); 
	SQL_close();
}
