# Generated by Django 3.2.25 on 2024-06-17 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management_api', '0010_alter_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendshiprequest',
            name='receiver_uuid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='friendshiprequest',
            name='sender_uuid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]