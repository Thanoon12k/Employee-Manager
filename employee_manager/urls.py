
from django.contrib import admin

from django.urls import path,include
from mainapp.api.urls import urlpatterns as api_urls
from mainapp.urls import urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('', include(urlpatterns)),
]
