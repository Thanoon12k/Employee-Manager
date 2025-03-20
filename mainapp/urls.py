from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import *

# Initialize router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'formalbooks', FormalBookViewSet)

urlpatterns = [
    # path('user/',getuserFormalBooks ),
    path('auth/token/', TokenAuthView.as_view(), name='token-auth'),  # Token authentication endpoint
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Add this to include the router-generated URLs

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)