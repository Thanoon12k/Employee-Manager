from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from .plots import report_statistics_view

urlpatterns = [
    path('',report_statistics_view, name='reboot'),  # Custom endpoint to reboot the server
    path('admin/', admin.site.urls),
    path('get-user-announcements/', getAnnouncement, name='get_announcements'),  # Custom endpoint to get announcements
   path('api-token-auth/', authenticate_user_and_get_token, name='api_token_auth'),  # Custom endpoint for token authentication
    path('get-user-reports/', get_user_reports, name='get_user_reports'), 
    path('get-users-list/', get_users_list, name='get_users_list'),  # Custom endpoint to get users list
    path('submit-report/', submit_report, name='submit_report'),  # Custom endpoint to submit a report
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  





