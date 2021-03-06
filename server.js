//Get metrics from the client continuously
//Store as var metric
var http = require('http');
var fs = require('fs');
var url = require('url');
var path = require('path');
var express = require('express');

var mimeTypes = {
    "html": "text/html",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "js": "text/javascript",
    "css": "text/css"};

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser');

app.use( bodyParser.json() );

app.post('/post', function (req, res) {
  console.log(req.body)
  if(req.body['decision']){
    io.emit('backtowork');
  }
  else if(req.body['decision']==false){
    io.emit('keepworking');
  }
  else{
    console.log("error");
  }
  res.send('Got a POST request')
})

app.use(express.static(__dirname))

http.listen(3001, function(){
  console.log('listening on *:3001');
});


