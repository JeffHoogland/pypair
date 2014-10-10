'''
A tool for pairing players in a swiss event
'''

#Library for loading player dumps
import cPickle as pickle
import random

dbg = True

class Tornament(object):
    def __init__( self, startingTable=1 ):
        
        '''
        Holds player data that are in the event.

        Each player entry is a dictonary named by DCI#

        DCI : { Name:String,
                Opponents:List, Each entry is a DCI number of someone you played
                Results:List, Each entry is a list of wins-losses-draws for the round
                Points:Int,
                OMW%:Float}
        '''
        
        self.playersDict = {}
        self.currentRound = 1
        self.openTable = 0
        self.startingTable = startingTable
        self.roundPairings = {}
        
    def addPlayer( self, DCINumber, playerName ):
        self.playersDict[DCINumber] = {  "Name": playerName,
                                        "Opponents":[],
                                        "Results":[],
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
            
            3.) Loop through each list of points and assign players opponents based with same points
            
            4.) Check for left over players and assign a pair down
        """
        
        #Clear old round pairings
        self.roundPairings = {}
        self.openTable = self.startingTable
        
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
            
            #Randomize the players in the list so the first player isn't always the first paired
            random.shuffle(pointLists[points])
            
        pointTotals.sort(reverse=True)

        for points in pointTotals:
            printdbg(  points ) 
            #While we have 2 or more players with the same points, pair them
            while len(pointLists[points]) > 1:
                ourPlayer = pointLists[points].pop(0)
                ourOpponent = pointLists[points].pop(0)
                
                self.pairPlayers(ourPlayer, ourOpponent)
                
            #Check if we have an odd man out that we need to pair down
            if len(pointLists[points]) == 1:
                #Check to make sure we aren't at the last player in the event
                printdbg(  "Player %s left in %s. The index is %s and the length of totals is %s"%(pointLists[points][0], points, pointTotals.index(points), len(pointTotals)))
                if pointTotals.index(points) + 1 == len(pointTotals):
                    self.assignBye(pointLists[points].pop(0))
                else:
                    nextPoints = pointTotals[pointTotals.index(points) + 1]
                    
                    ourPlayer = pointLists[points].pop(0)
                    ourOpponent = pointLists[nextPoints].pop(0)
                    
                    self.pairPlayers(ourPlayer, ourOpponent)
                    
        return self.roundPairings
                
    def pairPlayers( self, p1, p2 ):
        printdbg("Pairing players %s and %s"%(p1, p2))
        
        self.playersDict[p1]["Opponents"].append(p2)
        self.playersDict[p2]["Opponents"].append(p1)
            
        self.roundPairings[self.openTable] = [p1, p2]
        
        self.openTable += 1

    def assignBye( self, p1, reason="bye" ):
        printdbg( "%s got the bye"%p1)
        self.roundPairings[p1] = reason
        self.playersDict[p1]["Results"].append([0,0,0])
        
        #Add points for "winning"
        self.playersDict[p1]["Points"] += 3
        
    def reportMatch( self, table, result ):
        #table is an integer of the table number, result is a list
        p1 = self.roundPairings[table][0]
        p2 = self.roundPairings[table][1]
        if result[0] == result[1]:
            self.playersDict[p1]["Points"] += 1
            self.playersDict[p1]["Results"].append(result)
            self.playersDict[p2]["Points"] += 1
            self.playersDict[p2]["Results"].append(result)
            
        else:
            if result[0] > result[1]:
                self.playersDict[p1]["Points"] += 3
                self.playersDict[p1]["Results"].append(result)
            elif result[1] > result[0]:
                self.playersDict[p2]["Points"] += 3
                result[0], result[1] = result[1], result[0]
                self.playersDict[p2]["Results"].append(result)

def printdbg( msg ):
    if dbg == True:
        print msg
