# Generated by Django 5.0.1 on 2024-05-12 16:05

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_msc', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('full_name', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=10)),
                ('scores', models.IntegerField(default=0)),
                ('winnings', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('position', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('playing', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, default='static/images/astronaut3.jpeg', null=True, upload_to='static/images/%Y/%m/%d/')),
            ],
        ),
    ]
