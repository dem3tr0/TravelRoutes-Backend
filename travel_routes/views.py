from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Route, Review, Photo
from .serializers import (
    RouteSerializer,
    ReviewSerializer,
    RouteHistorySerializer,
    PhotoSerializer )


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    # Поиск по user_id вида: "GET http://127.0.0.1:8000/routes/?user_id=3"
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id']

    # Сортировка по created_at вида: "GET http://127.0.0.1:8000/routes/?ordering=-created_at"
    ordering_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    
    
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # Поиск по user_id вида: "GET http://127.0.0.1:8000//?user_id=3"
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
