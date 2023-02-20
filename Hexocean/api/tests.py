from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from .serializers import ImageSerializer
from django.core.files.uploadedfile import SimpleUploadedFile


def create_test_image(user):
    """Utility function to create a test image"""
    image_data = {
        "title": "Test Image",
        "description": "A test image",
        "user": user
    }
    image_file = SimpleUploadedFile(
        name='test_image.png',
        content=open('path/to/test_image.png', 'rb').read(),
        content_type='image/png'
    )
    serializer = ImageSerializer(data=image_data, files={'image': image_file})
    serializer.is_valid(raise_exception=True)
    return serializer.save()


class ImageViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.image = create_test_image(self.user)

    def test_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse(''))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.image.title)
        self.assertEqual(response.data[0]['description'], self.image.description)
        self.assertEqual(response.data[0]['image'], self.image.image.url)
        self.assertEqual(response.data[0]['user'], self.image.user.id)

