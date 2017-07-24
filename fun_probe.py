#!/usr/bin/env python
"""
pulls packet data, feeds to collector through gNMI

"""
import grpc
import gnmi.gnmi_pb2 as gnmi_pb2
import gnmi.gnmi_pb2_grpc as gnmi_pb2_grpc
from concurrent import futures
import time
import datetime
from random import randint
import argparse

import logging
import socket 

import scapy

# - logging configuration
logging.basicConfig()
logger = logging.getLogger('probe')

logger.setLevel(logging.DEBUG)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

host='localhost'
port=80049
time_frequency = 1.0

#gNMI service which provides all rpc calls for gNMI client 
class ProbeServicer(gnmi_pb2_grpc.gNMIServicer):
    
    def __init__(self):
       # createStreams()
       pass

    def createStreams():
        pass

    def getPacketData(self, path):
        packets = scapy.sniff(count=10)
        print packets
        return gnmi_pb2.Update(path=path, val=packets)

    def Subscribe(self, request_iterator, context):
        tag = 0
        for request in request_iterator:
            sublist = request.subscribe.subscription
            mode = request.subscribe.mode    
            while(1):
                update_msg = []
                for sub in sublist:
                    update_msg.append(update_msg=self.getPacketData(sub.path))
                tm = int(time.time() * 1000)
                notif = gnmi_pb2.Notification(timestamp=tm, update=update_msg)
                yield gnmi_pb2.SubscribeResponse(update=notif)
                if mode == 0:
                    continue
                else:
                    break
            if mode == 1:
                break
            print "waiting for new request"

        print "Streaming done: close channel"

def serve():
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', default='localhost',help='OpenConfig server host')
  parser.add_argument('--port', default=1080,help='OpenConfig server port')
  parser.add_argument('--time', default=1,help='data generating frequency')
  parser.add_argument('--debug', type=str, default='on', help='debug level')
  parser.add_argument('--interface', default='', help='interface for probe to sniff')

  args = parser.parse_args()

  global time_frequency
  global interface = args.interface

  time_frequency = float(args.time)

  if args.debug == "off":
       logger.setLevel(logging.INFO)

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  gnmi_pb2_grpc.add_gNMIServicer_to_server(
      ProbeServicer(), server)
  server.add_insecure_port(args.host + ":" + str(args.port))
  server.start()
  print "Probe Server Started...."
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()