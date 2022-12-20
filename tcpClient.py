from common import check_run_code,is_there_same_port

import socket
import time
import signal
from os import sys

def sigint_handler(signum, frame):
    print("Exiting...")
    client_socket.close()
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    check_run_code(sys.argv)
    port_to_use = int(sys.argv[1])
    port_list = sys.argv[2:]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port_to_use))

    print('Client : Connected to server %d'%(port_to_use))
    while True:
        buffer_to_send = input()
        client_socket.send(buffer_to_send.encode())
        
        data = client_socket.recv(1024)
        print(f'Received data: {data.decode()}')
