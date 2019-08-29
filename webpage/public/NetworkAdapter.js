class NetworkAdapter {

	constructor(){

	}

	eh(){
		console.log("unimplemented method call");
	}

        /**
         * @param {string} username
         * @param {string} password
         * @param {function} callback - function that is called when server responds with authentication results
         */
	send(data, callback){
        var http = new XMLHttpRequest();
        var url = 'http://localhost:8080/';

        var reMatcher = /^(\[(.*)\]\s(.*))$/;
        var stringMatch = data.match(reMatcher);
        var transactionNumber = stringMatch[2]
        var subString = stringMatch[3].split(",")
        var command = subString[0]
        var username = subString[1].trim()
        var message = transactionNumber + "," + stringMatch[3].trim()

        var params = "transactionNumber:" + transactionNumber + ",command:" + command + ",username:" + username + ",message:" + message

        http.open('POST', url, true);
        http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        http.setRequestHeader('Accept', 'application/x-www-form-urlencoded');
        http.onreadystatechange = function() {
            if(http.readyState == 4 && http.status == 200) {
                callback(http.statusText)
            }
        }
        http.send(params);
	}
}
  