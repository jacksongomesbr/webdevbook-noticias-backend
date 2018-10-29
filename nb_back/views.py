from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes((AllowAny, ))
def checklogin_view(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    user = authenticate(username=username, password=password)
    if user:
        resposta = {
            'situacao': 'ok',
            'mensagem': 'Autenticação realizada com sucesso',
        }
        return Response(resposta, status=200)
    else:
        resposta = {
            'situacao': 'erro',
            'mensagem': 'Nome de usuário ou senha incorretos',
        }
        return Response(resposta, status=403)


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

    


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
