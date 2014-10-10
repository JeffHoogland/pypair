#A simple script for testing pypair

from pypair import Tornament
import random

to = Tornament()

for p in range(17):
    to.addPlayer( p, "Timmy" )

pairings1 = to.pairRound()

for table in pairings1:
    if not type(pairings1[table]) is str:
        per = random.randint(1, 100)
        if per < 25:
            to.reportMatch(table, [2,0,0])
        elif per < 47:
            to.reportMatch(table, [2,1,0])
        elif per < 60:
            to.reportMatch(table, [0,2,0])
        elif per < 97:
            to.reportMatch(table, [1,2,0])
        elif per < 98:
            to.reportMatch(table, [0,0,1])
        else:
            to.reportMatch(table, [1,1,1])

to.saveEventData("/home/jeff/datadump1.txt")

#for p in to.playersDict:
#    print "%s has %s points"%(p, to.playersDict[p]["Points"])

pairings2 = to.pairRound()

for table in pairings2:
    if not type(pairings2[table]) is str:
        per = random.randint(1, 100)
        if per < 25:
            to.reportMatch(table, [2,0,0])
        elif per < 47:
            to.reportMatch(table, [2,1,0])
        elif per < 60:
            to.reportMatch(table, [0,2,0])
        elif per < 97:
            to.reportMatch(table, [1,2,0])
        elif per < 98:
            to.reportMatch(table, [0,0,1])
        else:
            to.reportMatch(table, [1,1,1])

to.saveEventData("/home/jeff/datadump2.txt")

#print ""
#print ""
#print ""
#for p in to.playersDict:
#    print "%s has %s points"%(p, to.playersDict[p]["Points"])

pairings3 = to.pairRound()

for table in pairings3:
    if not type(pairings3[table]) is str:
        per = random.randint(1, 100)
        if per < 25:
            to.reportMatch(table, [2,0,0])
        elif per < 47:
            to.reportMatch(table, [2,1,0])
        elif per < 60:
            to.reportMatch(table, [0,2,0])
        elif per < 97:
            to.reportMatch(table, [1,2,0])
        elif per < 98:
            to.reportMatch(table, [0,0,1])
        else:
            to.reportMatch(table, [1,1,1])

to.saveEventData("/home/jeff/datadump3.txt")
