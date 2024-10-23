from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('carrito/', views.carrito, name='carrito'),
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    path('agregar-al-carrito/<int:peluche_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar/<int:item_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('ver-mensajes/', views.ver_mensajes, name='ver_mensajes'),
    path('perfil/', views.perfil_usuario, name='perfil'),
]