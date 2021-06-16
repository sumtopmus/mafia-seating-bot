import random

from schedule import *
from metrics import *
from print import *

class OptimizeSeats:
    schedule : Schedule

    def __init__(self, schedule : Schedule):
        self.schedule = schedule
        pass

    def optimize(self, maxIterations : int):
        self.currentScore = self.scoreFunc()

        # debug
        print(f"Initial score: {self.currentScore}")

        goodIterations = 0
        totalIterations = 0
        for i in range(maxIterations):
            success = self.randomSeatChange()
            if success:
                goodIterations += 1
            totalIterations += 1

        # debug
        print(f"Final score: {self.currentScore}")
        print(f"Optimization finished: {goodIterations} / {totalIterations}")
    
    def randomSeatChange(self):
        game = random.choice(self.schedule.games)
        return self.randomSeatChangeInGame(game)

    def randomSeatChangeInGame(self, game : Game):
        oldPlayers = game.players.copy()

        random.shuffle(game.players)
        
        # TODO: optimization, we can only calculate and compare score func in a SINGLE game!
        # as we change only one game!
        score = self.scoreFunc()
        
        if score < self.currentScore:
            # debug
            print(f"New score: {score:8.4f}. Shuffle game: {game.id}")

            self.currentScore = score
            return True
        else:
            game.players = oldPlayers
            return False

    def scoreFunc(self) -> float :
        m = Metrics(self.schedule)
        
        target = self.schedule.numAttempts / 10
        
        penalty = 0.0
        for playerId in range(self.schedule.numPlayers):
            seats = m.calcPlayerSeatsHistogram(playerId)
            sd = m.calcSquareDeviation(seats, target)
            penalty += sd
        
        return penalty
