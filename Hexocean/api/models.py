from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from .validators import validate_file_extension


class User(AbstractUser):
    tier = models.ForeignKey('Tier', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.username)


class Tier(models.Model):
    name = models.CharField(max_length=100)
    original_link_flag = models.BooleanField(default=False)
    binary_image_link_flag = models.BooleanField(default=False)
    thumbnail_size = ArrayField(models.IntegerField(), help_text="Thumbnail sizes list")

    def __str__(self):
        return self.name


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=settings.IMAGES_URL, validators=[validate_file_extension], max_length=200)

    def __str__(self):
        return str(self.image)


class Thumbnail(models.Model):
    size = models.IntegerField(default=200, validators=[MinValueValidator(100), MaxValueValidator(2000)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=settings.IMAGES_URL, null=True, blank=True, max_length=200)

    def __str__(self):
        return str(self.thumbnail)



