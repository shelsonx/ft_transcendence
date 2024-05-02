from pprint import pprint
from datetime import timedelta

from django.utils import timezone

from user.models import User
from core.models import *

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

print("Can't create a duplicated rule")
# rule = GameRules(
#     max_duration=None
# )
# rule.full_clean()
# rule.save()

# rules = GameRules.objects.all()
# for r in rules:
#     pprint(vars(r))

# rule.delete()

rule1 = GameRules(
    rule_type=GameRuleType.MIXED_RULES,
    points_to_win=11,
    game_total_points=21,
    max_duration=timedelta(minutes=5),
)
# rule1.full_clean()
rule1.save()

rule2 = GameRules(
    rule_type=GameRuleType.MIXED_RULES,
    points_to_win=11,
    game_total_points=21,
    max_duration=timedelta(minutes=5),
)
# rule2.full_clean()
rule2.save()

pprint(vars(rule1))
pprint(vars(rule2))

rule1.delete()
rule2.delete()

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
