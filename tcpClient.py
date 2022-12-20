from common import check_run_code,is_there_same_port

import socket
import time
import signal
from os import sys
"""
Le client est un élément qui doit envoyer son message comme suit : EndPointAdrr/Message
"""
def sigint_handler(signum, frame):
    print("Exiting...")
    client_socket.close()
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    #check_run_code(sys.argv,2)
    port_to_use = int(sys.argv[1]) #Le client doit, pour le moment, savoir où se connecter
    end_point_port = sys.argv[2] #Le client doit connaitre l'adresse d'arrivé
    
    port_list = sys.argv[2:]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port_to_use))

    print('Client : Connected to server %d'%(port_to_use))
    while True:
        buffer_to_send = input()
        buffer_to_send = end_point_port+"/"+buffer_to_send
        client_socket.send(buffer_to_send.encode())
        
        data = client_socket.recv(1024)
        print(f'Received data: {data.decode()}')
