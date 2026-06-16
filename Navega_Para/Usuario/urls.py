from django.urls import path
from . import views

urlpatterns = [
    # Menu Principal
    path('menu/', views.menu_principal, name='menu'),

    # Usuários
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),

    # Paradas
    path('paradas/cadastrar/', views.cadastrar_parada, name='cadastrar_parada'),
    path('paradas/', views.listar_paradas, name='listar_paradas'),

    # Rotas
    path('rotas/cadastrar/', views.cadastrar_rotas, name='cadastrar_rotas'),
    path('rotas/', views.listar_rotas, name='listar_rotas'),

    # Passagens
    path('passagens/cadastrar/', views.cadastrar_passagem, name='cadastrar_passagem'),
    path('passagens/', views.listar_passagens, name='listar_passagens'),
]
