# Generated by Django 5.0.1 on 2024-06-27 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_userinfo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
