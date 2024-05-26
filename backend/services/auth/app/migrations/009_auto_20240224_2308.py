# Generated by Django 5.0.1 on 2024-02-24 23:08

from django.db import migrations
from ..constants.login_type_constants import LoginTypeConstants
from uuid import uuid4
from django.contrib.auth.hashers import make_password


login_types = [
    {"id": uuid4() ,"name": LoginTypeConstants.AUTH_EMAIL},
    {"id": uuid4() ,"name": LoginTypeConstants.AUTH_42},
]

def get_login_type_id(name):
    for login_type in login_types:
        if login_type['name'] == name:
            return login_type['id']
    return None

login_type_email = get_login_type_id(LoginTypeConstants.AUTH_EMAIL)
users = [
    {
        "id": "9a72c344-62c3-49c3-9bca-188f6f7b3cbe",
        "email":"sheela.khusal.08@gmail.com",
        "user_name":"sheela",
        "login_type_id":login_type_email,
        "enable_2fa":False,
        "password":make_password("Sheela123"),
        "is_active":True
    },
    {
        "id": "355aaf65-0300-47b6-8748-c8d0c1aed702",
        "email":"brunobonaldi1994@gmail.com",
        "user_name":"brunobonaldi",
        "login_type_id":login_type_email,
        "enable_2fa":False,
        "password":make_password("Bruno123"),
        "is_active":True
    },
    {
        "id": "38b8cb4d-34d8-4530-80f3-b4f10cf87b51",
        "email":"shelsonx@gmail.com",
        "user_name":"shelson",
        "login_type_id":login_type_email,
        "enable_2fa":False,
        "password":make_password("Shelson123"),
        "is_active":True
    },
    {
        "id": "9c001ba9-14d5-45ff-a4a4-4f43234dcdd7",
        "email":"eliarisalvares@gmail.com",
        "user_name":"eliaris",
        "login_type_id":login_type_email,
        "enable_2fa":False,
        "password":make_password("Eliaris123"),
        "is_active":True
    },
    {
        "id": "e054f322-7733-48be-b1b1-7a66357efecd",
        "email":"humberto.arndt@gmail.com",
        "user_name":"humberto",
        "login_type_id":login_type_email,
        "enable_2fa":False,
        "password":make_password("Humberto123"),
        "is_active":True
    }
]

def create_login_type(apps, schema_editor):
    LoginType = apps.get_model("app", "LoginType")
    for loginType in login_types:
        LoginType.objects.create(id=loginType["id"], name=loginType["name"])

def delete_login_type(apps, schema_editor):
    LoginType = apps.get_model("app", "LoginType")
    for loginType in login_types:
        LoginType.objects.filter(name=loginType["name"]).delete()

def create_users(apps, schema_editor):
    User = apps.get_model("app", "User")
    for user in users:
        User.objects.create(
            id=user["id"],
            email=user["email"],
            user_name=user["user_name"],
            login_type_id=user["login_type_id"],
            enable_2fa=user["enable_2fa"],
            password=user["password"],
            is_active=user["is_active"]
        )

def delete_users(apps, schema_editor):
    User = apps.get_model("app", "User")
    for user in users:
        User.objects.filter(email=user["email"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_forgotpassworddto_twofactordto_and_more"),
    ]

    operations = [
        migrations.RunPython(create_login_type, reverse_code=delete_login_type),
        migrations.RunPython(create_users, reverse_code=delete_users),
    ]
