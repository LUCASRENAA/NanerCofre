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
