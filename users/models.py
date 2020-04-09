from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from bookstore.models import Book
from django.db import models
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    Account_Nickname = models.CharField('Account Alias/Nickname', max_length=100, default='', null=True, blank=True)
    First_Name = models.CharField('First Name', max_length=100, default='', null=True, blank=True)
    Middle_Name = models.CharField('Middle Name', max_length=100, default='', null=True, blank=True)
    Last_Name = models.CharField('Last Name', max_length=100, default='', null=True, blank=True)
    address1 = models.CharField('Address 1', max_length=100, default='', null=True, blank=True)
    address2 = models.CharField('Address 2', max_length=100, default='', null=True, blank=True)
    zipcode = models.CharField('ZIP code', max_length=16, default='', null=True, blank=True)
    city = models.CharField('City', max_length=100, default='', null=True, blank=True)
    state = models.CharField('State', max_length=100, default='', null=True, blank=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
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