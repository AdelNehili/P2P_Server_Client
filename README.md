# P2P_Server_Client
Ce projet est une forme basic du réseau TOR. L'idée est de créer un réseau server/relay afin de brouiller les pistes. Le client devra se connecter à un des relay et envoyer son message à ce relait qui fera en sorte que le paquet traverse bel et bien le réseau.<br />

Pour ce faire, nous pouvons ajouter un flag en début de message afin de connaitre l'adresse d'arrivée.<br />

Un fichier bash vous est mis à disposition afin de lancer un premier test de communication inter-processus au travers un réseau.<br />

Useful command lines for the project:<br />
&emsp; ps aux : permet d'afficher tous les process en cours avec leur PID<br />
&emsp;	ps -T -p PID : permet d'afficher tous les sub-process en cours avec du process correspondant au PID<br />

&emsp; kill -s SIGINT -P $(pidof code)<br />


=======
GITHUB
=======
Command lines: <br />
To clone/download: <br />
&emsp;	git clone -b branch_name git_link <br />
&emsp;	//git clone -b other_branch https://github.com/AdelNehili/P2P_Server_Client.git <br />


To update FROM github:<br />
&emsp;	git init <br />
&emsp;	git pull <br />


To update GITHUB: <br />
&emsp;	git init <br />
&emsp;	git add . <br />
&emsp;	git commit -m <br />
&emsp;	git push <br />


