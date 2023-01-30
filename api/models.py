from django.db import models


from django.contrib.auth.models import User

# Create your models here.
class ChaveMestra(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    texto = models.TextField()


class BlocoNotasCriptografada(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    titulo = models.TextField()
    texto = models.BinaryField()
    e_cipher = models.BinaryField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



class CredencialSites(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    titulo = models.TextField()
    nome = models.BinaryField()
    e_cipher_nome = models.BinaryField()
    senha = models.BinaryField()
    e_cipher_senha = models.BinaryField()
    uri = models.TextField()
    notas = models.BinaryField()
    e_cipher_notas = models.BinaryField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)