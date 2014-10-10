#A simple script for testing pypair

from pypair import Tornament
import random
import os

home = os.path.expanduser("~")

to = Tornament()

for p in range(4501):
    to.addPlayer( str(p), "Timmy" )

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

to.saveEventData("%s/datadump1.txt"%home)

print ""
print to.playersDict['1']
print ""

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

to.saveEventData("%s/datadump2.txt"%home)

print ""
print to.playersDict['1']
print ""

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

to.saveEventData("%s/datadump3.txt"%home)

print ""
print to.playersDict['1']
print ""

pairings4 = to.pairRound()

for table in pairings4:
    if not type(pairings4[table]) is str:
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

to.saveEventData("%s/datadump4.txt"%home)

print ""
print to.playersDict['1']
print ""

pairings5 = to.pairRound()

for table in pairings5:
    if not type(pairings5[table]) is str:
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

to.saveEventData("%s/datadump5.txt"%home)

print ""
print to.playersDict['1']
print ""
