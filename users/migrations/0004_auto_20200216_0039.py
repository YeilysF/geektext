# Generated by Django 3.0.2 on 2020-02-16 05:39

import creditcards.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200216_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_name', models.CharField(max_length=250)),
                ('cc_number', creditcards.models.CardNumberField(max_length=25, verbose_name='card number')),
                ('cc_expire', creditcards.models.CardExpiryField(verbose_name='expiration date')),
                ('cc_code', creditcards.models.SecurityCodeField(max_length=4, verbose_name='security code')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='payment_method',
            field=models.ManyToManyField(to='users.PaymentMethod'),
        ),
    ]
