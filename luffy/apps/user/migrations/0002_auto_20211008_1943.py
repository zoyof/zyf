# Generated by Django 2.2.22 on 2021-10-08 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='moblie',
            new_name='mobile',
        ),
    ]