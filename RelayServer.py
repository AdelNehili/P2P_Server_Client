from common import check_run_code,is_there_same_port
import socket
import threading
import signal
import random
import sys

class ClientThread(threading.Thread):
    def __init__(self,next_relay, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.next_relay = next_relay
        self.running = True

    def connect_to_other_server(self):

        #Pour le moment, le chaque server se connect qu'à un seul autre server
        if self.next_relay != None:
          other_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          other_server_socket.connect(('localhost', self.next_relay))
          print("Thread : Connected to the relay:", self.next_relay)
          return other_server_socket
        
    def change_my_data(self,data_decoded):
      my_data_list = data_decoded.split("/")
      buffer_to_send =""
      if len(my_data_list) !=0:
        #print("Avant :", my_data_list)
        del my_data_list[0]
        #print("Apres :", my_data_list)
        for index,element in enumerate(my_data_list):
            if index == len(my_data_list)-1:
              buffer_to_send += element
            else:
              buffer_to_send += element+"/"
      return buffer_to_send
      
    def connect_to_other_server_bis(self,next_relay):

        other_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        other_server_socket.connect(('localhost', int(next_relay)))
        print("Thread : Connected to the relay:", next_relay)
        return other_server_socket

    def run(self):
        print("Thread : New client connected:", self.client_address)


        #print("Here it is my relay :", other_server_socket.getsockname()[1])
        #print("Here it is my Client :", self.client_socket)
        
        while self.running:
            data = self.client_socket.recv(1024)
            
            if not data:
              print("Voila la data recu : ", data.decode())
              break

            else:
              decoded_data = data.decode()
              splitted_data = decoded_data.split("/")
              print("Client : ",splitted_data, "len :",len(splitted_data))
              if len(splitted_data)!=1:
                next_relay = data.decode().split("/")[0]
                print("Si j'ai bien capte, c'est ca mon relait :", next_relay)
                other_server_socket = self.connect_to_other_server_bis(next_relay)
                decoded_data = self.change_my_data(decoded_data)
                data = decoded_data.encode()
              else:
                next_relay = None

              if next_relay != None:
                if other_server_socket.getsockname()[0]!=0:
                  other_server_socket.send(data)
                  data = other_server_socket.recv(1024)
                  print(f'Received data: {data.decode()} \n')
              else:
                #Pour l'instant on def. l'adresse d'arrivé comme étant le dernier point du message
                print("HEHEH TE VOILA A LA FIN DU CHEMIN! Je vais changer ton message!")
                message_warui = "Trouve!"
                data = message_warui.encode()
              self.client_socket.send(data)

        self.client_socket.close()
        print("Client disconnected:", self.client_address)

def sigint_handler(signum, frame):
    #Permet une déconnexion propre avec SIGINT
    print("Exiting...")
    server_socket.close()
    exit(0)


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
  next_relay = None
  port_to_use = int(sys.argv[1])
  if len(sys.argv)>=3:
    next_relay = int(sys.argv[2])
  print("Voici les adresses qui m'interressent : %s %s"%(port_to_use,next_relay))
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  not_okay = True 
  while not_okay:
    #Pour l'instant, ça ne sert à rien puique les ports sont donnés à l'appel des fonctions
    try:
      server_socket.bind(('localhost', port_to_use))
      not_okay = False
    except socket.error as e:
      port_to_use = random.randint(49000,65000)


  print("Server : Binded to the port : %d"%(port_to_use))
  server_socket.listen(5)

  signal.signal(signal.SIGINT, sigint_handler)

  while True:
      client_socket, client_address = server_socket.accept()
      client_thread = ClientThread(next_relay=next_relay,client_socket= client_socket,client_address= client_address)
      client_thread.start()
