from rest_framework import serializers
from rest_framework.fields import empty
from .models import *
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('noticias-back')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ('url', 'id', 'nome', 'email')

    def validate_empty_values(self, data):
        if not 'id' in data:
            return super().validate_empty_values(data)
        return True, Pessoa.objects.get(pk=data['id'])


class NoticiaSerializer(serializers.ModelSerializer):
    autor = PessoaSerializer(read_only=False)

    class Meta:
        model = Noticia
        fields = ('url', 'id', 'titulo', 'resumo', 'conteudo', 'autor',
                  'data', 'data_cadastro', 'publicada', 'destaque', 'foto')

    def create(self, validated_data):
        logger.info('NoticiaSerializer.create()')
        autor_data = validated_data.pop('autor')
        instance = Noticia(**validated_data)
        autor = None
        if hasattr(autor_data, 'id'):
            try:
                autor = Pessoa.objects.get(pk=getattr(autor_data, 'id'))
            except:
                raise serializers.ValidationError(
                    {'autor': 'Autor não encontrado'})
        else:
            autor = Pessoa(**autor_data)
            autor.save()
        instance.autor = autor
        instance.save()
        return instance
