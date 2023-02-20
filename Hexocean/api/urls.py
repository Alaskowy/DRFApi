from rest_framework import routers
from django.urls import path
from .views import ImageViewSet

router = routers.DefaultRouter()
router.register('images', ImageViewSet, basename='image')

urlpatterns = [
    path('images/binary/<int:pk>', ImageViewSet.binary_image_view, name='binary')
] + router.urls


