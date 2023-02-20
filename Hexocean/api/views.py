from typing import Union

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.http import FileResponse

from .models import Image
from .serializers import ImageSerializer
from .image_control import create_thumbnail, create_binary_image

MIN_EXPIRY_TIME = 300
MAX_EXPIRY_TIME = 30000


def has_permission_to_access_binary_images(request) -> bool:
    return request.user.tier.binary_image_link_flag


class ImageViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ImageSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = create_thumbnail(self.request)
        if request.user.tier.original_link_flag:
            response['original'] = serializer.data
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def link(self, request: Request, pk=None) -> Response:
        image = get_object_or_404(Image, id=pk)
        expires = int(request.query_params.get('expires', 300))

        if not has_permission_to_access_binary_images(request):
            return Response({
                'error': 'No access to binary image'
            }, status=status.HTTP_403_FORBIDDEN)

        if expires < MIN_EXPIRY_TIME or expires > MAX_EXPIRY_TIME:
            return Response({
                'error': f'Expiry time must be between {MIN_EXPIRY_TIME} and {MAX_EXPIRY_TIME}'
            }, status=status.HTTP_400_BAD_REQUEST)

        create_binary_image(request, image, expires)

        if cache.get(f'binary-{image.pk}') is not None:
            return Response({
                'expiry_time_in_seconds': expires,
                'binary_image': f'http://{get_current_site(request)}/api/images/binary/{image.pk}',
            })
        else:
            return Response({
                'error': 'Binary image expired'}, status=status.HTTP_404_NOT_FOUND
            )

    @api_view(['GET'])
    @action(methods=['get'], detail=True, url_path='binary')
    def binary_image_view(self, pk: int) -> Union[Response, FileResponse]:
        binary_file_path = cache.get(f'binary-{pk}')
        if binary_file_path is None:
            return Response({
                'error': 'Binary image expired'
             }, status=status.HTTP_410_GONE)
        try:
            return FileResponse(open(binary_file_path, 'rb'))
        except FileNotFoundError:
            return Response({
                'error': 'Binary image not found'
            }, status=status.HTTP_404_NOT_FOUND)

