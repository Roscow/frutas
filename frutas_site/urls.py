
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('frutas.urls')),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name='logout' ),
    
]
