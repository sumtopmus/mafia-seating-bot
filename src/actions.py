
from all_configurations import Configurations
from mafia_schedule.configuration import Configuration
from mafia_schedule.schedule import Schedule
from mafia_schedule.player import Participants
from mafia_schedule.schedule_factory import ScheduleFactory

import commands


class Actions:
    conf: Configuration = None
    schedule: Schedule = None
    participants: Participants = None
    filename: str = None

    def __init__(self):
        self.conf = None
        self.schedule = None
        self.participants = None
        self.filename = None

    def setConfig(self, params):
        if not params:
            if self.conf:
                print(self.conf)
            else:
                print("### Set config: name of config expected")
            return

        conf_name = params[0]
        self.conf = Configurations[conf_name]
        print(f"Configuration name: {conf_name}")
        print(self.conf)

    def initSchedule(self, params):
        if not self.conf:
            print("### Please, set config first")
            return

        self.schedule = ScheduleFactory.createInitialSchedule(self.conf)

    def loadSchedule(self, params):
        if not params:
            print("### File name expected!")
            return

        filename = params[0]
        path = commands.getFilePath(filename)
        self.schedule = commands.loadSchedule(path)

    def loadParticipants(self, params):
        if not params:
            print("### File name expected!")
            return

        filename_participants = params[0]
        path_participants = commands.getFilePath(filename_participants)
        self.participants = commands.loadParticipants(path_participants)

        if self.schedule:
            self.schedule.setParticipants(self.participants)

    def saveSchedule(self, params):
        if not self.schedule:
            print("### No schedule, nothing to save")
            return

        if not params:
            print("### File name expected!")
            return

        filename = params[0]
        path = commands.getFilePath(filename)
        commands.saveSchedule(self.schedule, path)

    def showSchedule(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showSchedule(self.schedule, self.participants,
                              scheduleByRounds=True, scheduleByPlayers=True, scheduleMwt=False)

    def showScheduleByRounds(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showSchedule(self.schedule, self.participants,
                              scheduleByRounds=True, scheduleByPlayers=False, scheduleMwt=False)

    def showScheduleByPlayers(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showSchedule(self.schedule, self.participants,
                              scheduleByRounds=False, scheduleByPlayers=True, scheduleMwt=False)

    def showScheduleMwt(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showSchedule(self.schedule, self.participants,
                              scheduleByRounds=False, scheduleByPlayers=False, scheduleMwt=True)

    def showOneRound(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        if not params:
            print("### Round index expected")
            return

        round_idx = int(params[0]) - 1
        commands.showRound(self.schedule, self.participants, round_idx)

    def showStats(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showStats(self.schedule, self.participants,
                           showOpponentMatrix=True, showOpponentHistogram=True, showPairs=False,
                           showSeats=True, showTables=True)

    def showStatsOpponents(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showStats(self.schedule, self.participants,
                           showOpponentMatrix=True, showOpponentHistogram=True,
                           showPairs=False,
                           showSeats=False, showTables=False)

    def showStatsPairs(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showStats(self.schedule, self.participants,
                           showOpponentMatrix=False, showOpponentHistogram=False,
                           showPairs=True,
                           showSeats=False, showTables=False)

    def showStatsTables(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showStats(self.schedule, self.participants,
                           showOpponentMatrix=False, showOpponentHistogram=False, showPairs=False,
                           showSeats=False, showTables=True)

    def showStatsSeats(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        commands.showStats(self.schedule, self.participants,
                           showOpponentMatrix=False, showOpponentHistogram=False, showPairs=False,
                           showSeats=True, showTables=False)

    def checkSchedule(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        if self.schedule.isValid():
            print("Schedule is valid")
        else:
            print("### Schedule is NOT valid")

    def copyRound(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        # zero-based round
        source_idx = int(params[0]) - 1
        dest_idx = int(params[1]) - 1

        print("\nBefore")
        commands.showRound(self.schedule, self.participants, source_idx)
        commands.showRound(self.schedule, self.participants, dest_idx)

        source = self.schedule.rounds[source_idx]
        dest = self.schedule.rounds[dest_idx]

        for i, source_game_id in enumerate(source.gameIds):
            dest_game_id = dest.gameIds[i]
            source_game = self.schedule.games[source_game_id]
            dest_game = self.schedule.games[dest_game_id]

            print(f"Copying game {source_game_id+1} to {dest_game_id+1}")

            for j, id in enumerate(source_game.players):
                dest_game.players[j] = id

        print("\nAfter")
        commands.showRound(self.schedule, self.participants, source_idx)
        commands.showRound(self.schedule, self.participants, dest_idx)

        if self.schedule.isValid():
            print("Schedule is valid")
        else:
            print("### Schedule is NOT valid")

    def switchTables(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        try:
            round_index = int(params[0]) - 1
            table_one = ord(params[1]) - ord('A')
            table_two = ord(params[2]) - ord('A')
        except:
            print("Wrong params")
            return

        round = self.schedule.rounds[round_index]
        game_one_id = round.gameIds[table_one]
        game_two_id = round.gameIds[table_two]
        game_one = self.schedule.games[game_one_id]
        game_two = self.schedule.games[game_two_id]

        print("\n*** Before")
        commands.showSingleRound(self.schedule, self.participants, round_index)

        # switch players in game_one and game_two
        temp = game_one.players.copy()
        game_one.players = game_two.players.copy()
        game_two.players = temp.copy()

        # print("\n*** After")
        commands.showSingleRound(self.schedule, self.participants, round_index)

    def switchPlayers(self, params):
        if not self.schedule:
            print("### No schedule!")
            return

        try:
            round_index = int(params[0]) - 1
            table_one = ord(params[1]) - ord('A')
            player_one = int(params[2]) - 1
            table_two = ord(params[3]) - ord('A')
            player_two = int(params[4]) - 1
        except:
            print("Wrong params")
            return

        # print(f"Round {round_index}. Tables: {table_one} and {table_two}")
        # print(f"Switching players: {player_one} and {player_two}")

        # print("\n*** Before")
        # commands.showRound(self.schedule, self.participants, round_index)

        round = self.schedule.rounds[round_index]
        game_one_id = round.gameIds[table_one]
        game_two_id = round.gameIds[table_two]
        game_one = self.schedule.games[game_one_id]
        game_two = self.schedule.games[game_two_id]

        # check that switch is possible
        one_idx = -1
        for i, player_id in enumerate(game_one.players):
            if player_id == player_one:
                one_idx = i

        two_idx = -1
        for i, player_id in enumerate(game_two.players):
            if player_id == player_two:
                two_idx = i

        if one_idx < 0 or two_idx < 0:
            print("### Something is WRONG")
            return

        # switch players in game_one and game_two
        game_one.players[one_idx] = player_two
        game_two.players[two_idx] = player_one

        # print("\n*** After")
        commands.showRound(self.schedule, self.participants, round_index)

        if self.schedule.isValid():
            print("Schedule is valid")
        else:
            print("### Schedule is NOT valid")
