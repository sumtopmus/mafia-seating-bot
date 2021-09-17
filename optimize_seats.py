import random

from schedule import *
from metrics import *
from print import *


class OptimizeSeats:
    verbose: bool
    schedule: Schedule

    # this callback is for Schedule that is the best at the current moment
    callbackBetterSchedule : None

    shuffleGameFunc = None


    def log(self, *kargs, **kwargs):
        if self.verbose:
            print(*kargs, **kwargs)

    def __init__(self, schedule: Schedule, verbose: bool = True):
        self.schedule = schedule
        self.verbose = verbose

    def optimize(self, numRuns: int, iterations: list()):
        print("\n*** Optimize seats")

        gamePlayers = self.schedule.saveGamePlayers()
        self.currentScore = None
        self.bestScore = None
        self.bestGamePlayers = None

        for i in range(numRuns):
            print(f"\n*** Seating optimization run: {i+1}")
            self.schedule.updateGamePlayers(gamePlayers)

            func = [
                self.swapAllPlayers,
                self.swapTwoPlayers]

            for stage in range(len(iterations)):
                numIterations = iterations[stage]
                print(f"\nStage: {stage+1} (iterations: {numIterations})")
                self.shuffleGameFunc = func[i % len(func)]
                self.optimizeStage(numIterations)
                if self.bestScore != None and 2 * self.bestScore < self.currentScore:
                    print("We have better best score, so... don't continue")
                    break

            if self.bestGamePlayers == None or self.currentScore < self.bestScore:
                print(f"Found best seating, score : {self.currentScore:8.4f}")
                self.bestScore = self.currentScore
                self.bestGamePlayers = self.schedule.saveGamePlayers()
                
                if self.callbackBetterSchedule:
                  self.schedule.updateGamePlayers(self.bestGamePlayers)
                  self.callbackBetterSchedule(self.schedule)
        
        self.schedule.updateGamePlayers(self.bestGamePlayers)

    def optimizeStage(self, iterations: int):
        self.currentScore = self.scoreFunc()

        goodIterations = 0
        for i in range(iterations):
            if i % 1000 == 0:
                print(
                    f"Iteration: {i:8d} of {iterations} (changes: {goodIterations:4d}, score: {self.currentScore:8.4f})")
            success = self.randomSeatChange()
            if success:
                goodIterations += 1

        # debug
        print(f"Final score: {self.currentScore:8.4f}")
        print(f"Good iterations: {goodIterations} of {iterations}")

    def randomSeatChange(self) -> bool:
        game = random.choice(self.schedule.games)

        oldPlayers = game.players.copy()
        self.shuffleGameFunc(game)
        score = self.scoreFunc()

        if score < self.currentScore:
            # debug
            self.log(f"Score: {score:8.4f}. Shuffle game: {game.id}")

            self.currentScore = score
            return True
        else:
            game.players = oldPlayers
            return False

    def swapTwoPlayers(self, game: Game):
        # pick 2 players
        playerOne = random.randrange(len(game.players))
        playerTwo = playerOne
        while playerOne == playerTwo:
            playerTwo = random.randrange(len(game.players))

        # swap two players
        game.players[playerOne], game.players[playerTwo] = game.players[playerTwo], game.players[playerOne]

    def swapAllPlayers(self, game: Game):
        random.shuffle(game.players)

    def scoreFunc(self) -> float:
        m = Metrics(self.schedule)

        target = self.schedule.numAttempts / 10

        # additional heuristics
        calcHalfSimmetry = True
        calcTrippleSimmetry = True
        calcFirstLastSimmetry = True
        factorHalf = 2.0
        factorTripple = 3.0
        factorFirstLast = 20.0

        penalty = 0.0
        for playerId in range(self.schedule.numPlayers):
            seats = m.calcPlayerSeatsHistogram(playerId)
            sd = m.calcSquareDeviation(seats, target)
            penalty += sd
            
            # half simmetry
            '''if calcHalfSimmetry:
                allSeats = sum(seats)
                k_lo = sum(seats[0:5]) / allSeats
                k_hi = sum(seats[5:10]) / allSeats
                penalty_lo = (k_lo - 0.5) ** 2
                penalty_hi = (k_hi - 0.5) ** 2
                penalty += factorHalf * (penalty_lo + penalty_hi)
            '''
            
            # tripple simmetry
            if calcTrippleSimmetry:
                allSeats = sum(seats)
                k_a = sum(seats[0:3]) / allSeats
                k_b = sum(seats[3:7]) / allSeats
                k_c = sum(seats[7:10]) / allSeats
                penalty_a = (10 * k_a - 3) ** 2
                penalty_b = (10 * k_b - 4) ** 2
                penalty_c = (10 * k_c - 3) ** 2
                penalty += factorTripple * (penalty_a + penalty_b + penalty_c)
            
            # first and last simmetry
            if calcFirstLastSimmetry:
                allSeats = sum(seats)
                k_first = seats[0] / allSeats
                k_last = seats[-1] / allSeats
                penalty_first = (10 * k_first - 1) ** 2
                penalty_last = (10 * k_last - 1) ** 2
                penalty += factorFirstLast * (penalty_first + penalty_last)

        return penalty
