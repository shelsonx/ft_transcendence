from pprint import pprint
from datetime import timedelta

from django.utils import timezone

from user.models import User
from core.models import *
from utils.generator import Generator

gen = Generator()

# u1 = User()
# u1.save()
# u2 = User()
# u2.save()
# users = User.objects.all()
# for u in users:
#     vars(u)
#     pprint(u.__dict__)
#     print()

# m = Game()
# m.player_a = u1
# m.player_b = u2
# m.datetime = timezone.now()
# m.save()
# games = Game.objects.all()
# pprint(games)

# r = GameRules(
#     player_reach_points=11,
#     game_total_points=None,
#     max_duration=None,
# )
# r.save()
# r = GameRules(
#     player_reach_points=None,
#     game_total_points=11,
#     max_duration=None,
# )
# r.save()
# r = GameRules(
#     player_reach_points=None,
#     game_total_points=None,
#     max_duration=timedelta(minutes=5),
# )
# r.save()

# rules = GameRules.objects.all()
# for r in rules:
#     pprint(vars(r))

# print("Can't create a duplicated rule")
# rule = GameRules(
#     max_duration=None
# )
# rule.full_clean()
# rule.save()

# rules = GameRules.objects.all()
# for r in rules:
#     pprint(vars(r))

# rule.delete()

# rule1 = GameRules(
#     rule_type=GameRuleType.MIXED_RULES,
#     points_to_win=11,
#     game_total_points=21,
#     max_duration=timedelta(minutes=5),
# )
# # rule1.full_clean()
# rule1.save()

# rule2 = GameRules(
#     rule_type=GameRuleType.MIXED_RULES,
#     points_to_win=11,
#     game_total_points=21,
#     max_duration=timedelta(minutes=5),
# )
# # rule2.full_clean()
# rule2.save()

# pprint(vars(rule1))
# pprint(vars(rule2))

# rule1.delete()
# rule2.delete()

# rules_base = GameRules()
# rules_base.save()

# rules2 = GameRules(
#     player_reach_points=None,
#     game_total_points=11,
#     max_duration=timedelta(minutes=5)
# )
# rules2.save()

# rules3 = GameRules(
#     player_reach_points=5,
# )
# rules3.save()

# Generator test

print()
print(" User model test ".center(80, "-"))
user1 = gen.seedUser()
user2 = gen.seedUser()
users = User.objects.all()
print(users)

print()
print(" GameRules model test ".center(80, "-"))
rules = GameRules.objects.all()
print(len(rules))
rule_default = gen.seedGameRules()
rules = GameRules.objects.all()
print(len(rules), rule_default)

rule5 = gen.seedGameRules(
    rule_type=GameRuleType.PLAYER_POINTS,
    points_to_win=10,
)
rule6 = gen.seedGameRules(
    points_to_win=21,
)
rule7 = gen.seedGameRules(
    rule_type=GameRuleType.GAME_TOTAL_POINTS,
    game_total_points=42,
)
rule8 = gen.seedGameRules(
    rule_type=GameRuleType.GAME_DURATION,
    max_duration=timedelta(minutes=42),
)
rules = GameRules.objects.all()
print(len(rules))

print()
print(" Game model test ".center(80, "-"))
games = Game.objects.all()
print(len(games))
game1 = gen.seedGame()
pprint(vars(game1))

game2 = gen.seedGame(status=GameStatus.WAITING, rules=rule5, players=[user1, user2])

pprint(vars(game2))
print()
print(" Tournament model test ".center(80, "-"))
tournaments = Tournament.objects.all()
print(len(tournaments))
tournament1 = gen.seedTournament()
pprint(vars(tournament1))
for r in tournament1.rounds.all():
    pprint(vars(r))
    for g in r.games.all():
        pprint(vars(g))

print()
print("Round Robin Tournament:")
tournament2 = gen.seedTournament(
    tournament_type=TournamentType.ROUND_ROBIN,
    status=TournamentStatus.SCHEDULED,
    rules=rule5,
    # players=[user1, user2, gen.seedUser(), gen.seedUser(), gen.seedUser()],
    players=[*User.objects.all()[:5]],
    number_of_players=5,
)
pprint(vars(tournament2))
# for r in tournament2.rounds.all():
#     pprint(vars(r))
#     for g in r.games.all():
#         pprint(vars(g))

# tournament3 = gen.seedTournament(
#     tournament_type=TournamentType.ELIMINATION,
#     status=TournamentStatus.SCHEDULED,
#     rules=rule5,
#     players=[user1, user2, gen.seedUser(), gen.seedUser()],
#     number_of_players=4,
# )
# pprint(vars(tournament3))

# print()
# print(" Deleting all objects - users:")
# user1.delete()
# user2.delete()
# print(users)

# print(" Deleting all objects - games:")
# game1.delete()
# game2.delete()
# games = Game.objects.all()
# print(len(games))

# print(" Deleting all objects - rules:")
# rule5.delete()
# rule6.delete()
# rule7.delete()
# rule8.delete()
# rules = GameRules.objects.all()
# print(len(rules))
