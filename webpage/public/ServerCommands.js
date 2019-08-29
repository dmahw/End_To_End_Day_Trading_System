var transactionNumber = 1;

function SEND() {
	var username = $("#UserName").val();
	var instruction = $("#Instruction").val();
	instruction = sanitize(instruction);
	instruction = "[" + transactionNumber + "] " + instruction;
	console.log(instruction)
	SendCommand(username, instruction)
}

function UPDATEINFO() {
	var username = $("#UserName").val();
	var instruction = "[" + transactionNumber + "] DISPLAY_SUMMARY," + username;
	(new NetworkAdapter()).send(instruction, callback);
	function callback(resp){
		parseOutResponse(resp);
	}
}

function SendCommand(username, data){	
	(new NetworkAdapter()).send(data, callBack);

	function callBack(resp){
		console.log(resp);
	}
	transactionNumber++;
}

function parseOutResponse (resp) {
	var jsonResp = JSON.parse(resp);
	console.log(jsonResp);
	$("#responseText").val(JSON.stringify(jsonResp, null, 4));  
}

function sanitize(data){
    return data.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;').replace(/\(/g, '%28;');
}

// function ADD(){
// 	if(CheckFields()){
// 		SendCommand("ADD", 3);
// 	}else{
// 		console.log("FALSE");
// 	}
// }

// function QUOTE(){
// 	var i = 1;
// 	if (!document.getElementById("UserName").value){
// 	    $('#user-err').html('Must be filled out');
// 	    i = 0;
// 	}else{
// 	    $('#user-err').html('');
// 	}
// 	if (!document.getElementById("Stock").value){
// 	    $('#stock-err').html('Must be filled out');
// 	    i = 0;
// 	}else{
// 		$('#stock-err').html('');
// 	}
// 	if(i==0){
// 		return false;
// 	}
// 	SendCommand("QUOTE", 2);
// }

// function BUY(){
// 	if(CheckFields()){
// 		SendCommand("BUY", 3);
// 		popup();
// 	}
// }

// function COMMIT_BUY(){
// 	if (!document.getElementById("UserName").value){
// 	    $('#user-err').html('Must be filled out');
// 	    return false;
// 	}else{
// 	    $('#user-err').html('');
// 	    SendCommand("COMMIT_BUY", 1);
// 	}
// 	//WHAT DO WE WANT? let them commit_buy whenever or force them to do it right away?

// }

// function CANCEL_BUY(){
// 	if (!document.getElementById("UserName").value){
// 	    $('#user-err').html('Must be filled out');
// 	    return false;
// 	}else{
// 	    $('#user-err').html('');
// 	    SendCommand("CANCEL_BUY", 1);
// 	}
// }

// function SELL(){
// 	if(CheckFields()){
// 		SendCommand("SELL", 3);
// 	}
// }

// function COMMIT_SELL(){
// 	if (!document.getElementById("UserName").value){
// 	    $('#user-err').html('Must be filled out');
// 	    return false;
// 	}else{
// 	    $('#user-err').html('');
// 	    SendCommand("COMMIT_SELL", 1);
// 	}
// }

// function CANCEL_SELL(){
// 	if (!document.getElementById("UserName").value){
// 	    $('#user-err').html('Must be filled out');
// 	    return false;
// 	}else{
// 	    $('#user-err').html('');
// 		SendCommand("CANCEL_SELL", 1);
// 	}
// }

// function SET_BUY_AMOUNT(){
// 	if(CheckFields()){
// 		SendCommand("SET_BUY_AMOUNT", 3);		
// 	}
// }

// function SET_BUY_TRIGGER(){
// 	if(CheckFields()){
// 		SendCommand("SET_BUY_TRIGGER", 3);
// 	}
// }

// function CANCEL_SET_BUY(){
// 	if(CheckFields()){
// 		SendCommand("CANCEL_SET_BUY", 3);
// 	}
// }

// function SET_SELL_AMOUNT(){
// 	if(CheckFields()){
// 		SendCommand("SET_SELL_AMOUNT", 3);
// 	}
// }

// function SET_SELL_TRIGGER(){
// 	if(CheckFields()){
// 		SendCommand("SET_SELL_TRIGGER", 3);
// 	}
// }

// function CANCEL_SET_SELL(){
// 	if(CheckFields()){
// 		SendCommand("CANCEL_SET_SELL", 3);
// 	}
// }

// function DISPLAY_SUMMARY(){
// 	if (!document.getElementById("UserName").value){
// 	    $('#user-err').html('Must be filled out');
// 	   	return false;
// 	}else{
// 	    $('#user-err').html('');
// 	    SendCommand("DISPLAY_SUMMARY", 1);
// 	}
// }

// function CheckFields(){
// 	var i = 1;
// 	if (!document.getElementById("UserName").value){
// 	    $('#user-err').html('Must be filled out');
// 	    i = 0;
// 	}else{
// 	    $('#user-err').html('');
// 	}
// 	if (!document.getElementById("Stock").value){
// 	    $('#stock-err').html('Must be filled out');
// 	    i = 0;
// 	}else{
// 		$('#stock-err').html('');
// 	}
// 	if (!document.getElementById("Amount").value){
// 	    $('#amount-err').html('Must be filled out');
// 	    i = 0;
// 	}else{
// 		$('#amount-err').html('');
// 	}

// 	if(i==0){
// 		return false;
// 	}
// 	return true;
// }

// function SendCommand(Command, x){	
// 	var username = $("#UserName").val();
// 	var comString = "[" + transactionNumber + "] " + Command + "," + username;
// 	if(x==3){
// 		var stock = $("#Stock").val();
// 		var amount = $("#Amount").val();
// 		comString += "," + stock + "," + amount;
// 	}else if(x==2){
// 		var stock = $("#Stock").val();
// 		comString += "," + stock;
// 	}

// 	console.log("Here now");
// 	(new NetworkAdapter()).send(comString, callBack);

// 	function callBack(success){
// 		if(success){
// 			console.log("Yay");
// 		}else{
// 			console.log("aww");
// 		}
// 	}

// 	console.log(comString);
// 	transactionNumber ++;
	
// }

// //popup
// var modal = document.getElementById('myModal');
// var span = document.getElementsByClassName("close")[0];

// function popup() {
// 	console.log("HERE");
// 	modal.style.display = "block";
// }

// span.onclick = function() {
//   modal.style.display = "none";
// }



// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }
