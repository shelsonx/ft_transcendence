from django import template

register = template.Library()

@register.filter()
def points_per_game(player):
    """Calculate points per game in tournament"""
    total_games = player.winnings + player.losses + player.ties

    return "{:.2f}".format(player.score / total_games if total_games else 0)
