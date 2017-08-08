import argparse
import logging
import sys
import time

import grpc.framework.interfaces.face
import potsdb

import pyopenconfig.gnmi_pb2 as gnmi_pb2
import gnmi.pkt_pb2 as pkt_pb2

import pyopenconfig.resources

import atexit
from scapy.all import *

import socket

import requests

# - logging configuration
logging.basicConfig()
logger = logging.getLogger('netclient')

logger.setLevel(logging.DEBUG)

host_ip = "" #h4.IP()
host_port = 9033

mode = "stream"
nums = 0

db_host = 'localhost'
db_port = 4242
metrics = potsdb.Client(db_host, port=db_port)

badsite_keywords= {"facebook", "twitter", "reddit", "netflix"}
path = "" 

def encodePath(path):
    pathStrs = "" 
    for pe in path:
        pstr = pe.name
        if pe.key:
             for k, v in pe.key.iteritems():
                  pstr += "[" + str(k) + "=" + str(v) + "]"
        pathStrs = pathStrs + "." + pstr
    return pathStrs[1:]

def saveToTSDB(ptg, response):
    global path
    path = pyopenconfig.resources.make_path(path) #not sure if this is the correct encoding procedure.
    path_metric = encodePath(path)  
    tm = response.update.timestamp
    metrics.send(path_metric, ptg, timestamp=tm)
    logger.debug("send to openTSDB: metric: %s, value: %s" %(path_metric, value))

def processPacket(response): 
    for update in response.update.update:
        path_metric = encodePath(update.path.elem)
        tm = response.update.timestamp
        batch = pkt_pb2.IpPairBatch()
        update.val.any_val.Unpack(batch)
        print(batch)
        badcounter = 0
        for pair in batch.ip: 
            src = pair.src
            dst = pair.dest
            try: 
                src_host = socket.getfqdn(src)
            except Exception as e:
                src_host = "none"
            try: 
                dst_host = socket.getfqdn(dst)
            except Exception as e:
                dst_host = "none"
            for bad_keyword in badsite_keywords:
                if (bad_keyword in src_host or bad_keyword in dst_host):
                    badcounter=badcounter+1
        ptg = (100*badcounter)/(len(batch.ip))
        #print(ptg)
        if(ptg>1):
            print("DECISION: Back to work!")
            decision=True
        elif(ptg<=1):
            print("DECISION: Keep working...")
            decision=False
        #requests.post('http://localhost:3000/post', json = { 'decision' : decision })
        badcounter = 0
        return ptg

# def processSites(ptg):
#     if ptg > 5: #value very low. 
#         backToWork()

# def backToWork(response):
#     print "All days are good days, even when they're bad days."

def get(stub, path_str, metadata):
    """Get and echo the response"""
    response = stub.Get(pyopenconfig.resources.make_get_request(path_str),
                        metadata=metadata)
    print(response)

def subscribe(stub, path_str, mode, metadata):
    logger.info("Client's subscribe method was called.")
    global nums
    """Subscribe and echo the stream"""
    logger.info("start to subscrib path: %s in %s mode" % (path_str, mode))
    subscribe_request = pyopenconfig.resources.make_subscribe_request(path_str=path_str, mode=mode)
    #iterator issue
    i = 500
    try:
        for response in stub.Subscribe(subscribe_request, metadata=metadata):
            ptg = processPacket(response)
            saveToTSDB(ptg, response)
            i += 500
            nums = i
    except grpc.framework.interfaces.face.face.AbortionError, error: # pylint: disable=catching-non-exception
        if error.code == grpc.StatusCode.OUT_OF_RANGE and error.details == 'EOF':
            # https://github.com/grpc/grpc/issues/7192
            sys.stderr.write('EOF after %d updates\n' % i)
            logger.info('EOF after %d updates\n' % i)
        else:
            raise

    logger.info("Finished streaming, %s updates has been streamed." % i)

def shutdown_hook():
    global nums
    try:
        pass
    except Exception:
        pass 
    finally:
        logger.info("%s updates has been streamed." % nums)
        logger.info('existing program')


def run():
    """Main loop"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost',
                        help='OpenConfig server host') #on mininet host's IP 
    parser.add_argument('--port', type=int, default=9033,
                        help='OpenConfig server port')
    parser.add_argument('--username', type=str, help='username')
    parser.add_argument('--password', type=str, help='password')
    parser.add_argument('--mode', type=str, default='stream', help='subscription mode')
    parser.add_argument('--debug', type=str, default='on', help='debug level')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--get',
                       help='OpenConfig path to perform a single-shot get')
    group.add_argument('--subscribe', type=str, default='interfaces/ethnet/state',
                       help='OpenConfig path to subscribe to')
    args = parser.parse_args()
    global path
    path = args.subscribe

    metadata = None
    if args.debug == "off":
        logger.setLevel(logging.INFO)
        
    if args.username or args.password:
        metadata = [("username", args.username), ("password", args.password)]

    channel = grpc.insecure_channel(args.host + ":" + str(args.port))
    stub = gnmi_pb2.gNMIStub(channel)

    atexit.register(shutdown_hook) 

    if args.get:
        get(stub, args.get, metadata)
    elif args.subscribe:
        subscribe(stub, args.subscribe, args.mode, metadata)
    else:
        subscribe(stub, '/', metadata)


if __name__ == '__main__':
    run()
