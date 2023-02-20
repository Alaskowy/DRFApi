import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Image
from .models import Thumbnail


@receiver(post_delete, sender=Image)
def delete_image(sender, instance, *args, **kwargs):
    os.remove(instance.image.path)


@receiver(post_delete, sender=Thumbnail)
def delete_thumbnail(sender, instance, *args, **kwargs):
    os.remove(instance.thumbnail.path)