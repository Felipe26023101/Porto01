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

    # Rotas de Edição e Exclusão
    path('rotas/editar/<int:id>/', views.editar_rota, name='editar_rota'),
    path('rotas/excluir/<int:id>/', views.excluir_rota, name='excluir_rota'),

    # Passagens de Edição e Exclusão
    path('passagens/editar/<int:id>/', views.editar_passagem, name='editar_passagem'),
    path('passagens/excluir/<int:id>/', views.excluir_passagem, name='excluir_passagem'),

    # Usuários de Edição e Exclusão
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<int:id>/', views.excluir_usuario, name='excluir_usuario'),

    # Paradas de Edição e Exclusão
    path('paradas/editar/<int:id>/', views.editar_parada, name='editar_parada'),
    path('paradas/excluir/<int:id>/', views.excluir_parada, name='excluir_parada'),

]
