var express = require('express');
var app = express();
var http = require('http');

var server = http.createServer(app);
var io = require("socket.io").listen(server);

app.use(express.static("public"));

app.get('', function(req, res, next) {
    res.sendFile(__dirname + '/public/Landing.html');
});

server.listen(3000, function(){
	console.log("Listening on port 3000");
});


