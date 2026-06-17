from django.shortcuts import render, redirect
from .formulario import UsuarioCadastroForm, RotasForm, PassagemForm, ParadaForm
from .models import Usuario, Rotas, Passagem, Parada
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password # Importação mantida para criptografia
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def menu_principal(request):
    return render(request, "Usuario/menu.html")

# ==================== USUÁRIOS ====================
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)

            # SOLUÇÃO DO ERRO: Define o e-mail como o username único exigido pelo Django
            usuario.username = form.cleaned_data["email"]

            # Criptografa a senha usando o método correto do Django
            usuario.senha = make_password(form.cleaned_data["senha"])

            usuario.save()
            return redirect("listar_usuarios")  # Redireciona para a lista após salvar com sucesso
    else:
        form = UsuarioCadastroForm()
    return render(request, "Usuario/cadastrar_usuario.html", {"form": form})

# CORREÇÃO: Readicionada a view de listagem que havia sumido
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
            passagem.numero_bilhete = f"{proximo_numero:04d}"
            passagem.save()
            return redirect("listar_passagens")
    else:
        form = PassagemForm()
    return render(request, "Usuario/cadastrar_passagem.html", {"form": form})

def listar_passagens(request):
    passagens = Passagem.objects.all()
    return render(request, "Usuario/listar_passagens.html", {"passagens": passagens})

# ==================== EDITAR ROTA ====================
def editar_rota(request, id):
    # Busca a rota pelo ID ou retorna erro 404 se não existir
    rota = get_object_or_404(Rotas, id=id)

    if request.method == "POST":
        # Passa o 'instance=rota' para o Django saber que deve EDITAR, e não criar um novo
        form = RotasForm(request.POST, instance=rota)
        if form.is_valid():
            form.save()
            return redirect("listar_rotas")
    else:
        form = RotasForm(instance=rota)  # Carrega os dados atuais nos inputs

    return render(request, "Usuario/cadastrar_rota.html", {"form": form, "editando": True})


# ==================== EXCLUIR ROTA ====================
def excluir_rota(request, id):
    rota = get_object_or_404(Rotas, id=id)
    rota.delete()  # Remove definitivamente do banco SQLite
    return redirect("listar_rotas")


# ==================== EDITAR PASSAGEM ====================
def editar_passagem(request, id):
    passagem = get_object_or_404(Passagem, id=id)

    if request.method == "POST":
        # Envia a instância atual para que o Django atualize o registro em vez de criar um novo
        form = PassagemForm(request.POST, instance=passagem)
        if form.is_valid():
            form.save()
            return redirect("listar_passagens")
    else:
        form = PassagemForm(instance=passagem)

    return render(request, "Usuario/cadastrar_passagem.html", {"form": form, "editando": True})


# ==================== EXCLUIR PASSAGEM ====================
def excluir_passagem(request, id):
    passagem = get_object_or_404(Passagem, id=id)
    passagem.delete()
    return redirect("listar_passagens")


# ==================== EDITAR USUÁRIO ====================
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_editado = form.save(commit=False)

            # Garante que o username mude se o email mudar
            usuario_editado.username = form.cleaned_data["email"]

            if form.cleaned_data.get("senha"):
                usuario_editado.senha = make_password(form.cleaned_data["senha"])

            usuario_editado.save()
            return redirect("listar_usuarios")
    else:
        form = UsuarioCadastroForm(instance=usuario)

    return render(request, "Usuario/cadastrar_usuario.html", {"form": form, "editando": True})

# ==================== EXCLUIR USUÁRIO ====================
def excluir_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect("listar_usuarios")

# ==================== EDITAR PARADA ====================
def editar_parada(request, id):
    parada = get_object_or_404(Parada, id=id)

    if request.method == "POST":
        # Passa a instância atual para o Django atualizar o registro existente
        form = ParadaForm(request.POST, instance=parada)
        if form.is_valid():
            form.save()
            return redirect("listar_paradas")
    else:
        form = ParadaForm(instance=parada)

    return render(request, "Usuario/cadastrar_parada.html", {"form": form, "editando": True})


# ==================== EXCLUIR PARADA ====================
def excluir_parada(request, id):
    parada = get_object_or_404(Parada, id=id)
    parada.delete()
    return redirect("listar_paradas")