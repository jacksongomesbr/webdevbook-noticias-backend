from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
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


class PessoaViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    """
    retrieve:
    Retorna uma pessoa específica, conforme o parâmetro de URL `id`. A seguir, um exemplo de retorno:

    ```json
    {
        "url": "http://localhost:8000/api/pessoas/1/",
        "id": 1,
        "nome": "GloboEsporte.com",
        "email": "contato@globoesporte.globo.com"
    } 
    ```

    list:
    Retorna uma lista das pessoas. A estrutura de retorno é um array de objetos do tipo `Pessoa`. Exemplo de retorno:

    ```json
    [
        {
            "url": "http://localhost:8000/api/pessoas/2/",
            "id": 2,
            "nome": "G1",
            "email": "contato@g1.com.br"
        },
        {
            "url": "http://localhost:8000/api/pessoas/1/",
            "id": 1,
            "nome": "GloboEsporte.com",
            "email": "contato@globoesporte.globo.com"
        }
    ]
    ```

    create:
    Cria uma instância de pessoa. A estrutura de entrada é um objeto do tipo `Pessoa`.

    update:
    Atualiza a pessoa.

    delete:
    Exclui a pessoa.
    """    
    queryset = Pessoa.objects.all().order_by('nome')
    serializer_class = PessoaSerializer
    filter = ('nome', 'email')
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('nome',)
    ordering_fields = '__all__'
    permission_classes = (IsAuthenticatedOrReadOnly,)


class NoticiaViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    """
    retrieve:
    Retorna uma notícia específica, conforme o parâmetro de rota `id`. A seguir, um exemplo de retorno:

    ```json
    {
        "url": "http://localhost:8000/api/noticias/1/",
        "id": 1,
        "titulo": "Os seis atos do jogo de equipe ...",
        "resumo": "Confira o passo a passo da polêmica ordem ao finlandês...",
        "conteudo": "O Grande Prêmio da Rússia ficará marcado na história da Fórmula 1...",
        "autor": {
            "url": "http://localhost:8000/api/pessoas/1/",
            "id": 1,
            "nome": "GloboEsporte.com",
            "email": "contato@globoesporte.globo.com"
        },
        "data": "2018-09-30T08:00:00-03:00",
        "data_cadastro": "2018-10-15T17:45:32.734336-03:00",
        "publicada": true,
        "destaque": false,
        "foto": "http://localhost:8000/media/f1_9fpCscj.jpg"
    }    
    ```

    O atributo `autor` é do tipo `Pessoa` ([veja][pessoas]).

    [pessoas]: #pessoas


    list:
    Retorna uma lista das notícias. A estrutura de retorno é um array de objetos do tipo `Noticia`. Exemplo de retorno:

    ```json
    [
        {
            "url": "http://localhost:8000/api/noticias/1/",
            "id": 1,
            ...
        },
        {
            "url": "http://localhost:8000/api/noticias/2/",
            "id": 2,
            ...
        },        
        ...
    ]
    ```
    
    create:
    Cria uma instância de notícia. A estrutura de entrada é um objeto do tipo `Noticia`.

    Além disso, é importante ressaltar que o atributo `autor` pode ser informado de duas formas:

    * para informar um autor já cadastrado: o objeto deve ter apenas o campo `id`
    * para cadastrar um autor: o objetivo deve ter os campos `nome` e `email`

    **Exemplo dos dados para cadastro de notícia informando autor existente**:

    ```json
    {
        "titulo": "Os seis atos do jogo de equipe ...",
        "resumo": "Confira o passo a passo da polêmica ordem ao finlandês...",
        "conteudo": "O Grande Prêmio da Rússia ficará marcado na história da Fórmula 1...",
        "autor": {
            "id": 1
        },
        "data": "2018-09-30T08:00:00-03:00",
        "data_cadastro": "2018-10-15T17:45:32.734336-03:00",
        "publicada": true,
        "destaque": false
    }    
    ```

    **Exemplo dos dados para cadastro de notícia e de [novo] autor:**

    ```json
    {
        "titulo": "Os seis atos do jogo de equipe ...",
        "resumo": "Confira o passo a passo da polêmica ordem ao finlandês...",
        "conteudo": "O Grande Prêmio da Rússia ficará marcado na história da Fórmula 1...",
        "autor": {
            "nome": "GloboEsporte.com",
            "email": "contato@globoesporte.globo.com"
        },
        "data": "2018-09-30T08:00:00-03:00",
        "data_cadastro": "2018-10-15T17:45:32.734336-03:00",
        "publicada": true,
        "destaque": false
    }        
    ```    


    update:
    Atualiza a notícia.

    partial_update:
    Atualização parcial da notícia.

    delete:
    Exclui a notícia.
    """

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
