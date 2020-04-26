# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: private_api.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='private_api.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x11private_api.proto\"9\n\x11\x45valuationRequest\x12\x16\n\x0e\x63hallenge_name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\"!\n\x0f\x45valuationReply\x12\x0e\n\x06result\x18\x01 \x01(\t\",\n\x0b\x45xecRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0f\n\x07options\x18\x02 \x01(\t\"\x1b\n\tExecReply\x12\x0e\n\x06result\x18\x01 \x01(\t\"0\n\x11WriteStdinRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"!\n\x0fWriteStdinReply\x12\x0e\n\x06result\x18\x01 \x01(\t\"\x1e\n\x10TerminateRequest\x12\n\n\x02id\x18\x01 \x01(\t\" \n\x0eTerminateReply\x12\x0e\n\x06output\x18\x01 \x01(\t2?\n\x07Manager\x12\x34\n\nEvaluation\x12\x12.EvaluationRequest\x1a\x10.EvaluationReply\"\x00\x32\x9a\x01\n\x0bSandboxExec\x12\"\n\x04\x45xec\x12\x0c.ExecRequest\x1a\n.ExecReply\"\x00\x12\x34\n\nWriteStdin\x12\x12.WriteStdinRequest\x1a\x10.WriteStdinReply\"\x00\x12\x31\n\tTerminate\x12\x11.TerminateRequest\x1a\x0f.TerminateReply\"\x00\x62\x06proto3'
)




_EVALUATIONREQUEST = _descriptor.Descriptor(
  name='EvaluationRequest',
  full_name='EvaluationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='challenge_name', full_name='EvaluationRequest.challenge_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='code', full_name='EvaluationRequest.code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=78,
)


_EVALUATIONREPLY = _descriptor.Descriptor(
  name='EvaluationReply',
  full_name='EvaluationReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='EvaluationReply.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=113,
)


_EXECREQUEST = _descriptor.Descriptor(
  name='ExecRequest',
  full_name='ExecRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='ExecRequest.code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='options', full_name='ExecRequest.options', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=115,
  serialized_end=159,
)


_EXECREPLY = _descriptor.Descriptor(
  name='ExecReply',
  full_name='ExecReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='ExecReply.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=161,
  serialized_end=188,
)


_WRITESTDINREQUEST = _descriptor.Descriptor(
  name='WriteStdinRequest',
  full_name='WriteStdinRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='WriteStdinRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='WriteStdinRequest.content', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=238,
)


_WRITESTDINREPLY = _descriptor.Descriptor(
  name='WriteStdinReply',
  full_name='WriteStdinReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='WriteStdinReply.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=240,
  serialized_end=273,
)


_TERMINATEREQUEST = _descriptor.Descriptor(
  name='TerminateRequest',
  full_name='TerminateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='TerminateRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=275,
  serialized_end=305,
)


_TERMINATEREPLY = _descriptor.Descriptor(
  name='TerminateReply',
  full_name='TerminateReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='output', full_name='TerminateReply.output', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=307,
  serialized_end=339,
)

DESCRIPTOR.message_types_by_name['EvaluationRequest'] = _EVALUATIONREQUEST
DESCRIPTOR.message_types_by_name['EvaluationReply'] = _EVALUATIONREPLY
DESCRIPTOR.message_types_by_name['ExecRequest'] = _EXECREQUEST
DESCRIPTOR.message_types_by_name['ExecReply'] = _EXECREPLY
DESCRIPTOR.message_types_by_name['WriteStdinRequest'] = _WRITESTDINREQUEST
DESCRIPTOR.message_types_by_name['WriteStdinReply'] = _WRITESTDINREPLY
DESCRIPTOR.message_types_by_name['TerminateRequest'] = _TERMINATEREQUEST
DESCRIPTOR.message_types_by_name['TerminateReply'] = _TERMINATEREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EvaluationRequest = _reflection.GeneratedProtocolMessageType('EvaluationRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATIONREQUEST,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:EvaluationRequest)
  })
_sym_db.RegisterMessage(EvaluationRequest)

EvaluationReply = _reflection.GeneratedProtocolMessageType('EvaluationReply', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATIONREPLY,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:EvaluationReply)
  })
_sym_db.RegisterMessage(EvaluationReply)

ExecRequest = _reflection.GeneratedProtocolMessageType('ExecRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXECREQUEST,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:ExecRequest)
  })
_sym_db.RegisterMessage(ExecRequest)

ExecReply = _reflection.GeneratedProtocolMessageType('ExecReply', (_message.Message,), {
  'DESCRIPTOR' : _EXECREPLY,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:ExecReply)
  })
_sym_db.RegisterMessage(ExecReply)

WriteStdinRequest = _reflection.GeneratedProtocolMessageType('WriteStdinRequest', (_message.Message,), {
  'DESCRIPTOR' : _WRITESTDINREQUEST,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:WriteStdinRequest)
  })
_sym_db.RegisterMessage(WriteStdinRequest)

WriteStdinReply = _reflection.GeneratedProtocolMessageType('WriteStdinReply', (_message.Message,), {
  'DESCRIPTOR' : _WRITESTDINREPLY,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:WriteStdinReply)
  })
_sym_db.RegisterMessage(WriteStdinReply)

TerminateRequest = _reflection.GeneratedProtocolMessageType('TerminateRequest', (_message.Message,), {
  'DESCRIPTOR' : _TERMINATEREQUEST,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:TerminateRequest)
  })
_sym_db.RegisterMessage(TerminateRequest)

TerminateReply = _reflection.GeneratedProtocolMessageType('TerminateReply', (_message.Message,), {
  'DESCRIPTOR' : _TERMINATEREPLY,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:TerminateReply)
  })
_sym_db.RegisterMessage(TerminateReply)



_MANAGER = _descriptor.ServiceDescriptor(
  name='Manager',
  full_name='Manager',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=341,
  serialized_end=404,
  methods=[
  _descriptor.MethodDescriptor(
    name='Evaluation',
    full_name='Manager.Evaluation',
    index=0,
    containing_service=None,
    input_type=_EVALUATIONREQUEST,
    output_type=_EVALUATIONREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MANAGER)

DESCRIPTOR.services_by_name['Manager'] = _MANAGER


_SANDBOXEXEC = _descriptor.ServiceDescriptor(
  name='SandboxExec',
  full_name='SandboxExec',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=407,
  serialized_end=561,
  methods=[
  _descriptor.MethodDescriptor(
    name='Exec',
    full_name='SandboxExec.Exec',
    index=0,
    containing_service=None,
    input_type=_EXECREQUEST,
    output_type=_EXECREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='WriteStdin',
    full_name='SandboxExec.WriteStdin',
    index=1,
    containing_service=None,
    input_type=_WRITESTDINREQUEST,
    output_type=_WRITESTDINREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Terminate',
    full_name='SandboxExec.Terminate',
    index=2,
    containing_service=None,
    input_type=_TERMINATEREQUEST,
    output_type=_TERMINATEREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SANDBOXEXEC)

DESCRIPTOR.services_by_name['SandboxExec'] = _SANDBOXEXEC

# @@protoc_insertion_point(module_scope)
