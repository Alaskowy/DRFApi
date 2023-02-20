import os
from typing import Any

from PIL import Image as PILImage
from rest_framework.request import Request
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache

from .models import Image, Thumbnail


def create_thumbnail(request: Request) -> dict[Any, str]:
    """Utility function to create thumbnail for supplied image"""
    result = {}
    for thumbnail_size in request.user.tier.thumbnail_size:
        with PILImage.open(request.data['image'].file) as im:
            im.thumbnail((thumbnail_size, thumbnail_size))
            extension = os.path.splitext(request.data['image'].name)[1]
            new_file_name = f'{request.data["image"].name}-thumbnail' \
                       + f'{thumbnail_size}' + extension
            new_file_path = f'{settings.MEDIA_ROOT}{settings.IMAGES_URL}' + new_file_name
            im.save(new_file_path)
            instance = Thumbnail.objects.create(user=request.user, size=thumbnail_size,
                                                thumbnail=new_file_path)
            image_url = f'http://{get_current_site(request)}{settings.MEDIA_URL}{settings.IMAGES_URL}{new_file_name}'
            instance.save()
            result[thumbnail_size] = image_url
    return result


def create_binary_image(request: Request, image: Image, time: int) -> None:
    """Utility function to create binary image"""
    with PILImage.open(image.image) as im:
        extension = os.path.splitext(image.image.url)[1]
        new_file_name = f'{image.image}-binary' + extension
        new_file_path = f'{settings.MEDIA_ROOT}' + new_file_name
        im.save(new_file_path)
        Image.objects.create(user=request.user, image=new_file_path)
        cache.set(f'binary-{image.pk}', f'{settings.MEDIA_ROOT}{new_file_name}', time)
