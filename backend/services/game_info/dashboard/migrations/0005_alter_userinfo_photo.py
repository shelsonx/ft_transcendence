# Generated by Django 5.0.1 on 2024-06-26 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_userinfo_full_name_alter_userinfo_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, default='media/avatars/astronaut3.jpeg', null=True, upload_to='media/avatars/'),
        ),
    ]
