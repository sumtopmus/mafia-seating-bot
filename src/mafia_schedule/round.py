import dataclasses


@dataclasses.dataclass(frozen=True, order=False)
class Round:
    '''
    Round is set of games played at the same time.
    Therefore, any player can be only in one of its games.
    '''
    id: int
    gameIds: list[int] = dataclasses.field(
        hash=False, compare=False, default_factory=list)

    @staticmethod
    def fromJson(d: dict):
        gameIds = [id for id in d['gameIds']]
        return Round(d['id'], gameIds)
