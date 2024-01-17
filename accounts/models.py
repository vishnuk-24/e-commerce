from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from core.models import BaseModel
from products.models import Product

from .utils import get_pic_path

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Not specified', 'Not Specified'),
)

class UserAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    house_no = models.CharField(max_length=32, blank=True, default="")
    street_name = models.CharField(max_length=32, blank=True, default="")
    address = models.TextField(blank=True, default="")
    city = models.CharField(max_length=150, blank=True, default="")
    state = models.CharField(max_length=64, blank=True, default="")
    country = models.CharField(max_length=32, blank=True, default="")
    zip_code = models.CharField(max_length=16, blank=True, default="")
    enabled = models.BooleanField(default=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, default='Not specified')
    birth_day = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, default="")
    profile_pic = models.ImageField(upload_to=get_pic_path, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_profile_picture_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return "{}defaults/profile-picture.jpg".format(settings.MEDIA_URL)
