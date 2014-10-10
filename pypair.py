'''
A tool for pairing players in a swiss event
'''

#Load our library for building/working with graphs
import networkx as nx
#Library for loading player dumps
import cPickle as pickle
import random

dbg = True
debuglevel = 1

class Tournament(object):
    def __init__( self, startingTable=1 ):
        #Will hold all player data
        self.playersDict = {}
        #Current round for the event
        self.currentRound = 0
        #The next table we are going to assign paired players to
        self.openTable = 0
        #The starting table number
        self.startingTable = startingTable
        #Pairings for the current round
        self.roundPairings = {}
        
        #this defines the max number of players in a network point range before we split it up. Lower the number, faster the calculations
        self.MaxGroup = 50 
        
        #Contains lists of players sorted by how many points they currently have
        self.pointLists = {}
        
        #Contains a list of points in the event from high to low
        self.pointTotals = []
        
    def addPlayer( self, DCINumber, playerName ):
        
        '''
        Holds player data that are in the event.

        Each player entry is a dictonary named by DCI#

        DCI : { Name:String,
                Opponents:List, Each entry is a DCI number of someone you played
                Results:List, Each entry is a list of wins-losses-draws for the round
                Points:Int,
                OMW%:Float,
                Fixed Seating:Bool/Int, if False no fixed seating, if int that is the assigned table number}
        '''
        
        self.playersDict[DCINumber] = {  "Name": playerName,
                                        "Opponents":[],
                                        "Results":[],
                                        "Points":0,
                                        "OMW%": 0.0,
                                        "Fixed Seating":False}

    def loadEventData( self, pathToLoad ):
        self.playersDict = pickle.load( open( pathToLoad, "rb" ) )
        
    def saveEventData( self, pathToSave ):
        pickle.dump( self.playersDict, open( pathToSave, "wb" ))

    def pairRound( self ):
        """
        Process overview:
            1.) Create lists of players with each point value
            
            2.) Create a list of all current points and sort from highest to lowest
            
            3.) Loop through each list of points and assign players opponents based with same points
            
            4.) Check for left over players and assign a pair down
        """
        self.currentRound += 1
        
        #Clear old round pairings
        self.roundPairings = {}
        self.openTable = self.startingTable
        
        #Contains lists of players sorted by how many points they currently have
        self.pointLists = pointLists = {}
        
        #Contains a list of points in the event from high to low
        self.pointTotals = pointTotals = []
        
        #Counts our groupings for each point amount
        self.countPoints = {}
        
        #Add all players to pointLists
        for player in self.playersDict:
            info = self.playersDict[player]
            #If this point amount isn't in the list, add it
            if "%s_1"%info['Points'] not in pointLists:
                pointLists["%s_1"%info['Points']] = []
                self.countPoints[info['Points']] = 1
            
            #Breakers the players into groups of their current points up to the max group allowed.
            #Smaller groups mean faster calculations
            if len(pointLists["%s_%s"%(info['Points'], self.countPoints[info['Points']])]) > self.MaxGroup:
                self.countPoints[info['Points']] += 1
                pointLists["%s_%s"%(info['Points'], self.countPoints[info['Points']])] = []
            
            #Add our player to the correct group
            pointLists["%s_%s"%(info['Points'], self.countPoints[info['Points']])].append(player)
            
        #Add all points in use to pointTotals
        for points in pointLists:
            pointTotals.append(points)
            
            #Randomize the players in the list so the first player isn't always the first paired
            random.shuffle(pointLists[points])
            
        #Sort our point groups based on points
        pointTotals.sort(reverse=True, key=lambda s: int(s.split('_')[0]))
        
        printdbg( "Point toals after sorting high to low are: %s"%pointTotals, 1 )

        #Actually pair the players utilizing graph theory networkx
        for points in pointTotals:
            printdbg(  points ) 
            
            #Create the graph object and add all players to it
            bracketGraph = nx.Graph()
            bracketGraph.add_nodes_from(pointLists[points])
            
            printdbg( pointLists[points], 5 )
            printdbg( bracketGraph.nodes(), 5 )
            
            #Create edges between all players in the graph who haven't already played
            for player in bracketGraph.nodes():
                for opponent in bracketGraph.nodes():
                    if opponent not in self.playersDict[player]["Opponents"] and player != opponent:
                        #Weight 1 is the default, if a person has more points, give higher weight to make sure they get paired this time
                        wgt = 1
                        if self.playersDict[player]["Points"] > points or self.playersDict[opponent]["Points"] > points:
                            wgt = 2
                        #Create edge
                        bracketGraph.add_edge(player, opponent, weight=wgt)
            
            #Generate pairings from the created graph
            pairings = nx.max_weight_matching(bracketGraph)
            
            printdbg( pairings, 3 )
            
            #Actually pair the players based on the matching we found
            for p in pairings:
                if p in pointLists[points]:
                    self.pairPlayers(p, pairings[p])
                    pointLists[points].remove(p)
                    pointLists[points].remove(pairings[p])
                
            #Check if we have an odd man out that we need to pair down
            if len(pointLists[points]) > 0:
                #Check to make sure we aren't at the last player in the event
                printdbg(  "Player %s left in %s. The index is %s and the length of totals is %s"%(pointLists[points][0], points, pointTotals.index(points), len(pointTotals)), 1)
                if pointTotals.index(points) + 1 == len(pointTotals):
                    while len(pointLists[points]) > 0:
                        #If they are the last player give them a bye
                        self.assignBye(pointLists[points].pop(0))
                else:
                    #Add our player to the next point group down
                    nextPoints = pointTotals[pointTotals.index(points) + 1]
                    
                    while len(pointLists[points]) > 0:
                        pointLists[nextPoints].append(pointLists[points].pop(0))
                    
        return self.roundPairings
                
    def pairPlayers( self, p1, p2 ):
        printdbg("Pairing players %s and %s"%(p1, p2), 5)
        
        self.playersDict[p1]["Opponents"].append(p2)
        self.playersDict[p2]["Opponents"].append(p1)
            
        self.roundPairings[self.openTable] = [p1, p2]
        
        self.openTable += 1

    def assignBye( self, p1, reason="bye" ):
        printdbg( "%s got the bye"%p1, 2)
        self.roundPairings[p1] = reason
        self.playersDict[p1]["Results"].append([0,0,0])
        
        #Add points for "winning"
        self.playersDict[p1]["Points"] += 3
        
    def reportMatch( self, table, result ):
        #table is an integer of the table number, result is a list
        p1 = self.roundPairings[table][0]
        p2 = self.roundPairings[table][1]
        if result[0] == result[1]:
            #If values are the same they drew! Give'em each a point
            self.playersDict[p1]["Points"] += 1
            self.playersDict[p1]["Results"].append(result)
            self.playersDict[p2]["Points"] += 1
            self.playersDict[p2]["Results"].append(result)
        else:
            #Figure out who won and assing points
            if result[0] > result[1]:
                self.playersDict[p1]["Points"] += 3
                printdbg("Adding result %s for player %s"%(result, p1), 2)
                self.playersDict[p1]["Results"].append(result)
                otresult = [result[1], result[0], result[2]]
                printdbg("Adding result %s for player %s"%(otresult, p2), 2)
                self.playersDict[p2]["Results"].append(otresult)
            elif result[1] > result[0]:
                self.playersDict[p2]["Points"] += 3
                printdbg("Adding result %s for player %s"%(result, p1), 2)
                self.playersDict[p1]["Results"].append(result)
                otresult = [result[1], result[0], result[2]]
                printdbg("Adding result %s for player %s"%(otresult, p2), 2)
                self.playersDict[p2]["Results"].append(otresult)

def printdbg( msg, level=1 ):
    if dbg == True and level <= debuglevel:
        print msg
