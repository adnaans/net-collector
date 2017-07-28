import argparse
import logging
import sys
import time

import grpc.framework.interfaces.face
import pyopenconfig.gnmi_pb2
import pyopenconfig.resources

import atexit
from scapy.all import *

import requests

# - logging configuration
logging.basicConfig()
logger = logging.getLogger('netclient')

logger.setLevel(logging.DEBUG)

host_ip = "" #h4.IP()
host_port = 9033

mode = "stream"
nums = 0

#db_host = 'localhost'
#db_port = 4242
#metrics = potsdb.Client(db_host, port=db_port)

counter = 0

badsites= {"facebook.com", "www.twitter.com", "www.reddit.com"} 

def encodePath(path):
    pathStrs = "" 
    for pe in path:
        pstr = pe.name
        if pe.key:
             for k, v in pe.key.iteritems():
                  pstr += "[" + str(k) + "=" + str(v) + "]"
        pathStrs = pathStrs + "." + pstr
    return pathStrs[1:]

def processPacket(response): #HAVE TO FIX THIS METHOD TO DEAL WITH AN IPPAIRBATCH OF ip string pairs 
    for update in response.update.update:
        path_metric = encodePath(update.path.elem)
        tm = response.update.timestamp
        pairs = update.val
        print(pairs)
        for pair in pairs: 
            if(pair.src() in badsites or pair.dst() in badsites or pair.src()=="10.0.0.1" or pair.dst()=="10.0.0.1"): #consider hashset
                badcounter=badcounter+1
        
        requests.post('http://localhost:3000/post', json = { 'ptg' : badcounter/(len(pairs))*100 })
        badcounter = 0

# def backToWork():
#     print("this happened! events ARE registering...LIFE IS EXCITING." +
#             "there's always more to see, do, and feel. and the world is" +
#             "so big compared to the people in it. and the universe is so big" +
#             "compared to the world.")


def get(stub, path_str, metadata):
    """Get and echo the response"""
    response = stub.Get(pyopenconfig.resources.make_get_request(path_str),
                        metadata=metadata)
    print(response)

def subscribe(stub, path_str, mode, metadata):
    global nums
    """Subscribe and echo the stream"""
    logger.info("start to subscrib path: %s in %s mode" % (path_str, mode))
    subscribe_request = pyopenconfig.resources.make_subscribe_request(path_str=path_str, mode=mode)
    i = 500
    try:
        for response in stub.Subscribe(subscribe_request, metadata=metadata):
            logger.debug(response)
            processPacket(response)
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
    group.add_argument('--subscribe', type=str, default='interfaces/eth0/ip',
                       help='OpenConfig path to subscribe to')
    args = parser.parse_args()

    metadata = None
    if args.debug == "off":
        logger.setLevel(logging.INFO)
        
    if args.username or args.password:
        metadata = [("username", args.username), ("password", args.password)]

    channel = grpc.insecure_channel(args.host + ":" + str(args.port))
    stub = pyopenconfig.gnmi_pb2.gNMIStub(channel)

    atexit.register(shutdown_hook) 

    if args.get:
        get(stub, args.get, metadata)
    elif args.subscribe:
        subscribe(stub, args.subscribe, args.mode, metadata)
    else:
        subscribe(stub, '/', metadata)


if __name__ == '__main__':
    run()
