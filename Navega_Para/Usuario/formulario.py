from django import forms
from .models import Usuario, Escala, Viagem, Rotas, Passagem


class UsuarioCadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirmar_senha = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = Usuario
        fields = ["nome", "tipo_de_usuario", "email", "celular", "senha"]

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        # Campos reais do modelo Viagem no seu models.py
        fields = ["rota", "administrador", "data_partida", "horario_saida", "capacidade_maxima"]

class EscalaForm(forms.ModelForm):
    class Meta:
        model = Escala
        # Campos reais do modelo Escala no seu models.py
        fields = ["rota", "local_parada", "ordem", "horario_estimado"]

# Caso precise criar também o formulário de Rotas e Passagens no futuro:
class RotasForm(forms.ModelForm):
    class Meta:
        model = Rotas
        fields = ["ponto_de_partida", "ponto_de_chegada", "dias_da_semana", "horario_saida"]

class PassagemForm(forms.ModelForm):
    class Meta:
        model = Passagem
        fields = ["viagem", "passageiro", "numero_bilhete", "ponto_embarque", "ponto_desembarque"]
