import os
import subprocess
import random
import dbth
import time

gateway_IP=""
while(1):
    random_server=dbth.dbth()%1
    serverFile=open("gateways")
    for i, line in enumerate(serverFile):
        if i==random_server:
            gateway_IP=line[:-1]
    cmd=["route","-n"]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    output=output.decode("utf-8")
    lis=output.split("\n")
    lis=lis[2].split("   ")
    old_server_gw= lis[3]
    cmd=["route","del","default","gw",old_server_gw]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    cmd=["route","add","default","gw",gateway_IP]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    print (gateway_IP)
    time.sleep(180)

