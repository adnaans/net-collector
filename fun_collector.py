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


# - logging configuration
logging.basicConfig()
logger = logging.getLogger('collector')

logger.setLevel(logging.DEBUG)

#configure southbound device address
device1_ip = "localhost"
device1_port = 80049

device2_ip = "localhost"
device2_port = 80051

host_ip = "localhost"
host_port = 80050

interval = 1

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CollectorServicer(gnmi_pb2_grpc.gNMIServicer):

    def __init__(self):
        #initiate an empty pathtree for storing updates from the probes
        self.ptree = Branch() 

    def Subscribe(self, request_iterator, context):
        #create a channel connecting to the southbound device
        channel1 = grpc.insecure_channel(device1_ip + ":" + str(device1_port))
        stub1 = gnmi_pb2.gNMIStub(channel)
        counter = 0

        channel2 = grpc.insecure_channel(device2_ip + ":" + str(device2_port))
        stub2 = gnmi_pb2.gNMIStub(channel)
        global interval
        #start streaming
        stubs = [stub1, stub2]
        result = map(aggregate, stubs)

        print "Streaming done!"

    def aggregate(stub):
        for response in stub.Subscribe(request_iterator):
            logger.debug(response)
            if response.update:
                self.saveToPathTree(response.update)
            else:
                pass
            counter+=1
            logger.debug("pathtree snapshot:")
            logger.debug(self.ptree.dic)
            if (counter>=interval):
                yield response
            print "Streaming done!"
    
    def saveToPathTree(self, update):
        tm = update.timestamp
        updates = update.update

        for u in updates:
           path = u.path
           val = u.val
           pathStrs = self.encodePath(path.elem)
           self.ptree.add(pathStrs, tm, val.int_val)

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
    parser.add_argument('--port', type=int, default=80050,
                        help='OpenConfig server port')
    parser.add_argument('--device1_port', type=int, default=80049,
                        help='OpenConfig device port')
    parser.add_argument('--device2_port', type=int, default=80051,
                        help='OpenConfig device port')
    parser.add_argument('--sample', type=int, default=1,
                        help='how many messages to be aggregated')
    parser.add_argument('--debug', type=str, default='on', help='debug level')
    args = parser.parse_args()

    global device_port
    global interval
    device_port = args.device_port
    interval = args.sample

    if args.debug == "off":
        logger.setLevel(logging.INFO)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gnmi_pb2_grpc.add_gNMIServicer_to_server(
        CollectorServicer(), server)
    server.add_insecure_port(args.host + ":" + str(args.port))
    server.start()
    logger.info("Collector Server Started.....")
    try:
       while True:
          time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()