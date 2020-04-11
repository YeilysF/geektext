# Generated by Django 3.0.5 on 2020-04-11 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('Account_Nickname', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Account Alias/Nickname')),
                ('First_Name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='First Name')),
                ('Middle_Name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Middle Name')),
                ('Last_Name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Last Name')),
                ('address1', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Address 1')),
                ('address2', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Address 2')),
                ('zipcode', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='ZIP code')),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='State')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('books', models.ManyToManyField(blank=True, to='bookstore.Book')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
