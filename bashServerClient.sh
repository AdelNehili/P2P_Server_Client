#!/bin/bash
clear
while read line; do
    gnome-terminal --geometry="40x24+0+0" -e "python3 tcpServer.py ${line}"
done < publicAdresseServer.txt
gnome-terminal --geometry="40x24+0+0" -e "python3 tcpServer.py ${line}"

sleep 0.5
gnome-terminal --geometry="132x24+100+0" -e "python3 tcpClient.py 50000"

exit 
