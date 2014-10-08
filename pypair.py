'''
A tool for pairing players in a swiss event
'''

#Network library to handle pairing players
# http://networkx.github.io/documentation/networkx-1.9.1/overview.html
import networkx as nx
#Library for loading player dumps
import cPickle as pickle
import random

class Tornament(object):
    def __init__( self ):
        
        '''
        Holds player data that are in the event.

        Each player entry is a dictonary named by DCI#

        DCI : { Name:String,
                Opponents:List,
                Points:Int,
                OMW%:Float}
        '''
        
        self.playersDict = {}
        
        self.roundPairings = {}
        
        #NetworkX object to make pairing easier
        self.playersNetwork = nx.Graph()
        
    def addPlayer( self, DCINumber, playerName ):
        self.playersDict[DCINumber] = {  "Name": playerName,
                                        "Opponents":[],
                                        "Points":0,
                                        "OMW%": 0.0}

    def loadEventData( self, pathToLoad ):
        self.playersDict = pickle.load( open( pathToLoad, "rb" ) )
        
    def saveEventData( self, pathToSave ):
        pickle.dump( self.playersDict, open( pathToSave, "wb" ))

    def pairRound( self ):
        """
        Process overview:
            1.) Create lists of players with each point value
            
            2.) Create a list of all current points and sort from highest to lowest
            
            3.) Assign edge weights based on how close in points the players are
        """
        
        #Clear old round pairings
        self.roundPairings = {}
        
        #Contains lists of players sorted by how many points they currently have
        pointLists = {}
        
        #Contains a list of points in the event from high to low
        pointTotals = []
        
        #Add all players to pointLists
        for player in self.playersDict:
            info = self.playersDict[player]
            if info['Points'] not in pointLists:
                pointLists[info['Points']] = []
            
            pointLists[info['Points']].append(player)
            
        #Add all points in use to pointTotals
        for points in pointLists:
            pointTotals.append(points)
            
        pointTotals.sort()

        for points in pointTotals:
            #While we have 2 or more players with the same points, pair them
            while len(pointLists[points]) > 1:
                ourPlayer = pointLists[points].pop(0)
                ourOpponent = pointLists[points].pop(random.randint(0, len(pointLists[points])-1))
                
                self.pairPlayers(ourPlayer, ourOpponent)
                
            #Check if we have an odd man out that we need to pair down
            if len(pointLists[points]) == 1:
                #Check to make sure we aren't at the last player in the event
                if pointTotals.index(points) < len(pointTotals) -1:
                    nextPoint = pointTotals.index(points) + 1
                else:
                    self.assignBye(pointLists[points].pop(0))
                    
        print self.roundPairings
        return self.roundPairings
                
    def pairPlayers( self, p1, p2 ):
        self.playersDict[p1]["Opponents"].append(p2)
        self.playersDict[p2]["Opponents"].append(p1)
            
        self.roundPairings[p1] = p2

    def assignBye( self, p1, reason="bye" ):
        self.roundPairings[p1] = reason
        
        #Add points for "winning"
        self.playersDict[p1]["Points"] += 3
