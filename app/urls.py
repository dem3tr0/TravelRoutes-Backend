from django.contrib import admin
from django.urls import path, include

apipaths = [
    path('', include('authentication.urls')),
    path('', include('travel_routes.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apipaths)),
]
