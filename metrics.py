from game import *
from player import *
from schedule import Schedule

import math

class Metrics:
    def __init__(self, schedule: Schedule):
        self.schedule = schedule
        self.idealHist = None

    def calcPlayerOpponents(self, thisPlayerId: int):
        '''
        Calculates opponents histogram for given <thisPlayerId>
        Returns a list of size <numPlayers>,
        where value of a[i] - total number of games that pair of players <thisPlayerId>, <i> are playing
        '''
        opponents = [0] * self.schedule.numPlayers

        # go through all games
        for slotId, slot in self.schedule.slots.items():
            if thisPlayerId in slot.players:
                for id in slot.players:
                    if thisPlayerId != id:
                        opponents[id] += 1

        return opponents

    def calcOpponentsMatrix(self):
        '''Calculates opponents histogram for all players'''
        matrix = []
        for playerId in range(self.schedule.numPlayers):
            line = self.calcPlayerOpponents(playerId)
            matrix.append(line)
        return matrix

    def calcPlayerPairsHistogram(self, thisPlayerId: int):
        '''
        Calculates pairs histogram for current player.
        Histogram is dictionary <numGames>:<numPairs>
        '''
        pairs = {}
        for val in range(self.schedule.numAttempts + 1):
            pairs[val] = 0

        opponents = self.calcPlayerOpponents(thisPlayerId)
        for id in range(len(opponents)):
            if id != thisPlayerId:
                numGames = opponents[id]
                pairs[numGames] += 1
        return pairs

    def calcPlayerPairs(self, thisPlayerId : int):
        '''
        Calculates pairs for current user.
        This is dictionary <numGames>:[opponents]
        '''
        pairs = {}
        for numGames in range(0, self.schedule.numAttempts + 1):
            pairs[numGames] = []
        
        opponents = self.calcPlayerOpponents(thisPlayerId)
        for id in range(len(opponents)):
            if id != thisPlayerId:
                numGames = opponents[id]
                pairs[numGames].append(id)
        return pairs

    def calcPairsHistogram(self):
        '''
        Calculates pairs histogram for all players.
        Histogram is dictionary <numGames> : <numPairs>
        '''
        allPairs = {}
        for val in range(self.schedule.numAttempts + 1):
            allPairs[val] = 0
        
        for playerId in range(self.schedule.numPlayers):
            pairs = self.calcPlayerPairsHistogram(playerId)

            for numGames, numPairs in pairs.items():
                allPairs[numGames] += numPairs
        return allPairs

    def pairsHistogramSum(self, pairs : dict):
        result = 0
        for numGames, numPairs in pairs.items():
            result += numPairs      
        return result

    def pairsHistogramCenter(self, pairs : dict):
        totalMult = 0
        totalPairs = 0
        for numGames, numPairs in pairs.items():
            totalMult += (numGames + 1) * numPairs * numPairs
            totalPairs += numPairs * numPairs
        
        center = totalMult / totalPairs
        return center

    def pairsHistogramRange(self, pairs : dict):
        beg = None
        for idx in sorted(pairs):
            if beg == None and pairs[idx] > 0:
                beg = idx
        
        end = None
        for idx in reversed(sorted(pairs)):
            if end == None and pairs[idx] > 0:
                end = idx
        return beg, end

    def penaltyIdealHistogram(self):
        hist = {}
        for val in range(self.schedule.numAttempts + 1):
            hist[val] = 0
        
        numPairs = self.schedule.numPlayers - 1
        target = 9 * self.schedule.numAttempts / (self.schedule.numPlayers-1)

        idxLow = math.floor(target)
        idxHi = math.ceil(target)
        hist[idxLow] = numPairs * (idxHi - target) 
        hist[idxHi] = numPairs - hist[idxLow]
        return hist

    def penaltyPlayer(self, playerId : int):
        target = 9 * self.schedule.numAttempts / (self.schedule.numPlayers-1)
        if self.idealHist == None:
            self.idealHist = self.penaltyIdealHistogram()

        hist = self.calcPlayerPairsHistogram(playerId)

        penalty = 0.0
        for idx in hist:
            idxDist = (idx - target) ** 2
            valueDist = abs(self.idealHist[idx] - hist[idx]) # ** 2
            penalty += idxDist * valueDist
        return penalty

    def calcPlayerSeatsHistogram(self, thisPlayerId: int):
        '''
        Calculates seats histogram for given <thisPlayerId>
        Returns a list of size 10,
        where value of a[i] - total number of games where player sits on seat number <i>
        '''
        seats = [0] * 10

        # go through all games
        for game in self.schedule.games:
            for seat_idx in range(0, 10):
                if game.players[seat_idx] == thisPlayerId:
                    seats[seat_idx] += 1
        return seats

    def calcSeatsMatrix(self):
        '''Calculates seats histogram for all players'''
        matrix = []
        for playerId in range(self.schedule.numPlayers):
            line = self.calcPlayerSeatsHistogram(playerId)
            matrix.append(line)
        return matrix

    def calcSquareDeviationExclude(self, data: list, target: float, exclude_idx: int):
        '''
        Calculates standard deviation between values in <data> and <target>, 
        except for item data[exclude_idx].
        '''
        sd = -(data[exclude_idx] - target) * (data[exclude_idx] - target)
        for i in range(len(data)):
            sd += (data[i] - target) * (data[i] - target)
        return sd / (len(data) - 1)

    def calcSquareDeviation(self, data: list, target: float):
        '''
        Calculates standard deviation between values in <data> and <target> value.
        '''
        sd = 0.0
        for i in range(len(data)):
            sd += (data[i] - target) * (data[i] - target)
        return sd / len(data)
