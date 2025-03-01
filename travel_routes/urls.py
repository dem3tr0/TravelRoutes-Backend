from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    RouteViewSet,
    RouteHistoryViewSet,
    ReviewViewSet,
    PhotoViewSet,
    LikeView
)

router = DefaultRouter()
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'history_routes', RouteHistoryViewSet, basename='history_route')
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),  # Подключаем все маршруты, созданные роутером
    path('routes/<int:route_id>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='route-reviews'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)