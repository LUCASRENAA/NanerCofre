from django.urls import path

from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('criado/<ano>/<mes>/<dia>/<opcao>', views.contasCriadas, name='contasCriadas'),

    path('usuario/<usuario>/<ano>', views.usuarioSenhasCriacao, name='usuarioSenhas'),
    path('usuario/<ano>', views.usuarioGeralCriacao, name='usuarioSenhas'),

    path('usuario_criado/<usuario>/<ano>', views.usuarioSenhas, name='usuarioSenhas'),
    path('usuario_criado/<ano>', views.usuarioGeral, name='usuarioSenhas'),
    path('usuario_sem_senhas/', views.usuariosSemSenhas, name='usuarioSenhas'),

    path('admin/', admin.site.urls),

]