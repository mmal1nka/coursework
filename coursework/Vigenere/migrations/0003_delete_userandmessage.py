# Generated by Django 4.0.1 on 2022-01-24 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vigenere', '0002_remove_userandmessage_login_userandmessage_mess_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAndMessage',
        ),
    ]