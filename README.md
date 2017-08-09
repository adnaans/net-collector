# net-collector

(For storage model):
Docker
Grafana
(Dependecies):
enum34
futures
grpcio
potsdb
protobuf
six
scapy 

1. Run OpenTSDB, preferrably using a Docker image.
```
    docker run -p 4242:4242 petergrace/opentsdb-docker
```
2. Start Grafana. (should already have opentsdb as data source).
```
    brew services start grafana
```
3. Start web server 
   i. in net-collector directory run: 

```
        node server.js
```

   ii. by default, on localhost:3001
4. ssh into server
5. run probe(s): 

```
    python fun_probe.py --host [IP of Switch] --port [an OPEN PORT]
```

6. run collector (can be on server or "remotely")

```
    python fun_collector.py --host [IP of Host] --port [an OPEN PORT] --d1host [First Probe's Host IP] --d1port [first probe's port] 
    optional: --d2host, --d2port
```
    i. currently only two probes possible supported from commandline. 
7. run client:
```
    python storednetclient.py --host [IP of Collector's HOST] --port [Collector's PORT] --subscribe ["any/separated/string"]
```
    i. string is by default interfaces/ethnet/state, metrics will appear under this name
    in the tsdb
