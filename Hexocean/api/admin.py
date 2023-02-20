from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Tier, Image, Thumbnail


class UserProfileAdmin(UserAdmin):
    fields = [
        'username',
        'password',
        'tier',
    ]
    fieldsets = []


class TierAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'original_link_flag',
        'binary_image_link_flag',
        'thumbnail_size',
    ]


class ImageAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'image',
    ]


class ThumbnailAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'thumbnail',
        'size',
    ]


admin.site.register(User, UserProfileAdmin)
admin.site.register(Tier, TierAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
