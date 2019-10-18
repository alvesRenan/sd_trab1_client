from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket

import smarthome_pb2


class ClientHandler(Thread):

  def __init__(self, client_socket):
    super(ClientHandler, self).__init__()
    
    # Tells when the thread must stop
    self._is_running = True

    self.packet = smarthome_pb2.Packet()
    
    self.client_socket = client_socket

    self.list_of_things = {'LAMP1':'DESLIGADA','PRES1':'VAZIO','TEMP1':'28'}

  def get_request(self):
    self.packet.ParseFromString(self.client_socket.recv(1024))
    
    print("GOT: {} {} {} from client.".format(
      self.packet.id, self.packet.action, self.packet.content))
  
  def send_response(self):
    # If req id is not 0 send the response
    if not self.packet.id == 0:

      if self.packet.action == 'LIST':
        thigs = smarthome_pb2.ListOfThings()
        for k, v in self.list_of_things.items():
          item = thigs.coisas.add()
          item.nome = k
          item.status = v
        
        res_content = thigs.SerializeToString()
      
      if self.packet.action == 'ACT':
        res_content = 'ACTED!'.encode()
      
      if self.packet.action == 'STATUS':
        res_content = 'MOCK STATUS!'.encode()
      
      self.packet.content = res_content

      r = self.packet.SerializeToString()
      self.client_socket.send(r)
    
    # else close the socket
    else:
      print("Close connection with client.")
      self.stop()
  
  def run(self):
    # Keeps looping until self.stop() is called
    while self._is_running:
      self.get_request()
      self.send_response()
  
  # Closes the thread execution
  def stop(self):
    self._is_running = False


class TCPMockServer:
  
  def __init__(self):
    self.server_socket =  socket(AF_INET, SOCK_STREAM)
    self.server_socket.bind(('', 1235))
    self.server_socket.listen()

    print("Server runnign ")

  def accept_clients(self):
    client_socket, addr = self.server_socket.accept()

    ClientHandler(client_socket).start()
  
  def stop(self):
    self.server_socket.close()


if __name__ == "__main__":
    mock = TCPMockServer()

    while True:
        mock.accept_clients()
