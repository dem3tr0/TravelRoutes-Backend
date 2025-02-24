from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RouteViewSet,
    RouteHistoryViewSet,
    ReviewViewSet,
    PhotoViewSet)


"""
Как сделать, чтобы мы обращаясь по одному роуту получали и роут
и превью к нему одновременно (так удобнее фронтам). Пока костыли.
"""
router = DefaultRouter()
router.register('routes', RouteViewSet)
router.register('routes_history', RouteHistoryViewSet)
router.register('reviews', ReviewViewSet)
router.register('route_preview', PhotoViewSet)

urlpatterns = [
    path('routes', include(router.urls)),
    #path('routes/<int:route_id>/likes', ),
    path('routes_history', include(router.urls)),
    path('reviews', include(router.urls)),
    path('photos', include(router.urls)),
]