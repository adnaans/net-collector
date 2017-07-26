//Get metrics from the client continuously
//Store as var metric
var http = require('http');
var fs = require('fs');
var url = require('url');
var path = require('path');

var mimeTypes = {
    "html": "text/html",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "js": "text/javascript",
    "css": "text/css"};

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


