//----------------------------------------------------------
//getElementById(id)
//----------------------------------------------------------
function $(obj){
	return document.getElementById(obj);
}

//----------------------------------------------------------
//getElementsByName(name)
//----------------------------------------------------------
function $$(obj){
	return document.getElementsByName(obj);
}

//----------------------------------------------------------
//display system time
//----------------------------------------------------------
function $showtime(id){
	//eg: pattern = "yyyy-MM-dd hh:mm:ss";
	Date.prototype.getFormattedDate = function(pattern){			    
		function getFullStr(i){return i>9?""+i:"0"+i;}		    
		pattern = pattern.replace(/yyyy/,this.getFullYear())
			.replace(/MM/,getFullStr(this.getMonth()+1))
			.replace(/dd/,getFullStr(this.getDate()))
			.replace(/hh/,getFullStr(this.getHours()))
			.replace(/mm/,getFullStr(this.getMinutes()))
			.replace(/ss/,getFullStr(this.getSeconds()));			
			return pattern;
			};			
	var localTimeSpan = document.getElementById(id);
	localTimeSpan.innerHTML = (new Date()).getFormattedDate("yyyy-MM-dd hh:mm:ss");
	setInterval(function(){localTimeSpan.innerHTML = (new Date()).getFormattedDate("yyyy-MM-dd hh:mm:ss");}, 1000);
}

//----------------------------------------------------------
//--excute shell command--
//----------------------------------------------------------
function $cmd(cmd){
	alert(cmd);
	var objShell = new ActiveXObject("Wscript.shell");
	objShell.Run("%Comspec% /c \"" + cmd + "\""); 
    	objShell = "";
}

//----------------------------------------------------------
//--get computer name--
function $computer(){
	var obj = new ActiveXObject("WScript.Network");
	var computer = unescape(obj.ComputerName);
	obj= null;
	return computer;
}

//----------------------------------------------------------
//--find column ID by column name for 2-dim array--
//----------------------------------------------------------
function $col_id(arr,col_name){
	for(var i=0; i<arr[0].length; i++){
		if(arr[0][i].toUpperCase() == col_name.toUpperCase()){return i;}
		}
	return -1;
}

//----------------------------------------------------------
//--arr with keywords of keyfiled highlighted--
//----------------------------------------------------------
function $arr_hlkw(arr,kf,kw){
	var cid = $col_id(arr,kf);
	if(cid!=-1){
		for(var i=1;i<arr.length;i++){ 	//--i start form 1 for not seraching arr head
			var re = new RegExp("\("+kw+"\)","gmi");
			arr[i][cid] = arr[i][cid].replace(re,"<span class='highlight'>$1</span>");
		} 	
	}
	return arr;
}

//----------------------------------------------------------
//--2-dim arr to HTML table--
//----------------------------------------------------------
function $arr2table(arr){
	var html = "";
	html=html+"<table>";
	html=html+"<tr>";

	for(var i=0;i<arr[0].length;i++){html=html+"<th>"+arr[0][i]+"</th>";} 
	html=html+"</tr>";
	for(var i=1;i<arr.length;i++){
		html=html+"<tr>";
		for(var j=0;j<arr[0].length;j++){html=html+"<td>"+arr[i][j]+"</td>";} 
		html=html+"</tr>";	
	} 
	html=html+"</table>";
	return html;	
}

//----------------------------------------------------------
//--change background-color for tab_id
//----------------------------------------------------------
function $chbgc(tab_id,id){
	var trid = tab_id.rows[id].style;
	if(trid.backgroundColor==""){
		trid.backgroundColor = "yellow";
		trid.cursor = "hand";
	}else{
		trid.backgroundColor = "";
		trid.cursor = "default";
	}
}

//----------------------------------------------------------
//select the option of sel_id by txt
//----------------------------------------------------------
function $selectop(sel_id,txt){
	var obj = $(sel_id);

	for(var i=0;i<obj.options.length;i++){
		if(obj.options[i].value == txt){obj.selectedIndex = i;}
	}
}

//----------------------------------------------------------
//2-dim arr to HTML table with table ID & events-
//fun=function name,  
//----------------------------------------------------------
function $arr2tabid(arr,tab_id,fun){
	var html = "";
	html=html+"<table id='"+tab_id+"'>";

	html=html+"<tr>";
	for(var i=0;i<arr[0].length;i++){html=html+"<th>"+arr[0][i]+"</th>";} 
	html=html+"</tr>";

	for(var i=1;i<arr.length;i++){
		html=html+"<tr onclick='"+fun+"("+tab_id+",this.rowIndex)' onmouseover='$chbgc("+tab_id+",this.rowIndex)' " ;
		html=html+ "onmouseout='$chbgc("+tab_id+",this.rowIndex)'>";
		for(var j=0;j<arr[0].length;j++){
			html=html+"<td>"+arr[i][j]+"</td>";
		} 
		html=html+"</tr>";	
	} 
	html=html+"</table>";
	return html;	
}
