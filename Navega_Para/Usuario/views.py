from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied  # Importação necessária para bloquear acessos
from .formulario import UsuarioCadastroForm, RotasForm, PassagemForm, ParadaForm
from .models import Usuario, Rotas, Passagem, Parada
from django.contrib.auth.decorators import login_required


# ==================== MENU PRINCIPAL ====================
@login_required
def menu_principal(request):
    return render(request, "Usuario/menu.html")


# ==================== USUÁRIOS ====================
@login_required
def cadastrar_usuario(request):
    # Restrição: Apenas Admin e Operador (guiche) podem cadastrar
    if request.user.tipo_de_usuario not in ['administrador', 'guiche']:
        raise PermissionDenied

    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.username = form.cleaned_data["email"]
            usuario.set_password(form.cleaned_data["senha"])
            usuario.save()
            return redirect("listar_usuarios")
    else:
        form = UsuarioCadastroForm()
    return render(request, "Usuario/cadastrar_usuario.html", {"form": form})


@login_required
def listar_usuarios(request):
    # Restrição: Apenas Admin e Operador podem listar usuários
    if request.user.tipo_de_usuario not in ['administrador', 'guiche']:
        raise PermissionDenied
    usuarios = Usuario.objects.all()
    return render(request, 'Usuario/listar_usuarios.html', {'usuarios': usuarios})


@login_required
def editar_usuario(request, id):
    # Restrição: Apenas Administrador pode editar usuários
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == "POST":
        form = UsuarioCadastroForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_editado = form.save(commit=False)
            usuario_editado.username = form.cleaned_data["email"]
            if form.cleaned_data.get("senha"):
                usuario_editado.set_password(form.cleaned_data["senha"])
            usuario_editado.save()
            return redirect("listar_usuarios")
    else:
        form = UsuarioCadastroForm(instance=usuario)
    return render(request, "Usuario/cadastrar_usuario.html", {"form": form, "editando": True})


@login_required
def excluir_usuario(request, id):
    # Restrição: Apenas Administrador pode apagar
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect("listar_usuarios")


# ==================== PARADAS ====================
@login_required
def cadastrar_parada(request):
    # Restrição: Apenas Administrador pode adicionar novas paradas
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    if request.method == 'POST':
        form = ParadaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_paradas')
    else:
        form = ParadaForm()
    return render(request, 'Usuario/cadastrar_parada.html', {'form': form})


@login_required
def listar_paradas(request):
    # Qualquer usuário logado (Admin, Operador ou Passageiro) pode ver
    paradas = Parada.objects.all().select_related('rota')
    return render(request, 'Usuario/listar_paradas.html', {'paradas': paradas})


@login_required
def editar_parada(request, id):
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    parada = get_object_or_404(Parada, id=id)
    if request.method == "POST":
        form = ParadaForm(request.POST, instance=parada)
        if form.is_valid():
            form.save()
            return redirect("listar_paradas")
    else:
        form = ParadaForm(instance=parada)
    return render(request, "Usuario/cadastrar_parada.html", {"form": form, "editando": True})


@login_required
def excluir_parada(request, id):
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    parada = get_object_or_404(Parada, id=id)
    parada.delete()
    return redirect("listar_paradas")


# ==================== ROTAS ====================
@login_required
def cadastrar_rotas(request):
    # Restrição: Apenas Administrador pode adicionar rotas
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    if request.method == "POST":
        form = RotasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_rotas")
    else:
        form = RotasForm()
    return render(request, "Usuario/cadastrar_rota.html", {"form": form})


@login_required
def listar_rotas(request):
    # Todos os tipos de usuários podem ver a listagem de rotas
    rotas = Rotas.objects.all()
    return render(request, "Usuario/listar_rotas.html", {"rotas": rotas})


@login_required
def editar_rota(request, id):
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    rota = get_object_or_404(Rotas, id=id)
    if request.method == "POST":
        form = RotasForm(request.POST, instance=rota)
        if form.is_valid():
            form.save()
            return redirect("listar_rotas")
    else:
        form = RotasForm(instance=rota)
    return render(request, "Usuario/cadastrar_rota.html", {"form": form, "editando": True})


@login_required
def excluir_rota(request, id):
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    rota = get_object_or_404(Rotas, id=id)
    rota.delete()
    return redirect("listar_rotas")


# ==================== PASSAGENS ====================
@login_required
def cadastrar_passagem(request):
    # Restrição: Apenas Admin e Operador (guiche) emitem passagens
    if request.user.tipo_de_usuario not in ['administrador', 'guiche']:
        raise PermissionDenied
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


@login_required
def listar_passagens(request):
    # REGRA CRUCIAL: Se for Passageiro (cliente), filtra apenas as passagens DELE
    if request.user.tipo_de_usuario == 'cliente':
        passagens = Passagem.objects.filter(passageiro=request.user)
    else:
        # Se for Admin ou Operador, vê todas as passagens do sistema
        passagens = Passagem.objects.all()
    return render(request, "Usuario/listar_passagens.html", {"passagens": passagens})


@login_required
def editar_passagem(request, id):
    # Restrição: Admin e Operador podem editar passagens
    if request.user.tipo_de_usuario not in ['administrador', 'guiche']:
        raise PermissionDenied
    passagem = get_object_or_404(Passagem, id=id)
    if request.method == "POST":
        form = PassagemForm(request.POST, instance=passagem)
        if form.is_valid():
            form.save()
            return redirect("listar_passagens")
    else:
        form = PassagemForm(instance=passagem)
    return render(request, "Usuario/cadastrar_passagem.html", {"form": form, "editando": True})


@login_required
def excluir_passagem(request, id):
    # Restrição: APENAS Administrador pode apagar/cancelar uma passagem
    if request.user.tipo_de_usuario != 'administrador':
        raise PermissionDenied
    passagem = get_object_or_404(Passagem, id=id)
    passagem.delete()
    return redirect("listar_passagens")
