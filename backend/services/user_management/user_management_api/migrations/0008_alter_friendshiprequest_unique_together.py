# Generated by Django 3.2.25 on 2024-05-18 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management_api', '0007_auto_20240518_1316'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendshiprequest',
            unique_together=set(),
        ),
    ]
