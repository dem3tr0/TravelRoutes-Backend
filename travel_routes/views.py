import django_filters.rest_framework
from django.shortcuts import render
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Route, Review, Likes
from .serializers import RouteSerializer, ReviewSerializer, RouteHistorySerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    # Поиск по user_id вида: "GET http://127.0.0.1:8000/routes/?user_id=3"
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id']

    # Сортировка по created_at вида: "GET http://127.0.0.1:8000/routes/?ordering=-created_at"
    ordering_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    #permission_classes = (IsAuthenticatedOrReadOnly, )


class RouteHistoryViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteHistorySerializer

    #Поиск по user_id вида: "GET http://127.0.0.1:8000/routes_history/?user_id=3"
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id']

    #permission_classes = (IsAuthenticatedOrReadOnly, )

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    #Сортировка по created_at вида: "GET http://127.0.0.1:8000/routes/?ordering=-created_at"
    ordering_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    #permission_classes = (IsAuthenticatedOrReadOnly, )

# class LikesViewSet(viewsets.ViewSet):
#     def list(self, request, search_route_id):
#         likes = Likes.objects.filter(route_id=search_route_id)
#     permission_classes = (IsAuthenticatedOrReadOnly, )
