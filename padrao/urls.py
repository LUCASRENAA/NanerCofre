"""controle_estoque URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', views.registro),


                  path('registro/submit', views.submit_registro),

                  path('inicio/',views.inicio),
                  path('upload/', views.subir_arquivo),

                  path('inicio/submit', views.inicio_submit),
                  path('baixar/<id>', views.descer_arquivo_path),
                  path('criptografar_texto/', views.criptografar_texto_submit),
                  path('descriptografar_texto/', views.descriptografar_texto),
                  path('logout/', views.logout_user),

                  path('login/', views.login_user),
    path('login/submit',views.submit_login),

                  path('',RedirectView.as_view(url='inicio/')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
