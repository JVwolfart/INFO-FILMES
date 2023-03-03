# INFO-FILMES

Exercício de consumo de APIs Jovem Programador SENAC

A tarefa era desenvolver um site de informações de filmes e séries baseado nas informações obtidas da API https://www.omdbapi.com/

O sistema é acessivel somente para usuários cadastrados e caso não tenha cadastro tem a possibilidade de fazer cadastro.

O site deve conter uma barra de pesquisa onde o usuário informa o termo que deseja consultar (nome do filme ou série) e o sistema consulta a API E retorna os dados da consulta.

Esta API devolve apenas 10 itens por página, portanto deve haver também no sistema uma paginação para permitir a busca de todos os dados referentees ao termo pesquisado.

O sistema deve listar todos os itens da busca e permitir que o usuário selecione algum dos itens para ver detalhes.

O usuário pode adicionar aos seus favoritos em sua conta ou também remover de seus favoritos da sua conta.

DEPENDÊNCIAS DO PROJETO

asgiref==3.5.2

certifi==2022.6.15

charset-normalizer==2.0.12

Django==4.0.5

django-environ==0.9.0

gunicorn==20.1.0

idna==3.3

psycopg2-binary==2.9.3

requests==2.28.0

sqlparse==0.4.2

urllib3==1.26.9

whitenoise==6.2.0

Para mais detalhes deste e de outros projetos acesse meu portifólio

http://jvitorwolfart.pinheirasc.com/index.php/2022/07/19/projeto-info-filmes/

Para quem quiser conhecer o site, segue abaixo o link com o deploy na minha VPS:

https://filmes.pinheirasc.com/
