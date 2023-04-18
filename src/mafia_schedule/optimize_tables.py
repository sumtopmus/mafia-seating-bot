import random

from .schedule import Schedule
from .metrics import Metrics
from .game import Game


class OptimizeTables:
    verbose: bool
    schedule: Schedule

    # this callback is for Schedule that is the best at the current moment
    callbackBetterSchedule: None

    shuffleGameFunc = None

    def log(self, *kargs, **kwargs):
        if self.verbose:
            print(*kargs, **kwargs)

    def __init__(self, schedule: Schedule, verbose: bool = True):
        self.schedule = schedule
        self.verbose = verbose

    def optimize(self, numRuns: int, numIterations: int):
        print("\n*** Optimize tables")

        if self.schedule.numTables == 1:
            print("Only one table, nothing to optimize")
            self.bestSchedule = self.schedule
            return

        gamePlayers = self.schedule.saveGamePlayers()
        self.bestSchedule = None
        self.bestScore = 0
        for i in range(numRuns):
            print(f"\n*** Table optimization run: {i+1}")

            self.schedule.updateGamePlayers(gamePlayers)
            self.optimizeStage(numIterations)

            if not self.bestSchedule or self.score < self.bestScore:
                self.bestScore = self.currentScore
                self.bestGamePlayers = self.schedule.saveGamePlayers()

                if self.callbackBetterSchedule:
                    self.schedule.updateGamePlayers(self.bestGamePlayers)
                    self.callbackBetterSchedule(self.schedule)

        # in the end set schedule to best one
        self.schedule.updateGamePlayers(self.bestGamePlayers)

    def optimizeStage(self, iterations: int):
        self.currentScore = self.scoreFunc()

        goodIterations = 0
        for i in range(iterations):
            if i % 1000 == 0:
                print(
                    f"Iteration: {i:8d} of {iterations} (changes: {goodIterations:4d}, score: {self.currentScore:8.4f})")
            success = self.randomTableChange()
            if success:
                goodIterations += 1

        # debug
        print(f"Final score: {self.currentScore:8.4f}")
        print(f"Good iterations: {goodIterations} of {iterations}")

    def randomTableChange(self) -> bool:
        round = random.choice(self.schedule.rounds)
        table_one = random.randrange(self.schedule.numTables)
        table_two = random.randrange(self.schedule.numTables-1)
        table_two = (table_one + table_two) % self.schedule.numTables

        # swap two tables in a round

        # check score
        '''if score < self.currentScore:
            self.currentScore = score
            return True
        else:
            game.players = oldPlayers
            return False
        '''
        return False

    def scoreFunc(self) -> float:
        m = Metrics(self.schedule)
        target = self.schedule.numAttempts / self.schedule.numTables

        penalty = 0.0
        player_tables = m.calcTablesMatrix()

        player_scores = []
        for player, tables in player_tables.items():
            score = m.calcSquareDeviation(tables, target)
            player_scores.append(score)

        penalty = sum(player_scores)
        return penalty
