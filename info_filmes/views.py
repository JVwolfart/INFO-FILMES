from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import requests
from django.core.paginator import Paginator

from info_filmes.models import Favorito
# Create your views here.
chave = '4883d295'
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário ou senha inválidos')
        return render(request, 'login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Login feito com sucesso!')
        return redirect('home')

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'cadastro.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! nenhum campo pode ficar vazio')
        return render(request, 'cadastro.html')
    
    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! senhas não conferem')
        return render(request, 'cadastro.html')

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'ERRO! senha deve ter mais de 8 caracteres')
        return render(request, 'cadastro.html')

    if senha.isnumeric():
        messages.add_message(request, messages.ERROR, 'ERRO! senha não pode ser somente numérica')
        return render(request, 'cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário {usuario} já existe')
        return render(request, 'cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Email {email} já existe')
        return render(request, 'cadastro.html')
    else:
        user = User.objects.create_user(username=usuario, email=email,  password=senha, first_name=nome, last_name=sobrenome)
        user.save()
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Cadastro de {usuario} feito com sucesso, aproveite nosso site')
        return redirect('home')


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout feito com sucesso')
    return redirect('index')

@login_required(login_url='login')
def home(request):
    user = request.user
    n_fav = Favorito.objects.all().filter(
        usuario=user
    ).count()
    return render(request, 'home.html', {'n_fav':n_fav})

@login_required(login_url='login')
def busca(request):
    user = request.user
    n_fav = Favorito.objects.all().filter(
        usuario=user
    ).count()
    termo = request.GET.get('s')
    page = request.GET.get('page')
    if not page:
        page = 1
    if not termo:
        messages.add_message(request, messages.ERROR, f'Termo da pesquisa não informado')
        return redirect('home')

    chave = 'apikey=4883d295'
    response = requests.get(f'http://www.omdbapi.com/?s={termo}&page={page}&{chave}').json()
    if response['Response'] == 'False':
        messages.add_message(request, messages.ERROR, f'Termo da pesquisa {termo} não encontrado')
        return redirect('home')
    else:
        total_itens = int(response['totalResults'])
        if total_itens % 10 == 0:
            n_paginas = total_itens // 10
        else:
            n_paginas = (total_itens // 10) + 1
        paginas = []
        for c in range(1, n_paginas+1):
            paginas.append(c)
        filmes = []
        for r in response['Search']:
            filmes.append(r)
        page = int(page)
        n_paginas = int(n_paginas)
        favoritos = Favorito.objects.all().filter(
            usuario=user
        )
        filmes_favoritos = []
        if favoritos.exists():
            for f in favoritos:
                filmes_favoritos.append(f.id_filme)

        return render(request, 'pesquisa.html', {'filmes':filmes, 'termo':termo, 'n_paginas':n_paginas, 'paginas':paginas, 'page':page, 'filmes_favoritos':filmes_favoritos, 'n_fav':n_fav})

@login_required(login_url='login')
def filme(request, id):
    chave = 'apikey=4883d295'
    filme = requests.get(f'http://www.omdbapi.com/?i={id}&{chave}').json()
    user = request.user
    n_fav = Favorito.objects.all().filter(
        usuario=user
    ).count()
    id_filme = request.GET.get('id_filme')
    capa = request.GET.get('capa')
    titulo = request.GET.get('titulo')
    ano = request.GET.get('ano')
    tipo = request.GET.get('tipo')
    favoritos = Favorito.objects.all().filter(
        usuario=user, id_filme=id
    ).exists()
    if id_filme:
        if capa == 'N/A':
            capa = 'https://www.google.com/url?sa=i&url=http%3A%2F%2Fplone.ufpb.br%2Flabeet%2Fcontents%2Fpaginas%2Facervo-brazinst%2Fcopy_of_cordofones%2Fudecra%2Fsem-imagem.jpg%2Fview&psig=AOvVaw3yHd74vCgWt_YpaLuVAgVL&ust=1652363452480000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCOjiktfL1_cCFQAAAAAdAAAAABAD'
        favorito = Favorito.objects.create(usuario=user, id_filme=id_filme, capa=capa, titulo=titulo, ano=ano, tipo=tipo)
        favorito.save()
        favoritos = Favorito.objects.all().filter(
        usuario=user, id_filme=id
        ).exists()
        messages.add_message(request, messages.SUCCESS, f'Filme {titulo} adicionado aos favoritos de {user}')
    return render(request, 'filme.html', {'filme':filme, 'favoritos':favoritos, 'n_fav':n_fav})

@login_required(login_url='login')
def remover_favoritos(request, id):
    #{% url 'favoritos'?id_filme=filme.imdbID&capa=filme.Poster&titulo=filme.Title&ano=filme.Year&tipo=filme.Type%}
    user = request.user
    id_filme = id
    filme = Favorito.objects.get(usuario=user, id_filme=id)
    filme.delete()
    messages.add_message(request, messages.INFO, 'Filme removido dos favoritos')
    return redirect('filme', id_filme)

@login_required(login_url='login')
def meus_favoritos(request):
    user = request.user
    filmes = Favorito.objects.all().filter(
        usuario=user
    ).order_by('-id')
    n_fav = Favorito.objects.all().filter(
        usuario=user
    ).count()
    paginator = Paginator(filmes, 5)
    page = request.GET.get('p')
    filmes = paginator.get_page(page)
    return render(request, 'meus_favoritos.html', {'filmes':filmes, 'n_fav':n_fav})