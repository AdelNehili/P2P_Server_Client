#!/bin/bash

clear

gnome-terminal --geometry="40x24+0+0" -e "python3 tcpServer.py 4545"
gnome-terminal --geometry="40x24+0+0" -e "python3 tcpServer.py 8000"
sleep 0.5
gnome-terminal --geometry="132x24+100+0" -e "python3 tcpClient.py 4545"

exit 
