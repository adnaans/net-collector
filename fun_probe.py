#!/usr/bin/env python
"""
pulls packet data, feeds to collector through gNMI

"""
import grpc
import gnmi.gnmi_pb2 as gnmi_pb2
import gnmi.gnmi_pb2_grpc as gnmi_pb2_grpc
import gnmi.pkt_pb2 as pkt_pb2
from google.protobuf import any_pb2

from concurrent import futures
import time
import datetime
from random import randint
import argparse

import logging

from scapy import all as scapy

# - logging configuration
logging.basicConfig()
logger = logging.getLogger('probe')

logger.setLevel(logging.DEBUG)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

host='localhost'
port=9030
time_frequency = 1


class ProbeServicer(gnmi_pb2_grpc.gNMIServicer):
    
    def __init__(self):
       pass

    def getPacketData(self):
        #sniff one packet on eth1 interface
        packet = scapy.sniff(iface="eth1",count=1)[0] 
        #take all attributes of scapy packet & put into protobuf model if there
        if packet:
          if scapy.Ether in packet:
              ethernet = pkt_pb2.Ethernet(dst=packet[scapy.Ether].dst, src=packet[scapy.Ether].src, type=packet[scapy.Ether].type)
          else:
              ethernet = None
          if scapy.IP in packet:
              ipp = pkt_pb2.IP(version=packet[scapy.IP].version, ihl=packet[scapy.IP].ihl, tos=packet[scapy.IP].tos,
                                len=packet[scapy.IP].len, id=packet[scapy.IP].id, flags=packet[scapy.IP].flags,
                                frag=packet[scapy.IP].frag, ttl=packet[scapy.IP].ttl, proto=packet[scapy.IP].proto,
                                chksum=packet[scapy.IP].chksum, src=packet[scapy.IP].src, dst=packet[scapy.IP].dst)
          else:
              ipp = None
          if scapy.TCP in packet:
              tcp = pkt_pb2.TCP(sport=packet[scapy.TCP].sport, dport=packet[scapy.TCP].dport, seq=packet[scapy.TCP].seq,
                                ack=packet[scapy.TCP].ack, dataofs=packet[scapy.TCP].dataofs, reserved=packet[scapy.TCP].reserved,
                                flags=packet[scapy.TCP].flags, window=packet[scapy.TCP].window, chksum=packet[scapy.TCP].chksum)
          else:
              tcp = None
          if scapy.Raw in packet:
              raw = pkt_pb2.Raw(load=packet[scapy.Raw].load) 
          else:
              raw = None
          gnmiPacket = pkt_pb2.Packet(e=ethernet, i=ipp, t=tcp, r=raw)
          any_msg = any_pb2.Any()
          any_msg.Pack(gnmiPacket) #send Packet message through google.protobuf.Any
          typedVal = gnmi_pb2.TypedValue(any_val=any_msg)
          update = gnmi_pb2.Update(val=typedVal) 
          return update

    def Subscribe(self, request_iterator, context): 
        logger.info("Probe has received a subscribe request.")  
        while(1):
            update_msg = []
            update_msg.append(self.getPacketData())
            tm = int(time.time() * 1000)
            notif = gnmi_pb2.Notification(timestamp=tm, update=update_msg)
            print "sent an update."
            yield gnmi_pb2.SubscribeResponse(update=notif)
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