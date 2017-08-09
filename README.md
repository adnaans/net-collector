# Network Collector

(For storage model):  
Docker, Grafana  

(Dependecies):  
enum34, futures, grpcio, potsdb, protobuf, six, scapy

### Run OpenTSDB
```sh
    docker run -p 4242:4242 petergrace/opentsdb-docker
```
### Start Grafana
(You should already have opentsdb as data source).
```sh
    brew services start grafana
```
### Start the web server  
In the net-collector directory run: 
```sh
    node server.js
```  
The server is by default, on localhost:3001. To modify this, go into server.js and change the port in http.listen.
### SSH into the server receiving the network traffic  
Run the probe(s):  

```sh
    python fun_probe.py --host [IP of Switch] --port [an OPEN PORT]
```
### On the server or remotely
Run the collector:
```sh
    python fun_collector.py --host [IP of Host] --port [an OPEN PORT] --d1host [First Probe's Host IP] --d1port [first probe's port] 
    optional: --d2host, --d2port
```
(Currently only two probes are supported from the commandline).

Run the client:
```sh
    python storednetclient.py --host [IP of Collector's HOST] --port [Collector's PORT] --subscribe ["any/separated/string"]
```
String is by default interfaces/ethnet/state, metrics will appear under this name in the tsdb and grafana.

### View the server page
Go to localhost:3001 in a browser on the device running storednetclient.py, or go to [ip of device running storednetclient.py]:3001 on a separate device's browser.
