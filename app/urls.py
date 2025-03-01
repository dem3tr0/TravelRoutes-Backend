# app/urls.py (главный urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

apipaths = [
    path('', include('authentication.urls')),
    path('', include('travel_routes.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apipaths)),
]

# Добавляем маршруты для медиафайлов только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
