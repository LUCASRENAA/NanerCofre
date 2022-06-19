from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [

path('registro/', views.registro),


                  path('registro/submit', views.submit_registro),

                  path('upload/', views.subir_arquivo),
                  path('inicio/', views.inicio),

                  path('inicio/submit', views.inicio_submit),
                  path('baixar/<id>', views.descer_arquivo_path),
                  path('criptografar_texto/', views.criptografar_texto_submit),
                  path('descriptografar_texto/', views.descriptografar_texto),
                  path('logout/', views.logout_user),

                  path('login/', views.login_user),
    path('login/submit',views.submit_login),

                  path('',RedirectView.as_view(url='inicio/')),
]