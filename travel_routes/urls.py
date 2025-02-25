from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RouteViewSet,
    RouteHistoryViewSet,
    ReviewViewSet,
    PhotoViewSet
)

router = DefaultRouter()
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'history_routes', RouteHistoryViewSet, basename='history_route')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),  # Подключаем все маршруты, созданные роутером
]