from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/', views.usuarios_inicio, name='usuarios'),
    path('frutas/', views.frutas_inicio, name='frutas'),
    path('estadisticas/', views.estadisticas_inicio, name='estadisticas'),
] 
