# Generated by Django 3.2.25 on 2024-06-22 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management_api', '0013_auto_20240618_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]