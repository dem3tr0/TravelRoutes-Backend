from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RouteViewSet, RouteHistoryViewSet, ReviewViewSet

router = DefaultRouter()
router.register('routes', RouteViewSet)
router.register('routes_history', RouteHistoryViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('routes', include(router.urls)),
    #path('routes/<int:route_id>/likes', ),
    path('routes_history', include(router.urls)),
    path('reviews', include(router.urls)),
]