from pprint import pprint
from datetime import timedelta
from random import randrange, shuffle

from django.utils import timezone

from user.models import User
from core.models import GameStatus, GamePlayer
from utils.generator import Generator


def set_scores(a: GamePlayer, b: GamePlayer, max_points: int):
    a.score = randrange(max_points + 1)
    a.save()

    if a.score != max_points:
        b.score = max_points
        b.save()


gen = Generator()

usernames = ["sheela", "brunobonaldi", "shelson", "eliaris", "humberto"]
users = User.objects.filter(username__in=usernames)

if not all([u.games.all().exists() for u in users]):
    control = True
    today = timezone.now()
    datebase = today - timedelta(days=7)
    for user in users:
        opponents = [u for u in users if u.id != user.id]
        for opponent in opponents:
            delta = timedelta(
                days=randrange(7), minutes=randrange(60), seconds=randrange(60)
            )
            game = gen.seedGame(
                game_datetime=(datebase + delta),
                status=GameStatus.ENDED,
                duration=timedelta(minutes=randrange(10), seconds=randrange(60)),
                players=[user, opponent],
                owner=user,
            )
            max_points = game.rules.points_to_win
            player_left, player_right = game.players
            if control:
                set_scores(player_left, player_right, max_points)
            else:
                set_scores(player_right, player_left, max_points)
            control = not control

        empty_status = [GameStatus.PENDING, GameStatus.SCHEDULED, GameStatus.CANCELED]
        shuffle(opponents)
        i = 0
        for status in empty_status:
            gen.seedGame(
                game_datetime=(today - timedelta(days=i)),
                status=status,
                duration=timedelta(seconds=0),
                players=[user, opponents[i]],
                owner=user,
            )
            i += 1

        not_fineshed_status = [GameStatus.ONGOING, GameStatus.PAUSED]
        for status in not_fineshed_status:
            game = gen.seedGame(
                game_datetime=(today - timedelta(days=i)),
                status=status,
                duration=timedelta(minutes=randrange(10), seconds=randrange(60)),
                players=[user, opponents[i]],
                owner=user,
            )
            max_points = game.rules.points_to_win
            player_left, player_right = game.players
            player_left.score = randrange(max_points)
            player_left.save()
            player_right.score = randrange(max_points)
            player_right.save()
