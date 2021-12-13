import random

from .configuration import Configuration
from .schedule_factory import ScheduleFactory
from .schedule import Schedule
from .metrics import Metrics


class OptimizeOpponents:
    verbose: bool

    # current score and schedule
    schedule: Schedule
    score: float

    # best score and schedule
    bestSchedule: Schedule
    bestScore: float

    # TODO: refactor into expectedPairs list, -1 means no constraint
    expectedZeroPairs: int
    expectedSinglePairs: int

    # this callback is for every Schedule generated on iteration if it is not that good
    callbackCurrSchedule = None

    # this callback is for Schedule that is the best at the current moment
    callbackBetterSchedule = None

    def log(self, *kargs, **kwargs):
        if self.verbose:
            print(*kargs, **kwargs)

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        # self.expectedZeroPairs = expectedZeroPairs

    def optimize(self, conf: Configuration, numRuns: int, numIterations: int):
        print("\n*** Optimize opponents")

        self.bestSchedule = None
        self.bestScore = 0
        for i in range(numRuns):
            print(f"\n*** Opponents optimization run: {i+1}")
            self.schedule = ScheduleFactory.createInitialSchedule(conf)
            self.schedule.generateSlotsFromGames()
            self.score = self.scoreFunc()
            self.optimizeStage(numIterations)

            self.schedule.updateGamesFromSlots()

            if not self.bestSchedule or self.score < self.bestScore:
                self.bestSchedule = self.schedule
                self.bestScore = self.score

                # callback for better schedule
                if self.callbackBetterSchedule:
                    self.callbackBetterSchedule(self.bestSchedule)
            else:
                # callback for every schedule
                if self.callbackCurrSchedule:
                    self.callbackCurrSchedule(self.schedule)

            self.schedule = None
            self.score = 0

        return self.bestSchedule

    def optimizeStage(self, numIterations: int):
        goodIterations = 0
        for i in range(0, numIterations):
            # debug
            if i % 1000 == 0:
                print(
                    f"Iteration: {i:8d} of {numIterations} (changes: {goodIterations:4d}, score: {self.score:8.4f})")

            success = self.randomOpponentChange()
            if success:
                goodIterations += 1

        # debug
        print(f"Final score: {self.score:8.4f}")
        print(f"Good iterations: {goodIterations} of {numIterations}")

    def randomOpponentChange(self) -> bool:
        if self.schedule.configuration.numTables == 1:
            roundOne = random.choice(self.schedule.rounds)
            roundTwo = roundOne
            while roundTwo == roundOne:
                roundTwo = random.choice(self.schedule.rounds)
            return self.randomOpponentChangeInRounds(roundOne.id, roundTwo.id)

        # special case - last round is NOT full and only contains 1 table
        # so we back up to
        r = None
        while (r is None) or (len(r.gameIds) == 1):
            r = random.choice(self.schedule.rounds)

        gameOneId = random.choice(r.gameIds)
        gameTwoId = gameOneId
        while gameTwoId == gameOneId:
            gameTwoId = random.choice(r.gameIds)
        return self.randomOpponentChangeInGames(gameOneId, gameTwoId)

    def randomOpponentChangeInRounds(self, roundOneId: int, roundTwoId: int) -> bool:
        # in this special case every round has one and only one game
        # that's why game index is equal to round index
        gameOneId = self.schedule.games[roundOneId].id
        gameTwoId = self.schedule.games[roundTwoId].id

        slotOne = self.schedule.slots[gameOneId]
        slotTwo = self.schedule.slots[gameTwoId]

        # figure out what players can be switched
        all = {playerId for playerId in range(self.schedule.numPlayers)}
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
                f"Swap in rounds: {roundOneId:2d} x {roundTwoId:2d}, players: {playerA:2d} x {playerB:2d}")
            return True
        else:
            slotOne.players.remove(playerB)
            slotOne.players.add(playerA)
            slotTwo.players.remove(playerA)
            slotTwo.players.add(playerB)
            return False

    def randomOpponentChangeInGames(self, gameOneId: int, gameTwoId: int) -> bool:
        slotOne = self.schedule.slots[gameOneId]
        slotTwo = self.schedule.slots[gameTwoId]

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
                     f"Swap in games: {gameOneId:2d} x {gameTwoId:2d}, players: {playerA:2d} x {playerB:2d}")
            return True
        else:
            slotOne.players.remove(playerB)
            slotOne.players.add(playerA)
            slotTwo.players.remove(playerA)
            slotTwo.players.add(playerB)
            return False

    '''
    # old score func
    def scoreFunc(self) -> float:
        metrics = Metrics(self.schedule)

        target = 9 * self.schedule.numAttempts / (self.schedule.numPlayers-1)
        penalty = 0.0
        for playerId in range(self.schedule.numPlayers):
            opponents = metrics.calcPlayerOpponents(playerId)
            sd = metrics.calcSquareDeviationExclude(
                opponents, target, playerId)
            penalty += sd
        return penalty
    '''

    # new score function
    def scoreFunc(self) -> float:
        metrics = Metrics(self.schedule)

        basePenalty = 0.0
        for playerId in range(self.schedule.numPlayers):
            basePenalty += metrics.penaltyPlayer(playerId)

        zeroPlayers = 0
        singlePlayers = 0
        for playerId in range(self.schedule.numPlayers):
            pairs = metrics.calcPlayerPairsHistogram(playerId)
            if pairs[0] == 1:
                zeroPlayers += 1
            if pairs[1] == 1:
                singlePlayers += 1

        # big number to affect basePenalty
        penaltyCoefficient = 100

        zeroPenalty = 0
        if self.expectedZeroPairs > 0:
            expectedZeroPlayers = 2 * self.expectedZeroPairs
            zeroPenalty = penaltyCoefficient * \
                (zeroPlayers - expectedZeroPlayers) ** 2

        singlePenalty = 0
        if self.expectedSinglePairs > 0:
            expectedSinglePlayers = 2 * self.expectedSinglePairs
            singlePenalty = penaltyCoefficient * \
                (singlePlayers - expectedSinglePlayers) ** 2

        return basePenalty + zeroPenalty + singlePenalty
