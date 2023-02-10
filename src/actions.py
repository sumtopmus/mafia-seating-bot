
from config_dir import Configurations
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
        g_conf = Configurations[conf_name]
        print(f"Configuration name: {conf_name}\n{g_conf}")
        print(g_conf)

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

    def validateSchedule(self, params):
        if not self.schedule:
            print("### No schedule, nothing to validate")
            return

        if self.schedule.isValid():
            print("Schedule is valid")
        else:
            print("### Schedule is NOT valid")

    def showSchedule(self, params):
        commands.showSchedule(self.schedule, self.participants)

    def showStats(self, params):
        commands.showStats(self.schedule, self.participants)

    def showSeats(self, params):
        commands.showSeats(self.schedule, self.participants)

    def showMwt(self, params):
        commands.showMwtSchedule(self.schedule, self.participants)
