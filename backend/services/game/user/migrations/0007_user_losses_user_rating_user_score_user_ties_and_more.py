# Generated by Django 5.0.3 on 2024-06-15 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='losses',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='ties',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='winnings',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
