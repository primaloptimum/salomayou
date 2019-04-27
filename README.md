# salomayou
A tor like network that uses openvpn server and clients to route data through servers randomly in a way similar to a train rail.

read the documentation for an in depth look at the project

the project only works for linux, yet.

the project requires many improvments and I am still finding a better way to scale the project, but to host a server in the network or to create your own network simply run si.py and serversetup on the servers then run sui.py on a client server to connect the two servers together. the sui.py will be the client and the si will be the server.

to connect to the network I am hosting all you need is clientSetup, serverslist, ui.py, and dbth.py simply run clientSetup then head to /home/$USER/.GradProject and then run ui.py then type in the command sudo openvpn --config client.conf.
(IT IS RECOMMENDED TO RUN ui.py EVERYTIME YOU WANT TO CONNECT TO THE NETWORK TO CHANGE THE ENTRY POINT).
