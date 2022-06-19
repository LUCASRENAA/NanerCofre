from django.urls import path

from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('criado/<ano>/<mes>/<dia>/<opcao>', views.contasCriadas, name='contasCriadas'),

    path('usuario/<usuario>/<ano>', views.usuarioSenhas, name='usuarioSenhas'),
    path('usuario/', views.usuarioGeral, name='usuarioSenhas'),

    path('admin/', admin.site.urls),

]