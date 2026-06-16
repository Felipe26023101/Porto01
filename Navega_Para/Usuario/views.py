from django.shortcuts import render, redirect
from .formulario import UsuarioCadastroForm, RotasForm, PassagemForm, ParadaForm
from .models import Usuario, Rotas, Passagem, Parada
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

@login_required
def menu_principal(request):
    return render(request, "Usuario/menu.html")

# ==================== USUÁRIOS ====================
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = make_password(form.cleaned_data["senha"])
            usuario.save()
            return redirect("menu")
    else:
        form = UsuarioCadastroForm()
    return render(request, "Usuario/cadastrar_usuario.html", {"form": form})

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'Usuario/listar_usuarios.html', {'usuarios': usuarios})

# ==================== PARADAS ====================
def cadastrar_parada(request):
    if request.method == 'POST':
        form = ParadaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_paradas')
    else:
        form = ParadaForm()
    return render(request, 'Usuario/cadastrar_parada.html', {'form': form})

def listar_paradas(request):
    paradas = Parada.objects.all().select_related('rota')
    return render(request, 'Usuario/listar_paradas.html', {'paradas': paradas})

# ==================== ROTAS ====================
def cadastrar_rotas(request):
    if request.method == "POST":
        form = RotasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_rotas")
    else:
        form = RotasForm()

    return render(request, "Usuario/cadastrar_rota.html", {"form": form})

def listar_rotas(request):
    rotas = Rotas.objects.all()
    return render(request, "Usuario/listar_rotas.html", {"rotas": rotas})

# ==================== PASSAGENS ====================
def cadastrar_passagem(request):
    if request.method == "POST":
        form = PassagemForm(request.POST)
        if form.is_valid():
            passagem = form.save(commit=False)

            total_passagens = Passagem.objects.count()
            proximo_numero = total_passagens + 1

            passagem.numero_bilhete = f"{proximo_numero:04d}"  # Gera '0001', '0002', etc.

            passagem.save()
            return redirect("listar_passagens")
    else:
        form = PassagemForm()
    return render(request, "Usuario/cadastrar_passagem.html", {"form": form})

def listar_passagens(request):
    passagens = Passagem.objects.all()
    return render(request, "Usuario/listar_passagens.html", {"passagens": passagens})
