# Generated by Django 5.0.3 on 2024-05-02 03:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_gameplayer_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_type', models.SmallIntegerField(choices=[(0, 'Challenge'), (1, 'Round-robin'), (2, 'Elimination'), (3, 'League with Playoff')], default=0, verbose_name='Tournament Type')),
                ('number_of_games', models.PositiveSmallIntegerField(default=0)),
                ('games', models.ManyToManyField(related_name='tournament', to='core.game', verbose_name='Games')),
                ('rules', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='tournament', to='core.gamerules', verbose_name='Games Rules')),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.tournament',),
        ),
        migrations.CreateModel(
            name='Elimination',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.tournament',),
        ),
        migrations.CreateModel(
            name='LeaguePlayoff',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.tournament',),
        ),
        migrations.CreateModel(
            name='RoundRobin',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.tournament',),
        ),
    ]
