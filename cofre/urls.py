"""cofre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from api import views
from frontend import views as views2

router = routers.DefaultRouter()
router.register('BlocoDeNotas', views.BlocoNotasCriptografadaViewSet )
router.register('sites', views.CredencialSitesViewSet )

#router.register('ChaveMestra', views.ChaveMestraViewSet )


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('', RedirectView.as_view(url='/front/cofre')),
    path('bloco', RedirectView.as_view(url='/front/home')),

    path("front/", include("frontend.urls")),
    path("gerenciador/", include("Gerenciador.urls")),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('registro/', views2.registro),
    path('logout/', views2.logout_user),
path('login/', views2.login_user),
    path('login/submit',views2.submit_login),
    path('registro/submit', views2.submit_registro),
]
