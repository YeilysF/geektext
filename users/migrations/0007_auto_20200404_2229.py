# Generated by Django 3.0.5 on 2020-04-05 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200404_2229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='middle_Name',
            new_name='Middle_Name',
        ),
    ]
