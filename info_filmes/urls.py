from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('busca/', views.busca, name='busca'),
    path('filme/<str:id>', views.filme, name='filme'),
    path('remover_favoritos/<str:id>', views.remover_favoritos, name='remover_favoritos'),
    path('meus_favoritos/', views.meus_favoritos, name='meus_favoritos'),
]