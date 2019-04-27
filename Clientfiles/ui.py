#!/usr/bin/python3
import os
from getpass import getuser
import sys
import subprocess
import socket
import dbth
import pexpect

buffer=100000

ServIp=''

#check if PKI file exists if not creates one
if os.path.exists(True):
    print("pki file exists\n")

else:
    print("please run clientSetup first")
    exit()


serverNum = dbth.dbth(3) #randomly chooses a server
serverFile = open("serverslist")
for i, line in enumerate(serverFile):
    if i == serverNum:
        ServIp=line[:-1]

print(ServIp)
#create configurations
config='client\ntls-client\nproto tcp\ncipher server1\ncipher AES-128-CBC\nremote ' + str(ServIp) + ' 119' + str(serverNum) + '\ndev tun\nnobind\nremote-cert-tls server\nca ca.crt\ncert client.crt\nkey client.key\nremote-cert-tls server\npersist-key\npersist-tun\nresolv-retry infinite'

if os.path.exists(""+ServIp): #check if server file exists
    print("ip address file exists")
    bashCommand = "cp " + ServIp + "/ca.crt ." #copy ca certificate to the outside of the server directory
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand = "cp " + ServIp + "/client.crt ." #copy client certificate to the outside of the server directory
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand = "cp " + ServIp + "/client.key ." #copy client key to the outside of the server directory
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand = "cp " + ServIp + "/client.conf ." #copy client config to the outside of the server directory
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

else:

    bashCommand = "/home/"+ getuser() + "/easy-rsa/easyrsa3/easyrsa gen-req client nopass" #generate a request to send to server
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd="/home/" + getuser() + "/easy-rsa/easyrsa3")
    output, error = process.communicate()

    bashCommand = "mkdir "+ServIp #create directory for server
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand = "mv /home/" + getuser() + "/easy-rsa/easyrsa3/pki/private/client.key ." #move client key file to current directory
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand = "mv /home/" + getuser() + "/easy-rsa/easyrsa3/pki/reqs/client.req ./"+ServIp #move request file to server directory
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ServIp, 5000))

    request = open(ServIp+"/client.req", "r")
    data = request.read()

    s.send("Req".encode('utf-8'))
    if s.recv(1).decode('ascii') == "1":
        s.send(data.encode('utf-8'))
        data = s.recv(3).decode('ascii')
        if data == "crt":
            print("\nThe password is 123\n")
            bashCommand = "scp client@" + ServIp + ":client.crt ." #obtain client certificate
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            print("\nThe password is 123\n")
            s.send("1".encode('utf-8'))
            if "ca" == s.recv(2).decode('ascii'):
                bashCommand = "scp client@" + ServIp + ":ca.crt ." #obtain ca certificate
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

            print("\nDone")

            s.close()

            conf = open("client.conf","w+") #create and write into client config file
            conf.write(config)
            conf.close()

            bashCommand = "cp ca.crt client.crt client.conf client.key "+ServIp #move files to server directory
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

print("\n\n** now type in the following command: sudo openvpn --config client.conf **")
print("\nIT IS RECCOMMENDED TO RUN ui.py EVERYTIME YOU WANT TO CONNECT TO THE NETWORK!")

