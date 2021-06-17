from schedule import *
from metrics import *
from print import *

import random


class OptimizeOpponents:
    schedule: Schedule

    def __init__(self, schedule: Schedule):
        self.schedule = schedule

    def optimize(self, maxIterations):

        self.currentScore = self.scoreFunc()

        # debug
        print(f"Initial score: {self.currentScore}")

        goodIterations = 0
        totalIterations = 0
        for i in range(0, maxIterations):
            success = self.randomOpponentChange()
            if success:
                goodIterations += 1
            totalIterations += 1

        # debug
        print(f"Final score: {self.currentScore}")
        print(
            f"Good iterations: {goodIterations} / total iterations: {totalIterations}")

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
        score = self.scoreFunc()
        if score < self.currentScore:
            print(
                f"New score: {score:8.4f}. Swap. Rounds: {roundOne} x {roundTwo}. Players: {playerA} x {playerB}")

            self.currentScore = score
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
        score = self.scoreFunc()
        if score < self.currentScore:
            print(
                f"New score: {score:8.4f}. Substitution in games: {gameOne} x {gameTwo}, players: {playerA} x {playerB}")

            self.currentScore = score
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
