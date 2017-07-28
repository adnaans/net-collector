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
/*
fs.readFile('./index.html', function (err, html) {
    if (err) {
        throw err; 
    }       
    http.createServer(function(request, response) {  
      var uri = url.parse(request.url).pathname;
      console.log(uri);
      var filename = path.join(process.cwd(), uri);
      fs.exists(filename, function(exists){
        if(!exists || uri=="/") {
          response.writeHeader(200, {"Content-Type": "text/html"});  
          response.write(html);  
          response.end();
          return
        }
        var mimeType = mimeTypes[path.extname(filename).split(".")[1]];
        response.writeHead(200, mimeType);

        console.log("success");
        var fileStream = fs.createReadStream(filename);
        fileStream.pipe(response);

      });
      //   response.writeHeader(200, {"Content-Type": "text/html"});  
      //   response.write(html);  
      //   response.end();  
    }).listen(8000);
});

*/

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);


// app.get('/', function(req, res){
// res.sendFile(__dirname + '/index.html');
// });

// app.get('/', function (req, res) {
  // res.send('Hello World!')
// })

// app.post('/', function (req, res) {
//   res.send('Got a POST request')
// })

// app.put('/user', function (req, res) {
//   res.send('Got a PUT request at /user')
// })

// app.delete('/user', function (req, res) {
//   res.send('Got a DELETE request at /user')
// })

app.use(express.static(__dirname))


// app.get('/Users/adnaansachidanandan/Projects/net-collector', function(req, res){
//   res.sendFile(__dirname + '/index.html');
// });

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});


