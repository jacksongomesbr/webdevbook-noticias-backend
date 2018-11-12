from django.shortcuts import render
from rest_framework import response, status, decorators, viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .utils import MultipartJsonParser
from .serializers import *
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes((AllowAny, ))
def checklogin_view(request):
    """
    Realiza a autenticação, verificando se o `username` e `password` informados estão corretos.

    Retorna um objeto conforme o resultado da autenticação.

    Se a autenticação estiver correta, retorna código `200` e um objeto:

    ```json
    {
        "situacao": "ok",
        "mensagem": "Autenticação realizada com sucesso"
    }
    ```

    Se a autenticação estiver incorreta, retorna código `403` e um objeto:

    ```json
    {
        "situacao": "erro",
        "mensagem": "Nome de usuário ou senha incorretos"
    }
    ```
    """
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
    """
    retrieve:
    Retorna uma pessoa específica, conforme o parâmetro de URL `id`. A seguir, um exemplo de retorno:

    ```json
    {
        "url": "http://localhost:8000/api/pessoas/1/",
        "id": 1,
        "nome": "GloboEsporte.com",
        "email": "contato@globoesporte.globo.com",
        "usuario": {
            "url": "http://localhost:8000/api/usuarios/3/",
            "id": 3,
            "username": "jackson",
            "email": "jackson@servidor.com",
            "is_superuser": false,
            "groups": [
                {
                "url": "http://localhost:8000/api/grupos/1/",
                "id": 1,
                "name": "Editores"
                }
            ]
        }
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
            ...
        },
        {
            "url": "http://localhost:8000/api/pessoas/1/",
            "id": 1,
            "nome": "GloboEsporte.com",
            "email": "contato@globoesporte.globo.com"
            ...
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


class NoticiaViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Retorna uma notícia específica, conforme o parâmetro de rota `id`. A seguir, um exemplo de retorno:

    ```json
    {
        "url": "http://localhost:8000/api/noticias/26/",
        "id": 26,
        "titulo": "notícia de teste 1000",
        "resumo": "resumo",
        "conteudo": "conteudo",
        "autor": {
            "url": "http://localhost:8000/api/pessoas/1/",
            "id": 1,
            "nome": "GloboEsporte.com",
            "email": "contato@globoesporte.globo.com",
            "usuario": {
                "url": "http://localhost:8000/api/usuarios/3/",
                "id": 3,
                "username": "jackson",
                "email": "jackson@servidor.com",
                "is_superuser": false,
                "groups": [
                    {
                        "url": "http://localhost:8000/api/grupos/1/",
                        "id": 1,
                        "name": "Editores"
                    }
                ]
            }
        },
        "data": null,
        "data_cadastro": "2018-11-12T16:27:08.104494-03:00",
        "publicada": false,
        "destaque": false,
        "foto": null,
        "tags": [
            {
                "url": "http://localhost:8000/api/tags/1/",
                "id": 1,
                "nome": "Política",
                "slug": "politica"
            }
        ]
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

    Além disso, é importante ressaltar o comportamento dos atributos relacionados: apenas na
    leitura (individual ou lista, usando GET) estão disponíveis os atributos `autor`, `categoria` e `tags`.
    No caso da criação ou atualização (POST ou PUT, respectivamente) estão disponíveis, respectivamente,
    os atributos:

    * `autor_id`: número; informa o identificador do autor
    * `categoria_id`: número; informa o identificador da categoria
    * `tags_ids`: array; informa os identificadores das tags

    **Exemplo dos dados para cadastro de notícia**:

    ```json
    {
        "titulo": "Os seis atos do jogo de equipe ...",
        "resumo": "Confira o passo a passo da polêmica ordem ao finlandês...",
        "conteudo": "O Grande Prêmio da Rússia ficará marcado na história da Fórmula 1...",
        "autor_id": 1,
        "data": "2018-09-30T08:00:00-03:00",
        "data_cadastro": "2018-10-15T17:45:32.734336-03:00",
        "publicada": true,
        "destaque": false,
        "categoria_id": 1,
        "tags_ids": [1, 3, 5]
    }    
    ```

    update:
    Atualiza a notícia.

    partial_update:
    Atualiza a notícia.

    delete:
    Exclui a notícia.
    """

    queryset = Noticia.objects.all().order_by('data')
    serializer_class = NoticiaSerializer
    filter_fields = ('titulo', 'resumo', 'conteudo',
                     'autor', 'destaque', 'publicada', 'categorias', 'tags')
    ordering_fields = '__all__'
    ordering = ('data', )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)

    @decorators.action(
        detail=True,
        methods=['PUT'],
        serializer_class=NoticiaFotoSerializer,
        parser_classes=[MultiPartParser],
    )
    def foto(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(
            obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering_fields = '__all__'
    filter_fields = ('username', 'email', 'groups',)
    permission_classes = (IsAdminUser, )
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser, )
    ordering_fields = '__all__'
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Retorna uma categoria específica, conforme o parâmetro de URL `id`. A seguir, um exemplo de retorno:

    ```json
    {
        "url": "http://localhost:8000/api/categorias/1/",
        "id": 1,
        "nome": "Política",
        "slug": "politica",
        "descricao": ""
    }
    ```

    list:
    Retorna uma lista das categorias. A estrutura de retorno é um array de objetos do tipo `Categoria`.

    Exemplo de retorno:

    ```json
    [
        {
            "url": "http://localhost:8000/api/categorias/1/",
            "id": 1,
            "nome": "Política",
            "slug": "politica",
            "descricao": ""
        },
        {
            "url": "http://localhost:8000/api/categorias/2/",
            "id": 2,
            "nome": "Educação",
            "slug": "educacao",
            "descricao": ""
        }
    ]
    ```

    create:
    Cria uma instância de categoria. A estrutura de entrada é um objeto do tipo `Categoria`.

    update:
    Atualiza a categoria.

    delete:
    Exclui a categoria.
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_fields = ('nome', 'slug', 'descricao')
    ordering_fields = '__all__'
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)


class TagViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Retorna uma tag específica, conforme o parâmetro de URL `id`. A seguir, um exemplo de retorno:

    ```json
    {
        "url": "http://localhost:8000/api/tags/1/",
        "id": 1,
        "nome": "Política",
        "slug": "politica"
    }
    ```

    list:
    Retorna uma lista das tags. A estrutura de retorno é um array de objetos do tipo `Tag`.

    Exemplo de retorno:

    ```json
    [
        {
            "url": "http://localhost:8000/api/tags/1/",
            "id": 1,
            "nome": "Política",
            "slug": "politica"
        },
        {
            "url": "http://localhost:8000/api/tags/2/",
            "id": 1,
            "nome": "Economia",
            "slug": "economia"
        }
    ]
    ```

    create:
    Cria uma instância de tag. A estrutura de entrada é um objeto do tipo `Tag`.

    update:
    Atualiza a tag.

    delete:
    Exclui a tag.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_fields = ('nome', 'slug',)
    ordering_fields = '__all__'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
