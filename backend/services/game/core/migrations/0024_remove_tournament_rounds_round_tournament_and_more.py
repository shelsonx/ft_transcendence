# Generated by Django 5.0.3 on 2024-06-15 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_tournament_name_alter_tournament_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='rounds',
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tournament'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='number_of_rounds',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='tournamentplayer',
            name='alias_name',
            field=models.CharField(blank=True, max_length=20, verbose_name="Tournament player's name"),
        ),
    ]