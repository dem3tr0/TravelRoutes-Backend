from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Route, Review, Photo
from .moderation import Moderation
from .serializers import (
    RouteSerializer,
    ReviewSerializer,
    RouteHistorySerializer,
    PhotoSerializer )


moderation = Moderation()

def route_moderation(charfield1, charfield2):
    if charfield1 is None or charfield2 is None:
        raise ValidationError("Поля 'description' и 'title' обязательны.")

    if not moderation.moderate(charfield1):
        return Response({
            "detail": "Описание не прошло проверку."
        }, status.HTTP_400_BAD_REQUEST)

    elif not moderation.moderate(charfield2):
        return Response({
            "detail": "Заголовок не прошел проверку."
        }, status.HTTP_400_BAD_REQUEST)

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    # Поиск по user_id вида: "GET http://127.0.0.1:8000/routes/?user_id=3"
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id']

    # Сортировка по created_at вида: "GET http://127.0.0.1:8000/routes/?ordering=-created_at"
    ordering_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        description = request.data['description']
        title = request.data['title']

        route_moderation(description, title) #Модерация

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Возврат успешного ответа с данными созданного объекта
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        description = request.data['description']
        title = request.data['title']

        route_moderation(description, title)  # Модерация

        route = self.get_object()
        response = super().update(request, *args, **kwargs)

        return response

    def partial_update(self, request, *args, **kwargs):
        description = request.data['description']
        title = request.data['title']

        route_moderation(description, title)  # Модерация

        route = self.get_object()
        response = super().update(request, *args, **kwargs)

        return response

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id']


class RouteHistoryViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteHistorySerializer

    #Поиск по user_id вида: "GET http://127.0.0.1:8000/routes_history/?user_id=3"
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Сортировка по created_at вида: "GET http://127.0.0.1:8000/routes/?ordering=-created_at"
    ordering_backends = [OrderingFilter]
    ordering_fields = ['route_id']

    def create(self, request, *args, **kwargs):
        text = request.data['text']

        if not moderation.moderate(text):
            return Response({
                "detail": "Описание не прошло проверку."
            }, status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Возврат успешного ответа с данными созданного объекта
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
