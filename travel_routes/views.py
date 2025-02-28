from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError

from .models import Route, Review, Photo
from .serializers import (
    RouteSerializer,
    ReviewSerializer,
    RouteHistorySerializer,
    PhotoSerializer
)


class RouteViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для маршрутов.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Автоматически присваиваем user_id текущего пользователя
        serializer.save(user_id=self.request.user)


class PhotoUploadView(APIView):
    """
    Загрузка изображений для маршрута через отдельный эндпоинт.
    """
    def post(self, request, *args, **kwargs):
        # Извлекаем данные из запроса
        image = request.FILES.get('image')
        route_id = request.POST.get('route_id')

        if not image or not route_id:
            return Response(
                {'error': 'Необходимо указать изображение и ID маршрута'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Создаем запись для изображения
            photo = Photo.objects.create(image=image, route_id=route_id)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PhotoViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для фотографий.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class RouteHistoryViewSet(viewsets.ModelViewSet):
    """
    История изменений маршрутов.
    """
    queryset = Route.objects.all()
    serializer_class = RouteHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']  # Фильтрация по user_id


class ReviewViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для отзывов.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['route_id']  # Сортировка по route_id