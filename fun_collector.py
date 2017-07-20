"""
Simple Collector, accept gNMI calls from test client and initiate new gNMI calls
to Probes. Behaves as gNMI server to the test client and gNMI client to the probes
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
device_ip = "localhost"
device_port = 80049
host_ip = "localhost"
host_port = 80050

interval = 1

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class FunCollectorServicer(gnmi_pb2_grpc.gNMIServicer):

    def __init__(self):
        #initiate an empty pathtree for storing updates from the probes
        self.ptree = Branch() 

    def Subscribe(self, request_iterator, context):
        #create a channel connecting to the southbound device
        channel = grpc.insecure_channel(device_ip + ":" + str(device_port))
        stub = gnmi_pb2.gNMIStub(channel)
        counter = 0
        global interval
        #start streaming
        for response in stub.Subscribe(request_iterator):
            logger.debug(response)
            if response.update:
                self.saveToPathTree(response.update)
            else:
                pass
            counter+=1
            logger.debug("pathtree snapshot:")
            logger.debug(self.ptree.dic)
            if(counter >= interval): 
                self.getAverage(response, interval)
                counter = 0
                yield response
        print "Streaming done!"
    
    def getAverage(self, response, interval):
        noti = response.update
        updates = noti.update
        for u in updates:
            path = u.path
            pathStrs = self.encodePath(path.elem)
            average = self.ptree.getAverage(pathStrs, interval)
            u.val.int_val = average

    
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
    parser.add_argument('--device_port', type=int, default=80049,
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
