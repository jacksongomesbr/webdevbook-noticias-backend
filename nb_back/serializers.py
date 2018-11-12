from rest_framework import serializers
from rest_framework.fields import empty
from .models import *
from django.contrib.auth.models import User, Group
import logging

logger = logging.getLogger('noticias-back')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    groups_ids = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, write_only=True,
                                                    required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email',
                  'password', 'is_superuser', 'groups', 'groups_ids')

    def create(self, validated_data):
        groups = validated_data.pop('groups_ids', None)
        instance = User(**validated_data)
        instance.save()
        if groups:
            for group in groups:
                instance.groups.add(group)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups_ids', None)
        if groups is not None:
            instance.groups.clear()
            for group in groups:
                instance.groups.add(group)
        instance.save()
        return instance


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('url', 'id', 'nome', 'slug', 'descricao')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'nome', 'slug')


class PessoaSerializer(serializers.ModelSerializer):
    usuario_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), pk_field=serializers.IntegerField(),
                                                    write_only=True, required=False)
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Pessoa
        fields = ('url', 'id', 'nome', 'email', 'usuario', 'usuario_id')

    def create(self, validated_data):
        usuario = validated_data.pop('usuario_id', None)
        instance = Pessoa(**validated_data)
        if usuario:
            instance.usuario = usuario
        instance.save()
        return instance

    def update(self, instance, validated_data):
        usuario = validated_data.pop('usuario_id', None)
        if usuario:
            instance.usuario = usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class NoticiaSerializer(serializers.ModelSerializer):
    autor = PessoaSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Pessoa.objects.all(), pk_field=serializers.IntegerField(),
                                                  write_only=True)
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), write_only=True,
                                                      required=False)
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), write_only=True,
                                                  required=False)

    class Meta:
        model = Noticia
        fields = ('url', 'id', 'titulo', 'resumo', 'conteudo', 'autor', 'autor_id',
                  'data', 'data_cadastro', 'publicada', 'destaque', 'foto', 'categoria', 'categoria_id',
                  'tags', 'tags_ids')
        read_only_fields = ('foto',)

    def create(self, validated_data):
        autor = validated_data.pop('autor_id', None)
        categoria = validated_data.pop('categoria_id', None)
        tags = validated_data.pop('tags_ids', None)
        instance = Noticia(**validated_data)
        instance.autor = autor
        instance.save()
        if categoria:
            instance.categoria = categoria
        if tags:
            for tag in tags:
                instance.tags.add(tag)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        autor = validated_data.pop('autor_id', None)
        categoria = validated_data.pop('categoria_id', None)
        tags = validated_data.pop('tags_ids', None)
        instance.autor = autor
        instance.categoria = categoria
        if tags is not None:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(tag)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class NoticiaFotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = ['foto']
