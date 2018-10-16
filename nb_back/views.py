from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from .models import *

# Create your views here.


class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all().order_by('nome')
    serializer_class = PessoaSerializer
    filter = ('nome', 'email')
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('nome',)
    ordering_fields = '__all__'
    permission_classes = (IsAuthenticatedOrReadOnly,)


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all().order_by('data')
    serializer_class = NoticiaSerializer
    filter_fields = ('titulo', 'resumo', 'conteudo', 'autor', 'destaque', 'publicada')
    ordering_fields = '__all__'
    ordering = ('data', )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
