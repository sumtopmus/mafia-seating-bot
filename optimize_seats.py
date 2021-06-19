import random

from schedule import *
from metrics import *
from print import *


class OptimizeSeats:
    verbose: bool
    schedule: Schedule

    shuffleGameFunc = None

    def log(self, *kargs, **kwargs):
        if self.verbose:
            print(*kargs, **kwargs)

    def __init__(self, schedule: Schedule, verbose: bool = True):
        self.schedule = schedule
        self.verbose = verbose
        pass

    def optimize(self, iterations: list()):
        print("\n*** Optimize seats")

        func = [
            self.swapAllPlayers,
            self.swapTwoPlayers,
        ]

        for i in range(len(iterations)):
            numIterations = iterations[i]
            print(f"\n*** Stage: {i+1} (iterations: {numIterations})")
            self.shuffleGameFunc = func[i % len(func)]
            self.optimizeStage(numIterations)

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

        penalty = 0.0
        for playerId in range(self.schedule.numPlayers):
            seats = m.calcPlayerSeatsHistogram(playerId)
            sd = m.calcSquareDeviation(seats, target)
            penalty += sd
        return penalty
