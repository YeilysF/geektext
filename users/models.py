from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse
from oscar.models.fields import UppercaseCharField
from bookstore.models import Book
from django.db import models
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    account_nickname = models.CharField('Account Alias/Nickname', max_length=100, default='', null=True, blank=True)
    first_name = models.CharField('First Name', max_length=100, default='', null=True, blank=True)
    middle_name = models.CharField('Middle Name', max_length=100, default='', null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=100, default='', null=True, blank=True)
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            resized_image = (300, 300)
            img.thumbnail(resized_image)
            img.save(self.image.path)


class Address(models.Model):
    address_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address_alias = models.CharField("Distinct Address Name", max_length=100)
    line1 = models.CharField("First line of address", max_length=255, blank=True)
    line2 = models.CharField("Second line of address", max_length=255, blank=True)
    city = models.CharField("City", max_length=255, blank=True)
    state = models.CharField("State/County", max_length=255, blank=True)
    postcode = UppercaseCharField("Post/Zip-code", max_length=64, blank=True)
    country = CountryField(blank_label='Select Country')

    def __str__(self):
        return self.address_alias

    def get_absolute_url(self):
        return reverse('shipping-address', args=[str(self.id)])

    class Meta:
        ordering = ['id']
