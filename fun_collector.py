"""
Simple Collector, initiates gNMI calls to multiple fun_probes and aggregates   
"""

import gnmi.gnmi_pb2_grpc as gnmi_pb2_grpc
import gnmi.gnmi_pb2 as gnmi_pb2
from pathtree.pathtree import Branch as Branch 
from pathtree.pathtree import Path
import grpc
from concurrent import futures
import time
import logging
import argparse

import Queue
import threading 

from scapy.all import *

queues = []
processingQ = Queue.Queue()

# - logging configuration
logging.basicConfig()
logger = logging.getLogger('collector')

logger.setLevel(logging.DEBUG)

#configure southbound device address
device1_ip = "" #h1.IP()
device1_port = ""

device2_ip = "" #h2.IP()
device2_port = ""

host_ip = ""
host_port = ""

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CollectorServicer(gnmi_pb2_grpc.gNMIServicer):

    def __init__(self):
        #initiate an empty pathtree for storing updates from the probes
        self.ptree = Branch() 

    def filterAndPackage(self, update):
        src = update.IP().src()
        dst = update.IP().dst()
        fixedUpdate = gnmi_pb2.IpPair(src=src, dst=dst)
        return fixedUpdate

    def stream(self, stub, request_iterator):  
        for response in stub.Subscribe(request_iterator):
            logger.debug(response)
            if response.update:
                logger.info("Collector has registered a response.")
                processingQ.put(filterAndPackage(response.update)) 
            else:
                pass

    def processThatQ(self): #STILL NEED TO FIGURE OUT PATHTREE STUFF
        PAIR_LIST = []
        while True: 
            pkgdPkt = processingQ.get()
            PAIR_LIST.append(pkgdPkt)
            if (len(PAIR_LIST)>=100): #if the number of saved IpPair messages is 100
                batch = gnmi_pb2.IpPairBatch()
                for pair in PAIR_LIST:
                    batch.add_ip(pair)
                    #saveToPathTree(batch)
                    for q in queues:
                        q.put(batch)
                    del PAIR_LIST[:]

    def Subscribe(self, request_iterator, context):
        logger.info("Collector has received a subscribe request.")
        #create a channel connecting to the southbound device
        logger.info("Connecting to: " + device1_ip + " : " + device1_port)
        logger.info("Connecting to: " + device2_ip + " : " + device2_port)
        channel1 = grpc.insecure_channel(device1_ip + ":" + str(device1_port))
        stub1 = gnmi_pb2.gNMIStub(channel1)

        channel2 = grpc.insecure_channel(device2_ip + ":" + str(device2_port))
        stub2 = gnmi_pb2.gNMIStub(channel2)

        q = Queue.Queue()
        queues.append(q)

        #start streaming
        stubs = [stub1, stub2]
        threads = []
        for stub in stubs:
            t = threading.Thread(target=self.stream, args=(stub, request_iterator))
            threads.append(t) #is this even needed bro
            t.start()
        processingT = threading.Thread(target=self.processThatQ)
        while True:
            for q in queues:
                yield q.get()


        print "Streaming done!"
    
    #def saveToPathTree(self, update): #what is the point of this pathtree... we should ask song eventually
        #tm = update.timestamp
        #updates = update.update

        #for u in updates:
           #path = u.path
           #val = u.val
           #pathStrs = self.encodePath(path.elem)
           #self.ptree.add(pathStrs, tm, val.ip)

    def encodePath(self, path):
        pathStrs = []
        for pe in path:
            pstr = pe.name
            if pe.key:
                for k, v in pe.key.iteritems():
                    pstr += "[" + str(k) + "=" + str(v) + "]"
            pathStrs.append(pstr)
        return pathStrs


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost',
                        help='OpenConfig server host')
    parser.add_argument('--port', type=int, default="",
                        help='OpenConfig server port')

    parser.add_argument('--d1host', default='', help='ip address for device 1')
    parser.add_argument('--d2host', default='', help='ip address for device 2')

    parser.add_argument('--d1port', default='', help='port for device 1')
    parser.add_argument('--d2port', default='', help='port for device 2')

    #parser.add_argument('--sample', type=int, default=1,
    #                   help='how many messages to be aggregated')
    parser.add_argument('--debug', type=str, default='on', help='debug level')
    args = parser.parse_args()

    #global interval
    #interval = args.sample
    host_ip = args.host
    host_port = args.port

    device1_ip = args.d1host
    device1_ip = args.d2host

    device1_port = args.d1port
    device2_port = args.d2port

    logger.info(device1_ip)
    logger.info(device2_ip)
    logger.info(device1_port)
    logger.info(device2_port)
    

    if args.debug == "off":
        logger.setLevel(logging.INFO)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #COULD BLOCK
    gnmi_pb2_grpc.add_gNMIServicer_to_server(
        CollectorServicer(), server)
    server.add_insecure_port(args.host + ":" + str(args.port))
    server.start()
    logger.info("Collector Server Started.....")
    #CONSTRUCT QUEUE FOR PROBE TO PROCESSING
    #KICK OFF CLIENT LISTENING (SENDING PKTS TO PROCESSING QUEUE) [1 THREAD PER CLIENT]
    #KICK OFF THREAD CONSUMING PROCESSING QUEUE
    #LIST OF SUBSCRIBER QUEUES
    try:
       while True:
          time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()