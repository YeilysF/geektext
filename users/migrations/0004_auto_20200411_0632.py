# Generated by Django 2.2.12 on 2020-04-11 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200411_0514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['id']},
        ),
    ]
