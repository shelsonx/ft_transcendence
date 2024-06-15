from datetime import timedelta
from random import randrange, shuffle

from django.utils import timezone

from core.models import *
from user.models import User
from utils.generator import Generator


def set_scores(
    a: GamePlayer, b: GamePlayer, max_points: int, is_total_points: bool = False
):
    a.score = randrange(max_points + 1)
    a.save()

    if a.score != max_points and not is_total_points:
        b.score = max_points
    elif is_total_points:
        b.score = is_total_points - a.score
    b.save()


gen = Generator()

usernames = ["sheela", "brunobonaldi", "shelson", "eliaris", "humberto"]
users = User.objects.filter(username__in=usernames)

today = timezone.now()
datebase = today - timedelta(days=7)
if not all([u.games.all().exists() for u in users]):
    control = True
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

names = [
    "libft",
    "Push Swap",
    "Minihell",
    "miniRT",
    "The Transcendence Journey",
]
# if True:
if not all([u.tournaments.all().exists() for u in users]):
    control = True

    for i, user in enumerate(users):
        rules = GameRules.objects.filter(pk=i + 1).first()
        t = gen.seedTournament(
            name=names[i],
            players=users,
            tournament_type=TournamentType.ROUND_ROBIN,
            status=TournamentStatus.SCHEDULED,
            tournament_date=(datebase + timedelta(days=i)),
            rules=rules,
            number_of_players=len(users),
            owner=user,
        )

        rules = t.rules
        duration = timedelta(minutes=(1 + randrange(10)), seconds=randrange(60))
        max_points = (
            rules.points_to_win
            or rules.game_total_points
            or randrange(int(duration.seconds / 15))
        )
        is_total_points = rules.rule_type == GameRuleType.GAME_TOTAL_POINTS
        for r in t.rounds.all():
            r: Round
            for g in r.games.all():
                g: Game
                g.status = GameStatus.ENDED
                g.duration = duration
                g.save()

                player_left, player_right = g.players
                if control:
                    set_scores(player_left, player_right, max_points, is_total_points)
                else:
                    set_scores(player_right, player_left, max_points, is_total_points)
                control = not control
        t.status = TournamentStatus.ENDED
        t.save()
        # t.calculate_scores()

    max_index = len(users) - 1
    status = [TournamentStatus.INVITATION, TournamentStatus.SCHEDULED]
    for i, user in enumerate(users):
        rules = GameRules.objects.filter(pk=i + 1).first()
        opponent_index = i + 1 if i < max_index else 0
        t = gen.seedTournament(
            players=[users[i], users[opponent_index]],
            tournament_type=TournamentType.CHALLENGE,
            status=status[i % 2],
            tournament_date=(datebase + timedelta(days=i)),
            rules=rules,
            number_of_players=2,
            number_of_rounds=i + 3,
            owner=user,
        )
