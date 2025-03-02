from django.urls import path, include
from .views import list_urls
urlpatterns = [
   path('', list_urls, name='list-urls'),
]
