# Generated by Django 5.0.3 on 2024-06-23 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_alter_game_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='tournament_date',
            field=models.DateTimeField(verbose_name='Tournament date'),
        ),
    ]