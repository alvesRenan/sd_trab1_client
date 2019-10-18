from socket import AF_INET, SOCK_STREAM, socket


class TCPClient:
  
  def __init__(self):
    self.server_ip = '172.20.10.120'
    self.server_port = 5000

    self.client_socket = socket(AF_INET, SOCK_STREAM)
    self.client_socket.connect((self.server_ip, self.server_port))
  
  def send_request(self, message):
    self.client_socket.send(message)

  def get_response(self):
    return self.client_socket.recv(2048)

  def close_connection(self):
    self.client_socket.close()
