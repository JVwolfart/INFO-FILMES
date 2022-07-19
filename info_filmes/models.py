from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_filme = models.CharField(max_length=30, blank=True, null=True)
    capa = models.URLField(max_length=255)
    titulo = models.CharField(max_length=255)
    ano = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.titulo} favorito de {self.usuario}'