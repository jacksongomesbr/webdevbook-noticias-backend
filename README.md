# webdevbook-noticias-backend

Este é um software de suporte à disciplina Linguagem de Programação para a Web, do Centro Universitário Luterano de Palmas, ministrada pelo professor Jackson Gomes (@jacksongomesbr).

O software é um backend construído sobre python, fornecendo uma API para acesso a dados de notícias. Mais especificamente, este software serve como API REST HTTP para o projeto **webdevbook-noticias-angular**.

## Executando localmente

Para executar localmente crie um ambiente python e instale os pacotes do arquivo `requirements.txt`. 

Depois, crie as migrations:

```
(venv) python manage.py migrate
```

Crie o superusuário:

```
(venv) python manage.py createsuperuser
```

Por fim, execute o projeto:

```
(venv) python manage.py runserver
```

Ao executar o projeto, a API HTTP REST estará disponível, por padrão, em `http://localhost:8000/api`.

