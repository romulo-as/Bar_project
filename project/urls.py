from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bar/', include('bar.urls')), # Inclui as URLs da sua app 'bar'
]