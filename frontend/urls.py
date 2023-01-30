from django.urls import include, path

from . import views
from django.contrib import admin

urlpatterns = [
    #path('', views.home),
    path('home', views.todos),
    #path('secreta', views.secreta),
    path('cofre', views.cofre),

    #path('gerador', views.teste),
    path('geradorDeSenha', views.geradorDeSenha),

    path('criptografar_texto/', views.criptografar),
    path('descriptografar_texto/<id>', views.descriptografar),


]