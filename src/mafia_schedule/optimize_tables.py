import random
import statistics
from tqdm import tqdm

from .progress import ProgressBar
from .schedule import Schedule
from .metrics import Metrics
from .game import Game


class OptimizeTables:
    verbose: bool
    schedule: Schedule

    # this callback is for Schedule that is the best at the current moment
    callbackBetterSchedule = None

    # this callback is for the progress bar
    callbackProgress = None

    # progress bar
    pbar: ProgressBar = None

    shuffleGameFunc = None

    def log(self, *kargs, **kwargs):
        if self.verbose:
            print(*kargs, **kwargs)

    def __init__(self, schedule: Schedule, verbose: bool = True):
        self.schedule = schedule
        self.verbose = verbose

    async def optimize(self, numRuns: int, numIterations: int):
        print("\n*** Optimize tables")

        if self.schedule.numTables == 1:
            print("Only one table, nothing to optimize")
            self.bestSchedule = self.schedule
            return

        gamePlayers = self.schedule.saveGamePlayers()
        self.bestSchedule = None
        self.bestScore = 0
        self.pbar = ProgressBar(numRuns*numIterations, self.callbackProgress)
        for i in range(numRuns):
            print(f"\n*** Table optimization run: {i+1}")

            self.schedule.updateGamePlayers(gamePlayers)
            await self.optimizeStage(numIterations)

            if not self.bestSchedule or self.score < self.bestScore:
                self.bestScore = self.currentScore
                self.bestGamePlayers = self.schedule.saveGamePlayers()

                if self.callbackBetterSchedule:
                    self.schedule.updateGamePlayers(self.bestGamePlayers)
                    self.callbackBetterSchedule(self.schedule)

        # in the end set schedule to best one
        self.schedule.updateGamePlayers(self.bestGamePlayers)

    async def optimizeStage(self, iterations: int):
        self.currentScore = self.scoreFunc()

        goodIterations = 0
        for i in range(iterations):
            if i % 1000 == 0:
                print(
                    f"Iteration: {i:8d} of {iterations} (changes: {goodIterations:4d}, score: {self.currentScore:8.4f})")
            success = self.randomTableChange()
            if success:
                goodIterations += 1
            if i % 100 == 50:
                await self.pbar.update(100)

        # debug
        print(f"Final score: {self.currentScore:8.4f}")
        print(f"Good iterations: {goodIterations} of {iterations}")

    def randomTableChange(self) -> bool:
        round = random.choice(self.schedule.rounds)
        table_one = random.randrange(self.schedule.numTables)
        table_two = 1 + random.randrange(self.schedule.numTables-1)
        table_two = (table_one + table_two) % self.schedule.numTables

        # last round MAY have less than numTables items, so we double check that
        # otherwise it may cause index-out-of-bounds
        if len(round.gameIds) < self.schedule.numTables:
            table_one = table_one % len(round.gameIds)
            table_two = table_two % len(round.gameIds)
            if table_one == table_two:
                return

        game_one_id = round.gameIds[table_one]
        game_two_id = round.gameIds[table_two]
        game_one = self.schedule.games[game_one_id]
        game_two = self.schedule.games[game_two_id]

        # switch games in a round
        temp = game_one.players.copy()
        game_one.players = game_two.players.copy()
        game_two.players = temp.copy()

        # check score
        score = self.scoreFunc()

        if score < self.currentScore:
            # debug
            '''
            print(
                f"\nSwithing tables. Round: {round.id}. Tables: {table_one} <-> {table_two}. Games: {game_one_id} <-> {game_two_id}")
            print(f"Score before: {self.currentScore}")
            print(f"Score after: {score}")

            print(f"Game1: {game_two.players}")
            print(f"Game2: {game_one.players}")
            '''

            self.currentScore = score
            return True
        else:
            # switch games back
            temp = game_one.players.copy()
            game_one.players = game_two.players.copy()
            game_two.players = temp.copy()
            return False

    def scoreFunc(self) -> float:
        m = Metrics(self.schedule)
        penalties = m.calcPlayerTablePenalties()

        score = statistics.mean(penalties) + max(penalties)
        return score
