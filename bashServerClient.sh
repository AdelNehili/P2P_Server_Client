#!/bin/bash
clear
#python3 cleaner.py

while read line; do
    gnome-terminal --geometry="40x24+0+0" -e "python3 tcpServer.py ${line}"
done < publicAdresseServer.txt

gnome-terminal --geometry="40x24+0+0" -e "python3 tcpServer.py ${line}"

gnome-terminal --geometry="132x24+100+0" -e "python3 tcpClient.py 50000 50100 50102"

exit 

#python3 tcpServer.py 50000 67000