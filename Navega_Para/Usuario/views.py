from django.shortcuts import render, redirect  # AJUSTE 1: Adicionado o redirect aqui
from .formulario import UsuarioCadastroForm, EscalaForm, ViagemForm, RotasForm, PassagemForm
from .models import Usuario, Escala, Viagem, Rotas, Passagem  # AJUSTE 3: Importado Rotas e Passagem que faltavam
from django.contrib.auth.decorators import login_required

@login_required
def menu_principal(request):
    return render(request, "Usuario/menu.html")

# ==================== USUÁRIOS ====================
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Se quiser salvar a senha criptografada:
            from django.contrib.auth.hashers import make_password
            usuario.senha = make_password(form.cleaned_data["senha"])
            usuario.save()
            return redirect("menu")
    else:
        form = UsuarioCadastroForm()
    return render(request, "Usuario/cadastrar_usuario.html", {"formulario": form})


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'Usuario/listar_usuarios.html', {'usuarios': usuarios})


# ==================== ESCALAS ====================
def cadastrar_escala(request):
    if request.method == "POST":
        form = EscalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_escalas")  # Nome da rota ajustado conforme seu urls.py
    else:
        form = EscalaForm()
    return render(request, "Usuario/cadastrar_escala.html", {"formulario": form})


def listar_escala(request):
    escalas = Escala.objects.all()
    # AJUSTE 5: Adicionado aspas no template
    return render(request, "Usuario/listar_escala.html", {"escalas": escalas})


# ==================== ROTAS ====================
def cadastrar_rotas(request):
    if request.method == "POST":
        form = RotasForm(request.POST)  # AJUSTE 6: Corrigido para usar o formulário de Rotas, não de Viagem
        if form.is_valid():
            form.save()
            return redirect("listar_rotas")
    else:
        form = RotasForm()
    return render(request, "Usuario/cadastrar_rota.html", {"formulario": form})


def listar_rotas(request):
    # AJUSTE 7: Mudado de Viagem para Rotas, para listar os dados da tabela certa
    rotas = Rotas.objects.all()
    return render(request, "Usuario/listar_rotas.html", {"rotas": rotas})


# ==================== PASSAGENS ====================
def cadastrar_passagem(request):
    if request.method == "POST":
        form = PassagemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_passagens")
    else:
        form = PassagemForm()
    return render(request, "Usuario/cadastrar_passagem.html", {"formulario": form})


def listar_passagens(request):
    passagens = Passagem.objects.all()
    # AJUSTE 8: Removido os parênteses errados, adicionado o 'render' que faltava e corrigido para string com aspas
    return render(request, "Usuario/listar_passagens.html", {"passagens": passagens})
