from django.db import models
from django_countries.fields import CountryField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.contrib.auth.models import User
from PIL import Image


class PaymentMethod(models.Model):
    payment_name = models.CharField(max_length=250)
    cc_number = CardNumberField(('card number'))
    cc_expire = CardExpiryField(('expiration date'))
    cc_code = SecurityCodeField(('security code'))

    def __str__(self):
        return self.payment_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    country = CountryField(blank_label='Select a Country', blank=True)
    home_address1 = models.CharField("Address Line 1", max_length=1024, null=True, blank=True)
    home_address2 = models.CharField("Address Line 2", max_length=1024, null=True, blank=True)
    city = models.CharField("City", max_length=1024, null=True, blank=True)
    state = models.CharField("State", max_length=1024, null=True, blank=True)
    zip_code = models.CharField("Postal Code", max_length=12, null=True, blank=True)
    payment_method = models.ManyToManyField(PaymentMethod)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            resized_image = (300, 300)
            img.thumbnail(resized_image)
            img.save(self.image.path)
