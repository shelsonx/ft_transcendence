from django.contrib import admin

# Local Folder
from .models import Game, GamePlayer, GameRules, Tournament, TournamentPlayer


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    # readonly_fields = ("created_by", "company")
    # list_filter = ["stepper_type"]

    # list_display = ["__str__", "created_by", "company", "datetime", "stepper_type"]

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
