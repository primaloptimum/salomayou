#!/usr/bin/python3
import os
import sys
import subprocess
import socket
import pexpect

buffer=100000

serverNum = 0
ServIp = ""

serverFile = open("serverslist")
for i, line in enumerate(serverFile): #move through the server list of ip addresses and connect to each one
    ServIp=line[:-1]
    serverNum = i

    if !os.path.exists("/root/client"):
        bashCommand = "mkdir /root/client" #make client directory
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #creating configurations
    config='client\ntls-client\nproto tcp\ncipher server1\ncipher AES-128-CBC\nremote ' + ServIp + ' 119' + str(serverNum) + '\ndev tun\nnobind\nremote-cert-tls server\nca ca.crt\ncert client.crt\nkey client.key\nremote-cert-tls server\npersist-key\npersist-tun\nresolv-retry infinite'

    if os.path.exists("/root/client/"+ServIp): #check if server file exists
        print("ip address file exists")
        bashCommand = "cp /root/client/" + ServIp + "/ca.crt /root/client/" #copy ca certificate to the main client directory
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        bashCommand = "cp /root/client/" + ServIp + "/client.crt /root/client/" #copy client certificate to the main client directory
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        bashCommand = "cp /root/client/" + ServIp + "/client.key /root/client/" #copy client key to the main client directory
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        bashCommand = "cp /root/client/" + ServIp + "/client.conf /root/client/" #copy client config to the main client directory
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    else:
        bashCommand = "mkdir /root/client/"+ServIp #create directory for server
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        bashCommand = "cp -r /root/pki /root/easy-rsa/easyrsa3/" #copy pki file to easyrsa3
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd="/root/easy-rsa/easyrsa3")
        output, error = process.communicate()

        bashCommand = "/root/easy-rsa/easyrsa3/easyrsa gen-req client nopass" #generate a request to send to server
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd="/root/easy-rsa/easyrsa3")
        output, error = process.communicate()

        bashCommand = "mv /root/easy-rsa/easyrsa3/pki/private/client.key /root/client/" #move client key file to server directory
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        bashCommand = "mv /root/easy-rsa/easyrsa3/pki/reqs/client.req /root/client/"+ServIp #move request file to server directory
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ServIp, 5000))

        request = open("client/"+ServIp+"/client.req", "r")
        data = request.read()
        request.close()
        
        s.send("Req".encode('utf-8'))
        if s.recv(1).decode('ascii') == "1":
            s.send(data.encode('utf-8'))
            data = s.recv(3).decode('ascii')
            if data == "crt":

                bashCommand = "scp client@" + ServIp + ":/home/client/client.crt /root/client/" #obtain client certificate
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

                s.send("1".encode('utf-8'))
                if "ca" == s.recv(2).decode('ascii'):
                    bashCommand = "scp client@" + ServIp + ":/home/client/ca.crt /root/client/" #obtain ca certificate
                    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()

                print("\nDone")

                s.close()

                conf = open("/root/client/client.conf","w+") #open client config for to edit upon it
                conf.write(config)
                conf.close()

                bashCommand = "cp /root/client/ca.crt /root/client/"+ServIp #move ca certificate to client directory
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

                bashCommand = "cp /root/client/client.crt /root/client/"+ServIp #move client certificate to client directory
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

                bashCommand = "cp /root/client/client.key /root/client/"+ServIp #move client key to client directory
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

                bashCommand = "cp /root/client/client.conf /root/client/"+ServIp #move client config file to client directory
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

            #bashCommand = "sudo openvpn --config client.conf" #move request file to server directory
            #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            #output, error = process.communicate()
