from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import login_view

from .views import *

# Initialize router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'queries', QueryViewSet, basename='query')  # Manage Query APIs
router.register(r'query-responses', QueryResponseViewSet, basename='queryresponse')  # Manage Responses APIs
router.register(r'formalbooks', FormalBookViewSet)
urlpatterns = [
    # path('user/',getuserFormalBooks ),
    path('api/auth/', TokenAuthView.as_view(), name='token-auth'),  # Token authentication endpoint
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Add this to include the router-generated URLs
    path('api/login/', login_view),  # Custom login endpoint
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)