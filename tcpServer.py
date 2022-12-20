from common import check_run_code,is_there_same_port
import socket
import threading
import signal
from os import sys

class ClientThread(threading.Thread):
    def __init__(self, port_list, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.port_list = port_list
        self.running = True

    def connect_to_other_server(self):

        #Pour le moment, le chaque server se connect qu'à un seul autre server
        other_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for relay in self.port_list:
          other_server_socket.connect(('localhost', relay))
          print("Thread : Connected to the relay:", relay)
        return other_server_socket


    def run(self):
        print("Thread : New client connected:", self.client_address)

        other_server_socket = self.connect_to_other_server()
        #print("Here it is my relay :", other_server_socket.getsockname()[1])
        #print("Here it is my Client :", self.client_socket)
        
        while self.running:
            data = self.client_socket.recv(1024)
            if not data:
              print("Voila la data recu : ", data.decode())
              break

            else:
              print("Client : ",data.decode())
              
              if other_server_socket.getsockname()[1] != 0:
                other_server_socket.send(data)
                data = other_server_socket.recv(1024)
                print(f'Received data: {data.decode()}')
              self.client_socket.send(data)

        self.client_socket.close()
        print("Client disconnected:", self.client_address)

def sigint_handler(signum, frame):
    print("Exiting...")
    server_socket.close()
    exit(0)




if __name__ == "__main__":
  check_run_code(sys.argv) #Exit si la liste en input n'est pas correct
  port_to_use = int(sys.argv[1])
  port_list = [int(x) for x in sys.argv[2:]]

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(('localhost', port_to_use))
  print("Server : Binded to the port : %d"%(port_to_use))
  server_socket.listen(5)

  signal.signal(signal.SIGINT, sigint_handler)

  while True:
      client_socket, client_address = server_socket.accept()
      client_thread = ClientThread(port_list,client_socket, client_address)
      client_thread.start()
