from schedule import *
from metrics import *
from print import *

import copy
import random


class OptimizeOpponents:
    verbose: bool

    schedule: Schedule

    # slots before optimization
    originalSlots: dict()

    # score in current stage
    score: float

    # best score and slots across all stages
    bestScore: float
    bestSlots: dict()

    def log(self, *kargs, **kwargs):
        if self.verbose:
            print(*kargs, **kwargs)

    def __init__(self, schedule: Schedule, verbose: bool = True):
        self.schedule = schedule
        self.verbose = verbose

    def optimize(self, stages: int, iterations: int):
        self.schedule.generateSlotsFromGames()
        self.originalSlots = copy.deepcopy(self.schedule.slots)

        self.bestScore = self.scoreFunc()
        self.bestSlots = None

        for stage in range(stages):
            print(f"\n*** Stage: {stage+1}")
            self.schedule.slots = copy.deepcopy(self.originalSlots)
            self.score = self.scoreFunc()

            # optimizes self.schedule.slots()
            # updates self.score
            self.optimizeStage(iterations)
            
            # output current schedule
            Print.printPairsHistogram(self.schedule)

            if self.score < self.bestScore:
                self.bestSlots = copy.deepcopy(self.schedule.slots)

        # final
        self.schedule.slots = copy.deepcopy(self.bestSlots)
        self.score = self.bestScore

    def optimizeStage(self, maxIterations: int):
        print(f"Initial score: {self.score:8.4f}")

        goodIterations = 0
        totalIterations = 0
        for i in range(0, maxIterations):
            # debug
            if i != 0 and i % 1000 == 0:
                self.log(f"Iteration: {i:8d}...")

            success = self.randomOpponentChange()
            if success:
                goodIterations += 1
            totalIterations += 1      

        # debug
        print(f"Final score: {self.score:8.4f}")
        print(f"Good iterations: {goodIterations} of {totalIterations}")

    def randomOpponentChange(self) -> bool:
        if self.schedule.configuration.numTables == 1:
            roundOne = random.choice(self.schedule.rounds)
            roundTwo = roundOne
            while roundTwo == roundOne:
                roundTwo = random.choice(self.schedule.rounds)
            return self.randomOpponentChangeInRounds(roundOne.id, roundTwo.id)

        r = random.choice(self.schedule.rounds)
        gameOne = random.choice(r.games)
        gameTwo = gameOne
        while gameTwo == gameOne:
            gameTwo = random.choice(r.games)
        return self.randomOpponentChangeInGames(gameOne.id, gameTwo.id)

    def randomOpponentChangeInRounds(self, roundOne: int, roundTwo: int) -> bool:
        # in this special case every round has one and only one game
        # that's why game index is equal to round index
        gameOneId = self.schedule.games[roundOne].id
        gameTwoId = self.schedule.games[roundTwo].id

        slotOne = self.schedule.slots[gameOneId]
        slotTwo = self.schedule.slots[gameTwoId]

        # figure out what players can be switched
        all = {player.id for player in self.schedule.participants}
        busyOne = slotOne.players
        freeOne = all.difference(busyOne)
        busyTwo = slotTwo.players
        freeTwo = all.difference(busyTwo)

        # chose 2 players to switch between games
        poolA = busyOne.intersection(freeTwo)
        poolB = busyTwo.intersection(freeOne)
        if len(poolA) == 0 or len(poolB) == 0:
            # can not find substitution as one of player pools is empty
            # print("empty pool!")
            return False

        playerA = random.choice(list(poolA))
        playerB = random.choice(list(poolB))

        # switch players from games
        slotOne.players.remove(playerA)
        slotOne.players.add(playerB)
        slotTwo.players.remove(playerB)
        slotTwo.players.add(playerA)

        # continue only if score gets better
        currentScore = self.scoreFunc()
        if currentScore < self.score:
            self.score = currentScore
            self.log(
                f"Score: {self.score:8.4f}. " +
                f"Swap in rounds: {roundOne:2d} x {roundTwo:2d}, players: {playerA:2d} x {playerB:2d}")
            return True
        else:
            slotOne.players.remove(playerB)
            slotOne.players.add(playerA)
            slotTwo.players.remove(playerA)
            slotTwo.players.add(playerB)
            return False

    def randomOpponentChangeInGames(self, gameOne: int, gameTwo: int) -> bool:
        slotOne = self.schedule.slots[gameOne]
        slotTwo = self.schedule.slots[gameTwo]

        busyOne = slotOne.players
        busyTwo = slotTwo.players
        busyBoth = busyOne.intersection(busyTwo)

        one = busyOne.difference(busyBoth)
        two = busyTwo.difference(busyBoth)
        if len(one) == 0 or len(two) == 0:
            # no candidates to swap
            # print("No candidates to swap!")
            return False

        playerA = random.choice(list(one))
        playerB = random.choice(list(two))

        # switch players from games
        slotOne.players.remove(playerA)
        slotOne.players.add(playerB)
        slotTwo.players.remove(playerB)
        slotTwo.players.add(playerA)

        # continue only if score gets better
        currentScore = self.scoreFunc()
        if currentScore < self.score:
            self.score = currentScore
            self.log(f"Score: {self.score:8.4f}. " +
                     f"Swap in games: {gameOne:2d} x {gameTwo:2d}, players: {playerA:2d} x {playerB:2d}")
            return True
        else:
            slotOne.players.remove(playerB)
            slotOne.players.add(playerA)
            slotTwo.players.remove(playerA)
            slotTwo.players.add(playerB)
            return False

    def scoreFunc(self) -> float:
        metrics = Metrics(self.schedule)

        target = 9 * self.schedule.configuration.numAttempts / \
            (self.schedule.configuration.numPlayers-1)

        penalty = 0.0
        for playerId in range(self.schedule.numPlayers):
            opponents = metrics.calcPlayerOpponentsHistogram(playerId)
            sd = metrics.calcSquareDeviationExclude(
                opponents, target, playerId)
            penalty += sd
        return penalty
