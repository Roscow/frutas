from django.urls import path
from . import views
from django.conf.urls.static import static 
from django.conf import settings

app_name= 'frutas1'
urlpatterns = [
    path('', views.index, name='index'),
    path('frutas/<int:page>/', views.frutas_inicio, name='frutas'),
    path('estadisticas/', views.estadisticas_inicio, name='estadisticas'),
    path('usuario_detalle/<int:id_usuario>/', views.usuario_detalle, name='usuario_detalle'),
    path('proyecto/', views.proyecto, name='proyecto'),
    path('ranking/', views.ranking, name='ranking'),
    path('faltantes/', views.faltantes, name='faltantes'),
    path('versus/', views.versus, name='versus'),
    path('mostrar_usuarios/<int:page>/', views.mostrar_usuarios, name='mostrar_usuarios'),
    path('agregar_fruta/', views.agregar_fruta, name='agregar_fruta'),    
    path('administracion_frutas/', views.administracion_frutas, name='administracion_frutas'),   
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),   
    path('actualizar_foto/', views.actualizar_foto, name='actualizar_foto'),   
     
] 

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
