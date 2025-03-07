from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, QuestionnaireViewSet, QuestionViewSet, FormalBookViewSet, login_view

# Initialize router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'formalbooks', FormalBookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Add this to include the router-generated URLs
    path('api/token/', login_view),  # Add the login view URL
]
