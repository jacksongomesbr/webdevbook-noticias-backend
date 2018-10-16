from rest_framework import serializers
from .models import *


class PessoaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pessoa
        fields = ('url', 'id', 'nome', 'email')


class NoticiaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Noticia
        fields = ('url', 'id', 'titulo', 'resumo', 'conteudo', 'autor', 'data', 'data_cadastro', 'publicada', 'destaque', 'foto')

