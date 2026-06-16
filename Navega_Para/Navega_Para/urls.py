from django.contrib import admin
from django.urls import path, include
from Usuario import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('Usuario.urls')),

    # Página inicial = login
    path('', auth_views.LoginView.as_view(template_name="login.html"), name="login"),

    # Menu protegido
    path('menu/', views.menu_principal, name="menu"),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout"),
]
