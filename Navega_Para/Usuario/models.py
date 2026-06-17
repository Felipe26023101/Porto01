from django.db import models
from django.contrib.auth.models import AbstractUser  # Importação necessária


class Usuario(AbstractUser):  # Alterado de models.Model para AbstractUser
    TIPO_CHOICES = [
        ('cliente', 'Passageiro'),
        ('guiche', 'Guichê / Operador'),
        ('administrador', 'Administrador'),
    ]

    # O AbstractUser JÁ CRIA internamente os campos:
    # username, password (senha), first_name, last_name, email, is_staff, is_active, etc.
    # Por isso, removemos o campo 'senha' e 'email' manuais daqui para não duplicar.

    nome = models.CharField(max_length=100)
    tipo_de_usuario = models.CharField(max_length=50, choices=TIPO_CHOICES)
    celular = models.CharField(max_length=20)

    # Definimos que o campo 'nome' será usado como primeiro nome no Django
    def save(self, *args, **kwargs):
        if self.nome:
            self.first_name = self.nome
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_de_usuario_display()})"


# As tabelas Rotas, Parada e Passagem continuam EXATAMENTE IGUAIS abaixo...
class Rotas(models.Model):
    ponto_de_partida = models.CharField(max_length=100)
    ponto_de_chegada = models.CharField(max_length=100)
    dias_da_semana = models.CharField(max_length=50)
    horario_saida = models.TimeField()

    def __str__(self): return f"{self.ponto_de_partida} → {self.ponto_de_chegada}"


class Parada(models.Model):
    rota = models.ForeignKey(Rotas, on_delete=models.CASCADE, related_name='paradas')
    local_parada = models.CharField(max_length=255, verbose_name="Local da Parada")
    ordem = models.IntegerField(verbose_name="Ordem da Parada")
    horario_estimado = models.TimeField(verbose_name="Horário Estimado")

    def __str__(self): return f"{self.local_parada} ({self.rota})"


class Passagem(models.Model):
    rota = models.ForeignKey(Rotas, on_delete=models.CASCADE, verbose_name="Rota")
    passageiro = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Passageiro")
    numero_bilhete = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Número do Bilhete")
    ponto_embarque = models.CharField(max_length=255, verbose_name="Ponto de Embarque")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço (R$)")

    def __str__(self): return f"Bilhete {self.numero_bilhete} - {self.passageiro.nome}"
