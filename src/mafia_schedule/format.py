from .schedule import Schedule


class Format:
    def pretty_round_id(self, round_id: int) -> str:
        ''' 
        Show round starting with 1, not with 0
        '''
        return f"{(round_id+1):>02d}"

    def pretty_game_id(self, game_id: int) -> str:
        ''' 
        Show game starting with 1, not with 0
        '''
        return f"{(game_id+1):>02d}"

    def pretty_table_id(self, table_id: int) -> str:
        '''
        Show table as A, B, C; not 0,1,2
        '''
        return chr(ord('A') + table_id)

    def pretty_player_id(self, player_id: int) -> str:
        if self.schedule.participants is None:
            if self.schedule.numTeams > 0:
                team_id = player_id % self.schedule.numTeams
                player_in_team = player_id // self.schedule.numTeams
                player_str = chr(ord('x') + player_in_team)
                return f"{(team_id+1):>2d}-{player_str}"
            else:
                return f"{(player_id+1):2d}"

        else:
            name = self.schedule.participants[player_id].name
            return f"{name}"

    def pretty_team_id(self, player_id: int, numTeams: int) -> str:
        team_id = (player_id // numTeams) + 1
        team_shift = (player_id % numTeams) + 1
        return f"{team_id+1}{team_shift}"

    def __init__(self, schedule: Schedule):
        self.schedule = schedule
