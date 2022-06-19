from datetime import timezone

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

class Hash_Senha_Cofre(models.Model):
    hash = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, models.CASCADE)

class Arquivo(models.Model):
    hash = models.ForeignKey(Hash_Senha_Cofre, models.CASCADE)
    local = models.CharField(max_length=50)
    dataAgora = models.CharField(max_length=31)

    def nome(self):
        return str(self.local).replace("salvar_Arquivos/","")



class Bloco_de_Notas_Criptografada(models.Model):

    titulo = models.CharField(max_length=100)
    texto = models.TextField()

class SenhaCriptografada(models.Model):
    titulo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    senha = models.CharField(max_length=1000)
    uri = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)






