# Generated by Django 3.0.5 on 2020-04-05 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200404_2225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Nickname',
            new_name='nickname',
        ),
    ]
