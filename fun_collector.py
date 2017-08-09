"""
Simple Collector, initiates gNMI calls to multiple fun_probes and aggregates   
"""

import gnmi.gnmi_pb2_grpc as gnmi_pb2_grpc
import gnmi.gnmi_pb2 as gnmi_pb2

import gnmi.pkt_pb2 as pkt_pb2

from google.protobuf import any_pb2 

from pathtree.pathtree import Branch as Branch 
from pathtree.pathtree import Path
import grpc
from concurrent import futures
import time
import logging
import argparse

import Queue
import threading 
import copy

from scapy.all import *


queues = []
processingQ = Queue.Queue()

# - logging configuration
logging.basicConfig()
logger = logging.getLogger('collector')
logger.setLevel(logging.DEBUG)


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

PAIR_LIST = []

class CollectorServicer(gnmi_pb2_grpc.gNMIServicer):

    def __init__(self):
        #initiate an empty pathtree for storing updates from the probes
        self.ptree = Branch() 

    def filterAndPackage(self, notif):
        updates = notif.update
        for u in updates: 
            packet =pkt_pb2.Packet()
            u.val.any_val.Unpack(packet)
            src = packet.i.src
            dst = packet.i.dst
            fixedUpdate = pkt_pb2.IpPair(src=src, dest=dst)
            return fixedUpdate

    def stream(self, stub, request_iterator):  
        for response in stub.Subscribe(request_iterator): 
            if response.update:
                print "got smth!"
                processingQ.put(self.filterAndPackage(response.update)) 
            else:
                pass

    def processThatQ(self): 
        logger.info("thread to aggregate off collection q called.")
        while True: 
            try: 
                pkgdPkt = processingQ.get(False) #STUCK HERE
            except Queue.Empty:
                pkgdPkt = None
            if pkgdPkt != None: 
                PAIR_LIST.append(pkgdPkt)
                if (len(PAIR_LIST)>=250): 
                    for pair in PAIR_LIST:
                        batch = pkt_pb2.IpPairBatch(ip=PAIR_LIST)
                        for q in queues:
                            q.put(batch)
                    del PAIR_LIST[:]

    def Subscribe(self, request_iterator, context):
        q = Queue.Queue()
        queues.append(q)

        while True:
            #for q in queues: 
            batch = None
            try: 
                batch = q.get(False)
            except Queue.Empty:
                batch = None
            if batch!=None:
                any_msg = any_pb2.Any()
                any_msg.Pack(batch)
                t = gnmi_pb2.TypedValue(any_val=any_msg)
                update_msg = [gnmi_pb2.Update(val=t)]
                tm = int(time.time() * 1000)
                notif = gnmi_pb2.Notification(timestamp=tm, update=update_msg)
                response = gnmi_pb2.SubscribeResponse(update=notif)
                print "sent something!"
                yield response

        print "Streaming done!"
    
    #def saveToPathTree(self, update): #what is the point of this pathtree... we should ask song eventually
        #tm = update.timestamp
        #updates = update.update

        #for u in updates:
           #path = u.path
           #val = u.val
           #pathStrs = self.encodePath(path.elem)
           #self.ptree.add(pathStrs, tm, val.ip)

    #def encodePath(self, path):
        #pathStrs = []
        #for pe in path:
            #pstr = pe.name
            #if pe.key:
                #for k, v in pe.key.iteritems():
                    #pstr += "[" + str(k) + "=" + str(v) + "]"
            #pathStrs.append(pstr)
        #return pathStrs

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

    parser.add_argument('--debug', type=str, default='on', help='debug level')
    args = parser.parse_args()


    host_ip = args.host
    host_port = args.port
    device1_ip = args.d1host
    device2_ip = args.d2host
    device1_port = args.d1port
    device2_port = args.d2port

    if args.debug == "off":
        logger.setLevel(logging.INFO)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #COULD BLOCK
    gnmi_pb2_grpc.add_gNMIServicer_to_server(
        CollectorServicer(), server)
    server.add_insecure_port(args.host + ":" + str(args.port))
    server.start()

    logger.info("Collector Server Started.....")
    
    #open connection to probes
    logger.info("Connecting to: " + device1_ip + " : " + device1_port)
    logger.info("Connecting to: " + device2_ip + " : " + device2_port)
    
    stub1 = None
    stub2 = None
    if device1_ip and device1_port:
        channel1 = grpc.insecure_channel(device1_ip + ":" + str(device1_port))
        stub1 = gnmi_pb2_grpc.gNMIStub(channel1)

    if device2_ip and device2_port:
        channel2 = grpc.insecure_channel(device2_ip + ":" + str(device2_port))
        stub2 = gnmi_pb2_grpc.gNMIStub(channel2)

    #start streaming
    stubs = [stub1, stub2]
    threads = []
    for stub in stubs: #sends dummy iter to probe.
        if stub:
            t = threading.Thread(target=CollectorServicer().stream, args=(stub, iter([])))
            threads.append(t)
            t.daemon = True
            t.start()
    processingT = threading.Thread(target=CollectorServicer().processThatQ)
    processingT.daemon = True
    threads.append(processingT)
    processingT.start()

    try:
       while True:
          time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()