#A simple script for testing pypair

from pypair import Tornament

to = Tornament()

dummyplayers = {    1:"Derp",
                    2:"Merp",
                    3:"Burp",
                    4:"Yarg",
                    5:"Blarg"}

for p in dummyplayers:
    to.addPlayer( p, dummyplayers[p] )

pairings = to.pairRound()
