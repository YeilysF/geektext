# Generated by Django 3.0.2 on 2020-02-06 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='date_of_death',
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='release_date',
            field=models.DateField(null=True),
        ),
    ]
