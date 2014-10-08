#A simple script for testing pypair

from pypair import Tornament

to = Tornament()

for p in range(3001):
    to.addPlayer( p, "Timmy" )

pairings = to.pairRound()
