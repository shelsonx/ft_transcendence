from django.contrib import admin

# Local Folder
from .models import (
    Game,
    GamePlayer,
    GameRules,
    Tournament,
    TournamentPlayer,
    GameRuleType,
)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    readonly_fields = ("owner", "_players")
    list_filter = ["status", "rules__rule_type"]

    list_display = ["__str__", "owner", "game_datetime", "get_rule_type"]

    @admin.display(ordering="rules__rule_type", description="Rule Type")
    def get_rule_type(self, obj):
        return GameRuleType(obj.rules.rule_type).label


@admin.register(GamePlayer)
class GamePlayerAdmin(admin.ModelAdmin):
    model = GamePlayer


@admin.register(GameRules)
class GameRulesAdmin(admin.ModelAdmin):
    model = GameRules


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    model = Tournament


@admin.register(TournamentPlayer)
class TournamentPlayerAdmin(admin.ModelAdmin):
    model = TournamentPlayer
