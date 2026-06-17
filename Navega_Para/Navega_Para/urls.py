from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importa as views prontas do Django

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rota do Login Customizado
    path('', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),

    # CORREÇÃO DO ERRO: Adicionada a rota oficial de Logout do Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Inclui as rotas do seu aplicativo Usuario
    path('usuario/', include('Usuario.urls')),
]
