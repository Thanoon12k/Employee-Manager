from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from mainapp.views import login_view

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-user-announcements/', getBoooks, name='get_announcements'),  # Custom endpoint to get announcements
   path('api-token-auth/', authenticate_user_and_get_token, name='api_token_auth'),  # Custom endpoint for token authentication
    path('get-user-reports/', get_user_reports, name='get_user_reports'),  # Custom endpoint to get user reports
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  





