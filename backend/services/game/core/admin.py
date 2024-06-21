from django.contrib import admin

# Local Folder
from .models import (
    Game,
    GamePlayer,
    GameRules,
    GameRuleType,
    Round,
    Tournament,
    TournamentPlayer,
    TournamentType,
)


class GamePlayerInline(admin.TabularInline):
    model = GamePlayer
    fields = ["user", "score", "position"]
    readonly_fields = ["user"]
    max_num = 2


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    fields = ["game_datetime", "status", "duration", "rules", "owner"]
    readonly_fields = ("owner",)
    inlines = [GamePlayerInline]

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


class TournamentPlayerInline(admin.TabularInline):
    model = TournamentPlayer
    extra = 0
    fields = ["user", "alias_name", "score", "rating", "winnings", "losses", "ties"]
    readonly_fields = ["user"]


class RoundInline(admin.TabularInline):
    model = Round
    extra = 0
    fields = ["round_number", "number_of_games"]
    readonly_fields = ["round_number"]


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    model = Tournament
    readonly_fields = ("owner", "rules", "tournament_type")
    fields = [
        "name",
        "tournament_type",
        "tournament_date",
        "status",
        "rules",
        "number_of_players",
        "number_of_rounds",
        "owner",
    ]
    inlines = [TournamentPlayerInline, RoundInline]

    list_filter = ["status", "tournament_type", "rules__rule_type"]
    list_display = [
        "name",
        "owner",
        "tournament_date",
        "get_tournament_type",
        "get_rule_type",
    ]
    search_fields = ["name", "owner"]

    @admin.display(ordering="rules__rule_type", description="Rule Type")
    def get_rule_type(self, obj):
        return GameRuleType(obj.rules.rule_type).label

    @admin.display(ordering="tournament_type", description="Tournament Type")
    def get_tournament_type(self, obj):
        return TournamentType(obj.tournament_type).label


@admin.register(TournamentPlayer)
class TournamentPlayerAdmin(admin.ModelAdmin):
    model = TournamentPlayer

    list_display = [
        "__str__",
        "tournament",
    ]


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    model = Round
    readonly_fields = ["games", "tournament"]
    list_display = ["__str__", "tournament"]
    search_fields = ["tournament"]
