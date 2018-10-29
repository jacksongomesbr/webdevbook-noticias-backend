from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PessoaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pessoa
        fields = ('url', 'id', 'nome', 'email')


class NoticiaSerializer(serializers.HyperlinkedModelSerializer):
    # autor = PessoaSerializer()
    class Meta:
        model = Noticia
        fields = ('url', 'id', 'titulo', 'resumo', 'conteudo', 'autor',
                  'data', 'data_cadastro', 'publicada', 'destaque', 'foto')

