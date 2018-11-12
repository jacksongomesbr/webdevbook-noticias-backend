from django.db import models
from django.contrib.auth.models import User, Group


class Categoria(models.Model):
    nome = models.CharField(max_length=64, help_text='O nome da categoria')
    slug = models.SlugField(
        max_length=64, help_text='O slug do nome da categoria')
    descricao = models.TextField(
        'Descrição', help_text='A descrição da categoria', blank=True, null=True)

    def __str__(self):
        return self.nome


class Tag(models.Model):
    nome = models.CharField(max_length=64, help_text='O nome da tag')
    slug = models.SlugField(max_length=64, help_text='O slug do nome da tag')

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    nome = models.CharField(
        max_length=128, help_text='Nome completo da pessoa')
    email = models.EmailField(max_length=128, help_text='E-mail da pessoa')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,
                                blank=True, null=True, help_text='O usuário associado à pessoa')

    def __str__(self):
        return self.nome


class Noticia(models.Model):
    titulo = models.CharField(max_length=256, help_text='O título da notícia')
    slug = models.SlugField(max_length=256, blank=True,
                            null=True, help_text='O slug do título da notícia')
    resumo = models.TextField(help_text='O resumo do conteúdo da notícia')
    conteudo = models.TextField('conteúdo', help_text='O conteúdo da notícia')
    autor = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE, help_text='O autor (pessoa) da notícia')
    data_cadastro = models.DateTimeField(
        auto_now=True, help_text='A data de cadastro da notícia (definida automaticamente)')
    data = models.DateTimeField(
        blank=True, null=True, help_text='A data da publicação da notícia (quando publicada)')
    destaque = models.BooleanField(
        default=False, help_text='Indica se a notícia é destaque')
    publicada = models.BooleanField(
        default=False, help_text='Indica se a notícia está publicada (independentemente da data')
    foto = models.FileField(blank=True, null=True,
                            help_text='A foto da notícia')
    categorias = models.ForeignKey(Categoria, on_delete=models.SET_NULL, related_name='noticias', null=True, blank=True,
                                   help_text='Indica a categoria da notícia')
    tags = models.ManyToManyField(Tag, related_name='+', help_text='Indica a lista de tags da notícia')

    def __str__(self):
        return self.titulo
