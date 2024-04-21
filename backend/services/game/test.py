from pprint import pprint

from django.utils import timezone

from user.models import User
from core.models import Match

# u1 = User()
# u1.save()
# u2 = User()
# u2.save()
users = User.objects.all()
for u in users:
    vars(u)
    pprint(u.__dict__)
    print()

# m = Match()
# m.player_a = u1
# m.player_b = u2
# m.datetime = timezone.now()
# m.save()
matchs = Match.objects.all()
pprint(matchs)
