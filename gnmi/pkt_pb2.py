# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pkt.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import any_pb2 as any__pb2
import descriptor_pb2 as descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pkt.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\tpkt.proto\x1a\tany.proto\x1a\x10\x64\x65scriptor.proto\"P\n\x06Packet\x12\x14\n\x01\x65\x18\x01 \x01(\x0b\x32\t.Ethernet\x12\x0e\n\x01i\x18\x02 \x01(\x0b\x32\x03.IP\x12\x0f\n\x01t\x18\x03 \x01(\x0b\x32\x04.TCP\x12\x0f\n\x01r\x18\x04 \x01(\x0b\x32\x04.Raw\"2\n\x08\x45thernet\x12\x0b\n\x03\x64st\x18\x01 \x01(\t\x12\x0b\n\x03src\x18\x02 \x01(\t\x12\x0c\n\x04type\x18\x03 \x01(\x05\"\xab\x01\n\x02IP\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12\x0b\n\x03ihl\x18\x02 \x01(\x03\x12\x0b\n\x03tos\x18\x03 \x01(\x03\x12\x0b\n\x03len\x18\x04 \x01(\x03\x12\n\n\x02id\x18\x05 \x01(\x03\x12\r\n\x05\x66lags\x18\x06 \x01(\x03\x12\x0c\n\x04\x66rag\x18\x07 \x01(\x03\x12\x0b\n\x03ttl\x18\x08 \x01(\x03\x12\r\n\x05proto\x18\t \x01(\x03\x12\x0e\n\x06\x63hksum\x18\n \x01(\x03\x12\x0b\n\x03\x64st\x18\x0b \x01(\t\x12\x0b\n\x03src\x18\x0c \x01(\t\"\x9f\x01\n\x03TCP\x12\r\n\x05sport\x18\x01 \x01(\x03\x12\r\n\x05\x64port\x18\x02 \x01(\x03\x12\x0b\n\x03seq\x18\x03 \x01(\x03\x12\x0b\n\x03\x61\x63k\x18\x04 \x01(\x03\x12\x0f\n\x07\x64\x61taofs\x18\x05 \x01(\x03\x12\x10\n\x08reserved\x18\x06 \x01(\x03\x12\r\n\x05\x66lags\x18\x07 \x01(\x03\x12\x0e\n\x06window\x18\x08 \x01(\x03\x12\x0e\n\x06\x63hksum\x18\t \x01(\x03\x12\x0e\n\x06urgptr\x18\n \x01(\x03\"\x13\n\x03Raw\x12\x0c\n\x04load\x18\x01 \x01(\t\"\"\n\x0bIpPairBatch\x12\x13\n\x02ip\x18\x01 \x03(\x0b\x32\x07.IpPair\"#\n\x06IpPair\x12\x0b\n\x03src\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x65st\x18\x02 \x01(\tb\x06proto3')
  ,
  dependencies=[any__pb2.DESCRIPTOR,descriptor__pb2.DESCRIPTOR,])




_PACKET = _descriptor.Descriptor(
  name='Packet',
  full_name='Packet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='e', full_name='Packet.e', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i', full_name='Packet.i', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='t', full_name='Packet.t', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='r', full_name='Packet.r', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=122,
)


_ETHERNET = _descriptor.Descriptor(
  name='Ethernet',
  full_name='Ethernet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dst', full_name='Ethernet.dst', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='src', full_name='Ethernet.src', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='Ethernet.type', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=124,
  serialized_end=174,
)


_IP = _descriptor.Descriptor(
  name='IP',
  full_name='IP',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='IP.version', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ihl', full_name='IP.ihl', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tos', full_name='IP.tos', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='len', full_name='IP.len', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='IP.id', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flags', full_name='IP.flags', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frag', full_name='IP.frag', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ttl', full_name='IP.ttl', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proto', full_name='IP.proto', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chksum', full_name='IP.chksum', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dst', full_name='IP.dst', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='src', full_name='IP.src', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=177,
  serialized_end=348,
)


_TCP = _descriptor.Descriptor(
  name='TCP',
  full_name='TCP',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sport', full_name='TCP.sport', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dport', full_name='TCP.dport', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq', full_name='TCP.seq', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ack', full_name='TCP.ack', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dataofs', full_name='TCP.dataofs', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reserved', full_name='TCP.reserved', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flags', full_name='TCP.flags', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='window', full_name='TCP.window', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chksum', full_name='TCP.chksum', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='urgptr', full_name='TCP.urgptr', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=351,
  serialized_end=510,
)


_RAW = _descriptor.Descriptor(
  name='Raw',
  full_name='Raw',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='load', full_name='Raw.load', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=512,
  serialized_end=531,
)


_IPPAIRBATCH = _descriptor.Descriptor(
  name='IpPairBatch',
  full_name='IpPairBatch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='IpPairBatch.ip', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=533,
  serialized_end=567,
)


_IPPAIR = _descriptor.Descriptor(
  name='IpPair',
  full_name='IpPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='src', full_name='IpPair.src', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dest', full_name='IpPair.dest', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=569,
  serialized_end=604,
)

_PACKET.fields_by_name['e'].message_type = _ETHERNET
_PACKET.fields_by_name['i'].message_type = _IP
_PACKET.fields_by_name['t'].message_type = _TCP
_PACKET.fields_by_name['r'].message_type = _RAW
_IPPAIRBATCH.fields_by_name['ip'].message_type = _IPPAIR
DESCRIPTOR.message_types_by_name['Packet'] = _PACKET
DESCRIPTOR.message_types_by_name['Ethernet'] = _ETHERNET
DESCRIPTOR.message_types_by_name['IP'] = _IP
DESCRIPTOR.message_types_by_name['TCP'] = _TCP
DESCRIPTOR.message_types_by_name['Raw'] = _RAW
DESCRIPTOR.message_types_by_name['IpPairBatch'] = _IPPAIRBATCH
DESCRIPTOR.message_types_by_name['IpPair'] = _IPPAIR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Packet = _reflection.GeneratedProtocolMessageType('Packet', (_message.Message,), dict(
  DESCRIPTOR = _PACKET,
  __module__ = 'pkt_pb2'
  # @@protoc_insertion_point(class_scope:Packet)
  ))
_sym_db.RegisterMessage(Packet)

Ethernet = _reflection.GeneratedProtocolMessageType('Ethernet', (_message.Message,), dict(
  DESCRIPTOR = _ETHERNET,
  __module__ = 'pkt_pb2'
  # @@protoc_insertion_point(class_scope:Ethernet)
  ))
_sym_db.RegisterMessage(Ethernet)

IP = _reflection.GeneratedProtocolMessageType('IP', (_message.Message,), dict(
  DESCRIPTOR = _IP,
  __module__ = 'pkt_pb2'
  # @@protoc_insertion_point(class_scope:IP)
  ))
_sym_db.RegisterMessage(IP)

TCP = _reflection.GeneratedProtocolMessageType('TCP', (_message.Message,), dict(
  DESCRIPTOR = _TCP,
  __module__ = 'pkt_pb2'
  # @@protoc_insertion_point(class_scope:TCP)
  ))
_sym_db.RegisterMessage(TCP)

Raw = _reflection.GeneratedProtocolMessageType('Raw', (_message.Message,), dict(
  DESCRIPTOR = _RAW,
  __module__ = 'pkt_pb2'
  # @@protoc_insertion_point(class_scope:Raw)
  ))
_sym_db.RegisterMessage(Raw)

IpPairBatch = _reflection.GeneratedProtocolMessageType('IpPairBatch', (_message.Message,), dict(
  DESCRIPTOR = _IPPAIRBATCH,
  __module__ = 'pkt_pb2'
  # @@protoc_insertion_point(class_scope:IpPairBatch)
  ))
_sym_db.RegisterMessage(IpPairBatch)

IpPair = _reflection.GeneratedProtocolMessageType('IpPair', (_message.Message,), dict(
  DESCRIPTOR = _IPPAIR,
  __module__ = 'pkt_pb2'
  # @@protoc_insertion_point(class_scope:IpPair)
  ))
_sym_db.RegisterMessage(IpPair)


# @@protoc_insertion_point(module_scope)
