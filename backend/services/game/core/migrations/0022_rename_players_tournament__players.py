# Generated by Django 5.0.3 on 2024-06-14 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_game_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='players',
            new_name='_players',
        ),
    ]
