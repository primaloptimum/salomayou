#!/usr/bin/python
import socket
import subprocess
import os
import sys
import pexpect
from thread import start_new_thread

HOST = '' # all availabe interfaces
PORT = 5000 # arbitrary port
clientNum = "0"


if os.path.exists("/root/pki"):
    print("print pki exists")

else:
    bashCommand = "/root/setup-script" # setup server
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
    sys.exit(0)

print("[-] Socket Created")

# bind socket
try:
    s.bind((HOST, PORT))
    print("[-] Socket Bound to port " + str(PORT))
except socket.error, msg:
    print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
    sys.exit()

s.listen(10)
print("Listening...")

def client_thread(conn):

    while True:
        data = conn.recv(1024)
        if not data:
            break
        if data == 'Req': # creates a certificate and folder for the client
            conn.send("1".encode('utf-8'))
            data = conn.recv(1024).decode('ascii') # recv request from client

            bashCommand = "mkdir /root/client"+clientNum # create directory for server
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            clientReq = open("/root/client" + clientNum + "/client" + clientNum + ".req","w+") # store req in client folder
            clientReq.write(data)
            clientReq.close()

            bashCommand = "/root/easy-rsa/easyrsa3/easyrsa import-req /root/client" + clientNum + "/client" + clientNum + ".req client" + clientNum  # import client req to /pki/req
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            bashCommand = "/root/easy-rsa/easyrsa3/easyrsa sign-req client client" + clientNum  # sign client certificate
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            child = pexpect.spawn(bashCommand)
    	    # redirect output to stdout
    	    child.logfile_read = sys.stdout
    	    child.expect('details:')
    	    child.sendline('yes')
    	    child.expect('ca.key:')
    	    child.sendline('0102030405')
    	    # Wait for the process to close its output
    	    child.expect("crt")

            bashCommand = "cp /root/pki/issued/client" + clientNum + ".crt /home/client/client.crt" # move crt to client folder
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            conn.send("crt".encode('utf-8'))

            bashCommand = "chown client /home/client/client.crt" # move crt to client folder
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()


            bashCommand = "cp /root/pki/ca.crt /home/client/ca.crt" # move crt to client folder
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            data = conn.recv(1) # acknowledge retrieval CA certificate
            if data == '1':
                conn.send("ca".encode('utf-8')) # confirm to client certificate signing)

            bashCommand = "chown client /home/client/ca.crt" # change the owner of file
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            data = conn.recv(1) # acknowledge retrieval CA certificate
            if data == '1':
                conn.send("ca".encode('utf-8'))


            bashCommand = "rm -r /root/client" + clientNum  # delete client folder
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            bashCommand = "rm /root/pki/reqs/client" + clientNum + ".req"  # delete client folder
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            print("client done")
            break

    conn.close()

while True:
    conn, addr = s.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

    start_new_thread(client_thread, (conn,))

s.close()
