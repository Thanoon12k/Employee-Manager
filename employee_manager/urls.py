

from django.urls import path,include
from mainapp.urls import urlpatterns as mainapp_urls 
 
urlpatterns = [
    
    path('', include(mainapp_urls)),
    
]
