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
  serialized_pb=b'\n\x11private_api.proto\"9\n\x11\x45valuationRequest\x12\x16\n\x0e\x63hallenge_name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\"!\n\x0f\x45valuationReply\x12\x0e\n\x06result\x18\x01 \x01(\t\"3\n\x12SandboxExecRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0f\n\x07options\x18\x02 \x01(\t\"\"\n\x10SandboxExecReply\x12\x0e\n\x06result\x18\x01 \x01(\t2?\n\x07Manager\x12\x34\n\nEvaluation\x12\x12.EvaluationRequest\x1a\x10.EvaluationReply\"\x00\x32\x46\n\x0bSandboxExec\x12\x37\n\x0bSandboxExec\x12\x13.SandboxExecRequest\x1a\x11.SandboxExecReply\"\x00\x62\x06proto3'
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


_SANDBOXEXECREQUEST = _descriptor.Descriptor(
  name='SandboxExecRequest',
  full_name='SandboxExecRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='SandboxExecRequest.code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='options', full_name='SandboxExecRequest.options', index=1,
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
  serialized_end=166,
)


_SANDBOXEXECREPLY = _descriptor.Descriptor(
  name='SandboxExecReply',
  full_name='SandboxExecReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='SandboxExecReply.result', index=0,
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
  serialized_start=168,
  serialized_end=202,
)

DESCRIPTOR.message_types_by_name['EvaluationRequest'] = _EVALUATIONREQUEST
DESCRIPTOR.message_types_by_name['EvaluationReply'] = _EVALUATIONREPLY
DESCRIPTOR.message_types_by_name['SandboxExecRequest'] = _SANDBOXEXECREQUEST
DESCRIPTOR.message_types_by_name['SandboxExecReply'] = _SANDBOXEXECREPLY
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

SandboxExecRequest = _reflection.GeneratedProtocolMessageType('SandboxExecRequest', (_message.Message,), {
  'DESCRIPTOR' : _SANDBOXEXECREQUEST,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:SandboxExecRequest)
  })
_sym_db.RegisterMessage(SandboxExecRequest)

SandboxExecReply = _reflection.GeneratedProtocolMessageType('SandboxExecReply', (_message.Message,), {
  'DESCRIPTOR' : _SANDBOXEXECREPLY,
  '__module__' : 'private_api_pb2'
  # @@protoc_insertion_point(class_scope:SandboxExecReply)
  })
_sym_db.RegisterMessage(SandboxExecReply)



_MANAGER = _descriptor.ServiceDescriptor(
  name='Manager',
  full_name='Manager',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=204,
  serialized_end=267,
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
  serialized_start=269,
  serialized_end=339,
  methods=[
  _descriptor.MethodDescriptor(
    name='SandboxExec',
    full_name='SandboxExec.SandboxExec',
    index=0,
    containing_service=None,
    input_type=_SANDBOXEXECREQUEST,
    output_type=_SANDBOXEXECREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SANDBOXEXEC)

DESCRIPTOR.services_by_name['SandboxExec'] = _SANDBOXEXEC

# @@protoc_insertion_point(module_scope)
