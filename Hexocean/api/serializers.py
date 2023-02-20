from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Image
        fields = ['pk', 'user', 'image']

    def image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_url(obj.image.url)