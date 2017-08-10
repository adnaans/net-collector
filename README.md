# Network Collector

### Prerequisites
For storage model:  
> Docker, Grafana 

Dependecies, should all be installable via pip:  
> enum34, futures, grpcio, potsdb, protobuf, six, scapy

Server:
> Node.js, Express.js, Socket.io

### Run OpenTSDB
```sh
    docker run -p 4242:4242 petergrace/opentsdb-docker
```
### Start Grafana
(You should already have opentsdb as data source). (Instruction is Mac OS X specific).
```sh
    brew services start grafana
```
### Start the web server  
In the net-collector directory run: 
```sh
    node server.js
```  
The server is by default, on localhost:3001. To modify this, go into server.js and change the port in http.listen.
### Running the probe(s)
SSH into the server receiving the network traffic. 
```sh
ssh [user]@[server IP]
```  
Login and use the command. 

```sh
    python fun_probe.py --host [IP of Server] --port [an OPEN PORT]
```

### Running the collector
This can be done on the server or remotely.
```sh
    python fun_collector.py --host [IP of Host] --port [an OPEN PORT] --d1host [First Probe's Host IP] --d1port [first probe's port] 
    optional: --d2host, --d2port
```
(Currently only two probes are supported from the commandline).

### Run the client:
```sh
    python storednetclient.py --host [IP of Collector's HOST] --port [Collector's PORT] --subscribe ["any/separated/string"]
```
String is by default interfaces/ethnet/state, metrics will appear under this name in the tsdb and grafana.

### View the results
Go to localhost:3001 in a browser on the device running storednetclient.py, or go to [ip of device running storednetclient.py]:3001 on a separate device's browser. The metrics can be viewed via grafana at (by default) localhost:3000, provided you have a dashboard connected to OpenTSDB. Metrics can also be seen via OpenTSDB's graphical interface at (by default) localhost:4242.

### Note about Data Models
Data sent between probe, collector, and client are defined in protobuf files. The unique message types which are used in this case can be found in pkt.proto. Alterations can be made by the standard method: changing the source .proto file & then generating a .py file using the protobuf compiler.
