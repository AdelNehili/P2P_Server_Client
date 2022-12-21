from common import check_run_code,is_there_same_port
import socket
import threading
import signal
import random
from os import sys

class ClientThread(threading.Thread):
    def __init__(self,port_to_use,port_list, client_socket, client_address):
        threading.Thread.__init__(self)
        self.port_to_use = port_to_use
        self.port_list = port_list
        self.client_socket = client_socket
        self.client_address = client_address
        
        self.running = True

    def connect_to_other_server(self):

        #Pour le moment, le chaque server se connect qu'à un seul autre server
        other_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for relay in self.port_list:
          other_server_socket.connect(('localhost', relay))
          print("Thread : Connected to the relay:", relay)
        return other_server_socket
    def increment_hop():
      
    def run(self):
        print("Thread : New client connected:", self.client_address)

        other_server_socket = self.connect_to_other_server()
        #print("Here it is my relay :", other_server_socket.getsockname()[1])
        #print("Here it is my Client :", self.client_socket)
        
        while self.running:
            data = self.client_socket.recv(1024)
            if not data:
              break
            else:
              decoded_data = data.decode()
              [end_point,hops,message] = decoded_data.split("/")
              print("end_point/hops/message : %s/%s/%s"%(end_point,hops,message))

              new_hops= int(hops)+1
              data = (end_point+"/"+str(new_hops)+"/"+message).encode()
              
              if end_point == str(self.port_to_use):
                #Si le server en cours est le point d'arrivé
                print("MI TSU KE TA! Hehe je vais changer ton message!!!")
                data = "Nyak nyak nyak que je suis vil!".encode()
              else:
                if other_server_socket.getsockname()[1] != 0:
                  #Verifie que le port soit diff. de zero, c'est à dire que l'élément choisit pour other_server_socket ne soit pas vide
                  other_server_socket.send(data)
                  data = other_server_socket.recv(1024)
                  print(f'Received data: {data.decode()} \n')
              self.client_socket.send(data)

        self.client_socket.close()
        print("Client disconnected:", self.client_address)


def sigint_handler(signum, frame):
    print("Exiting...")
    server_socket.close()
    exit(0)


def add_my_port(port_to_use):
  file = open("publicAdresseServer.txt","a")
  file.write(str(port_to_use)+"\n")
  file.close()

def choose_a_port(my_port):
  port_list= []
  file = open("publicAdresseServer.txt","r")
  lines = file.readlines()
  rand_index = random.randint(0,len(lines)-1)
  while my_port == int(lines[rand_index].strip()):
    rand_index = random.randint(0,len(lines)-1)
  file.close()
  port_list.append(int(lines[rand_index].strip()))
  return port_list


if __name__ == "__main__":
  #check_run_code(sys.argv) #Exit si la liste en input n'est pas correct
  port_to_use = int(sys.argv[1])
  
  port_list = [int(x) for x in sys.argv[2:]]
  
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  ### Attention, cette partie ne sert QUE si on veut randomiser ###
  not_okay = True
  while not_okay:
    try:
      server_socket.bind(('localhost', port_to_use))
      not_okay = False
    except socket.error as e:
      port_to_use = random.randint(49000,65000)
  #add_my_port(port_to_use)
  #################################################################

  print("Server : Binded to the port : %d"%(port_to_use))
  server_socket.listen(5)

  signal.signal(signal.SIGINT, sigint_handler)

  while True:
      client_socket, client_address = server_socket.accept()
      client_thread = ClientThread(port_to_use,port_list,client_socket, client_address)
      client_thread.start()
