#A simple script for testing pypair

from pypair import Tornament
import random

to = Tornament()

for p in range(16):
    to.addPlayer( p, "Timmy" )

pairings1 = to.pairRound()

for p in pairings1:
    if not type(pairings1[p]) is str:
        per = random.randint(1, 100)
        if per < 47:
            to.reportMatch(p, pairings1[p], p)
        elif per < 98:
            to.reportMatch(p, pairings1[p], pairings1[p])
        else:
            to.reportMatch(p, pairings1[p], "draw")

to.saveEventData("/home/jeff/datadump1.txt")

for p in to.playersDict:
    print "%s has %s points"%(p, to.playersDict[p]["Points"])

pairings2 = to.pairRound()

for p in pairings2:
    if not type(pairings2[p]) is str:
        per = random.randint(1, 100)
        if per < 47:
            to.reportMatch(p, pairings2[p], p)
        elif per < 98:
            to.reportMatch(p, pairings2[p], pairings2[p])
        else:
            to.reportMatch(p, pairings2[p], "draw")

to.saveEventData("/home/jeff/datadump2.txt")

print ""
print ""
print ""
for p in to.playersDict:
    print "%s has %s points"%(p, to.playersDict[p]["Points"])
