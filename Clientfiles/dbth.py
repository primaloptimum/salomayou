import random
import time
import sys
import os
from math import ceil, log

def dbth(numOfServers):

    numOfChoices = ceil(log(numOfServers, 2))

    numOfCompetitors=numOfServers
    if numOfCompetitors%2!=0:
        numOfCompetitors -= 1
    round=1

    competitors = []
    for i in range(numOfCompetitors):
        competitor = ""
        for j in range(numOfChoices):
            choice = random.randint(0,2)
            if choice == 1:
                competitor += "P"
            elif choice == 2:
                competitor += "R"
            else:
                competitor += "S"

        competitors.append(competitor)

    while(round<numOfChoices):
        temp = []
        Winner = ""
        randLeft=0
        randRight=0
        randRange=len(competitors)-1

        while(randRange>=1):
            randLeft = random.randint(0,randRange)
            randRight = random.randint(0,randRange)

            while(randLeft==randRight):
                randLeft = random.randint(0,randRange)
                randRight = random.randint(0,randRange)

            if competitors[randLeft]<competitors[randRight]:
                if competitors[randLeft]=="P" and competitors[randRight]=="S":
                    temp.append(competitors.pop(randRight))
                    if randLeft<randRight:
                        competitors.pop(randLeft-1)
                    else:
                        competitors.pop(randLeft)
                else:
                    temp.append(competitors.pop(randLeft))
                    if randLeft<randRight:
                        competitors.pop(randRight-1)
                    else:
                        competitors.pop(randRight)

            elif competitors[randLeft]>competitors[randRight]:
                if competitors[randLeft]=="S" and competitors[randRight]=="P":
                    temp.append(competitors.pop(randLeft))
                    if randLeft<randRight:
                        competitors.pop(randRight-1)
                    else:
                        competitors.pop(randRight)
                else:
                    temp.append(competitors.pop(randRight))
                    if randLeft<randRight:
                        competitors.pop(randLeft)
                    else:
                        competitors.pop(randLeft-1)

            else:
                if random.randint(0,1) == 1:
                    temp.append(competitors.pop(randLeft))
                    if randLeft > randRight:
                        competitors.pop(randRight)
                    else:
                        competitors.pop(randRight-1)
                else:
                    temp.append(competitors.pop(randRight))
                    if randLeft < randRight:
                        competitors.pop(randLeft)
                    else:
                        competitors.pop(randLeft-1)
            randRange-=2

        competitors=temp
        round+=1

    servBin=b''
    for i in competitors[0]:
        if i == "P":
            servBin+=str(random.randint(0,1)).encode()
        elif i == "R":
            servBin+=b'1'
        else:
            servBin+=b'0'

    server = int(servBin, 2)

    return server%numOfServers
