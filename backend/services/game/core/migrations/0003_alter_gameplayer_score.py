# Generated by Django 5.0.3 on 2024-05-02 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_gameplayer_game_players'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameplayer',
            name='score',
            field=models.IntegerField(default=0, verbose_name="Player' score in the game"),
        ),
    ]
