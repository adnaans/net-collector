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

from scapy.all import *


# - logging configuration
logging.basicConfig()
logger = logging.getLogger('probe')

logger.setLevel(logging.DEBUG)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

host='localhost'
port=9030
time_frequency = 0.001

#gNMI service which provides all rpc calls for gNMI client 
class ProbeServicer(gnmi_pb2_grpc.gNMIServicer):
    
    def __init__(self):
       # createStreams()
       pass

    def createStreams():
        pass

    def getPacketData(self, path):
        packet = scapy.sniff(count=1)[0]
        
        ethernet = gnmi_pb2.Ethernet(dst=packet[scapy.Ether].dst, src=packet[scapy.Ether].src, type=packet[scapy.Ether].type)
        ipp = gnmi_pb2.IP(version=packet[scapy.IP].version, ihl=packet[scapy.IP].ihl, tos=packet[scapy.IP].tos,
                            len=packet[scapy.IP].len, id=packet[scapy.IP].id, flags=packet[scapy.IP].flags,
                            frag=packet[scapy.IP].frag, ttl=packet[scapy.IP].ttl, proto=packet[scapy.IP].proto,
                            chksum=packet[scapy.IP].chksum, src=packet[scapy.IP].src, dst=packet[scapy.IP].dst)
        tcp = gnmi_pb2.TCP(sport=packet[scapy.TCP].sport, dport=packet[scapy.TCP].dport, seq=packet[scapy.TCP].seq,
                            ack=packet[scapy.TCP].ack, dataofs=packet[scapy.TCP].dataofs, reserved=packet[scapy.TCP].reserved,
                            flags=packet[scapy.TCP].flags, window=packet[scapy.TCP].window, chksum=packet[scapy.TCP].chksum,
                            urgptr=packet[scapy.TCP].urgptr, options=packet[scapy.TCP].options)
        raw = gnmi_pb2.Raw(load=packet[scapy.Raw].load)
        gnmiPacket = gnmi_pb2.Packet(e=ethernet, i=ipp, t=tcp, r=raw)

        return gnmiPacket

        # packets = scapy.sniff(timeout=5)
        # gnmiPackets=[]
        # for packet in packets:
        #     ethernet = gnmi_pb2.Ethernet(dst=packet[scapy.Ether].dst, src=packet[scapy.Ether].src, type=packet[scapy.Ether].type)
        #     ipp = gnmi_pb2.IP(version=packet[scapy.IP].version, ihl=packet[scapy.IP].ihl, tos=packet[scapy.IP].tos,
        #                         len=packet[scapy.IP].len, id=packet[scapy.IP].id, flags=packet[scapy.IP].flags,
        #                         frag=packet[scapy.IP].frag, ttl=packet[scapy.IP].ttl, proto=packet[scapy.IP].proto,
        #                         chksum=packet[scapy.IP].chksum, src=packet[scapy.IP].src, dst=packet[scapy.IP].dst)
        #     tcp = gnmi_pb2.TCP(sport=packet[scapy.TCP].sport, dport=packet[scapy.TCP].dport, seq=packet[scapy.TCP].seq,
        #                         ack=packet[scapy.TCP].ack, dataofs=packet[scapy.TCP].dataofs, reserved=packet[scapy.TCP].reserved,
        #                         flags=packet[scapy.TCP].flags, window=packet[scapy.TCP].window, chksum=packet[scapy.TCP].chksum,
        #                         urgptr=packet[scapy.TCP].urgptr, options=packet[scapy.TCP].options)
        #     raw = gnmi_pb2.Raw(load=packet[scapy.Raw].load)
        #     gnmiPacket = gnmi_pb2.Packet(e=ethernet, i=ipp, t=tcp, r=raw)

        #     yield gnmiPacket
            
        #     gnmiPackets.append(gnmiPacket)
        # return gnmi_pb2.Update(path=path, val=gnmiPackets)

    def Subscribe(self, request_iterator, context):
        tag = 0
        for request in request_iterator:
            sublist = request.subscribe.subscription
            mode = request.subscribe.mode    
            while(1):
                update_msg = []
                for sub in sublist:
                    update_msg.append(self.getPacketData(sub.path))
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
  parser.add_argument('--port', default=9030,help='OpenConfig server port')
  parser.add_argument('--time', default=1,help='data generating frequency')
  parser.add_argument('--debug', type=str, default='on', help='debug level')
  parser.add_argument('--interface', default='', help='interface for probe to sniff')

  args = parser.parse_args()

  global time_frequency
  global interface 

  time_frequency = float(args.time)
  interface = args.interface

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