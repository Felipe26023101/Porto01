from django.urls import path
from . import views

urlpatterns = [
    # Rotas de Usuário
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('listar_usuario/', views.listar_usuarios, name='listar_usuarios'),

    # Rotas de Escala (Corrigido para views.listar_escala no singular)
    path('cadastrar_escala/', views.cadastrar_escala, name='cadastrar_escala'),
    path('listar_escala/', views.listar_escala, name='listar_escalas'),

    # Rotas de Rota
    path('cadastrar_rota/', views.cadastrar_rotas, name='cadastrar_rota'),
    path('listar_rotas/', views.listar_rotas, name='listar_rotas'),

    # Rotas de Passagem
    path('cadastrar_passagem/', views.cadastrar_passagem, name='cadastrar_passagem'),
    path('listar_passagens/', views.listar_passagens, name='listar_passagens'),
]