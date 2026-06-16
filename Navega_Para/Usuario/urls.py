from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('escalas/', views.listar_escala, name='listar_escalas'),
    path('rotas/', views.listar_rotas, name='listar_rotas'),
    path('rotas/cadastrar/', views.cadastrar_rotas, name='cadastrar_rotas'),
    path('passagens/', views.listar_passagens, name='listar_passagens'),
    path('passagens/cadastrar/', views.cadastrar_passagem, name='cadastrar_passagem'),
]