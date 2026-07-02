from django.db import models

class Jogador(models.Model):
    nome = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    nacionalidade = models.CharField(max_length=100)
    foto = models.URLField(blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    posicao = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome