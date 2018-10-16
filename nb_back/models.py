from django.db import models

# Create your models here.


class Pessoa(models.Model):
    nome = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)

    def __str__(self):
        return self.nome


class Noticia(models.Model):
    titulo = models.CharField(max_length=256)
    resumo = models.TextField()
    conteudo = models.TextField('conteúdo')
    autor = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_cadastro = models.DateTimeField(auto_now=True)
    data = models.DateTimeField(blank=True, null=True)
    destaque = models.BooleanField(default=False)
    publicada = models.BooleanField(default=False)
    foto = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.titulo
