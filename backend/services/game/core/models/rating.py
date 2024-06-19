# Third Party
from enum import IntEnum


class GameRating(IntEnum):
    TIE = 1
    WIN = 2


class TournamentGameRating(IntEnum):
    TIE = 1
    WIN = 3


class TournamentRatingWeight(IntEnum):
    WINNER = 3
    SECOND = 2
    FINISHED = 1
