import sys

from texttable import Texttable

import smarthome_pb2
from TCPClient import TCPClient


class Client:

  def __init__(self):
    self.packet = smarthome_pb2.Packet()

    self.request_id = 0

    self.table = Texttable()
    self.table.add_row(['Option', 'Action'])
    self.table.add_row(['1', 'LISTAR TODOS'])
    self.table.add_row(['2', 'ATUAR EM UM ATUADOR'])
    self.table.add_row(['3', 'RECEBER STATUS DE UM SENSOR'])
    self.table.add_row(['0', 'SAIR'])

    self.tcp_client = TCPClient()
  
  def show_table(self):
    print(self.table.draw())

  @staticmethod
  def get_action(user_input):
    actions = {
      '1': 'list_things',
      '2': 'act_on_thing',
      '3': 'status_from_thing',
      '0': 'sair'
    }

    if user_input in actions:
      return actions.get(user_input)
    else:
      return False

  def list_things(self):
    """BEGIN REQ"""
    self.increment_request_id()

    self.packet.id = self.request_id
    self.packet.action = 'LIST'
    self.packet.content = b''

    req = self.packet.SerializeToString()
    
    self.tcp_client.send_request(req)
    """END REQ"""
    
    """BEGIN RES"""
    self.packet.ParseFromString(self.tcp_client.get_response())

    list_of_thigs = smarthome_pb2.ListOfThings()
    list_of_thigs.ParseFromString(self.packet.content)

    for coisa in list_of_thigs.coisas:
      print(coisa.nome)
    """END RES"""
  
  def act_on_thing(self):
    actuator_id = input('Actuator ID: ')

    """BEGIN REQ"""
    self.increment_request_id()

    self.packet.id = self.request_id
    self.packet.action = 'ACT'
    self.packet.content = actuator_id.encode()

    req = self.packet.SerializeToString()

    self.tcp_client.send_request(req)
    """END REQ"""

    """BEGIN RES"""
    self.packet.ParseFromString(self.tcp_client.get_response())
    print(self.packet.content.decode())
    """END RES"""
  
  def status_from_thing(self):
    # thing = input('Thing ID or \'ALL\' for the complete status list: ')
    
    """BEGIN REQ"""
    self.increment_request_id()

    self.packet.id = self.request_id
    self.packet.action = 'STATUS'
    self.packet.content = 'ALL'.encode()

    req = self.packet.SerializeToString()

    self.tcp_client.send_request(req)
    """END REQ"""

    """BEGIN RES"""
    self.packet.ParseFromString(self.tcp_client.get_response())
    
    list_of_thigs = smarthome_pb2.ListOfThings()
    list_of_thigs.ParseFromString(self.packet.content)

    for coisa in list_of_thigs.coisas:
      print("%s ---- %s" % (coisa.nome, coisa.status))
    """END RES"""

  def increment_request_id(self):
    self.request_id += 1

  def sair(self):
    self.tcp_client.close_connection()
    sys.exit(0)
