# Generated by Django 2.2.5 on 2020-03-01 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '__first__'),
        ('users', '0002_auto_20200223_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='books',
            field=models.ManyToManyField(blank=True, to='bookstore.Book'),
        ),
    ]
