from django import forms
# REMOVIDO: 'Viagem' da linha abaixo
from .models import Usuario, Rotas, Passagem, Parada

# 1. CLASSE BASE AUTOMATIZADA PARA BOOTSTRAP
class BootstrapModelForm(forms.ModelForm):
    """Classe base que injeta classes do Bootstrap automaticamente em todos os campos"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nome_campo, campo in self.fields.items():
            placeholder_texto = f"Digite o(a) {campo.label.lower()}" if campo.label else ""
            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(campo.widget, forms.RadioSelect):
                campo.widget.attrs.update({'class': 'form-check-input'})
            else:
                campo.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': placeholder_texto
                })

# 2. SEUS FORMULÁRIOS HERDANDO A AUTOMAÇÃO
class UsuarioCadastroForm(BootstrapModelForm):
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput())
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

# NOTA: O 'ViagemForm' foi totalmente removido daqui!

class ParadaForm(BootstrapModelForm):
    class Meta:
        model = Parada
        fields = ["rota", "local_parada", "ordem", "horario_estimado"]
        widgets = {
            'horario_estimado': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

class RotasForm(BootstrapModelForm):
    class Meta:
        model = Rotas
        fields = ["ponto_de_partida", "ponto_de_chegada", "dias_da_semana", "horario_saida"]
        widgets = {
            'horario_saida': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

class NomePassageiroModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nome

class PassagemForm(BootstrapModelForm):
    passageiro = NomePassageiroModelChoiceField(queryset=Usuario.objects.all(), label="Passageiro")
    class Meta:
        model = Passagem
        fields = ["rota", "passageiro", "ponto_embarque"]
