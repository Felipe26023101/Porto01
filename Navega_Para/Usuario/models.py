from django.db import models

class Usuario(models.Model):
    TIPO_CHOICES = [
        ('cliente', 'Passageiro'),
        ('guiche', 'Guichê / Operador'),
        ('administrador', 'Administrador'),
    ]

    nome = models.CharField(max_length=100)
    tipo_de_usuario = models.CharField(max_length=50, choices=TIPO_CHOICES)
    email = models.EmailField()
    celular = models.CharField(max_length=20)
    senha = models.CharField(max_length=20)
    confirmacao = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.nome}"

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_de_usuario_display()})"


class Rotas(models.Model):
    ponto_de_partida = models.CharField(max_length=100)
    ponto_de_chegada = models.CharField(max_length=100)
    dias_da_semana = models.CharField(max_length=50)
    horario_saida = models.TimeField()

    def __str__(self):
        return f"{self.ponto_de_partida} x {self.ponto_de_chegada}"


class Escala(models.Model):
    rota = models.ForeignKey(Rotas, on_delete=models.CASCADE, related_name='escalas')
    local_parada = models.CharField(max_length=100)
    ordem = models.PositiveIntegerField(help_text="Ordem da parada no trajeto")
    horario_estimado = models.TimeField()

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.local_parada} (Parada da rota {self.rota})"


class Viagem(models.Model):
    rota = models.ForeignKey(Rotas, on_delete=models.CASCADE, related_name='viagens')
    administrador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'tipo_de_usuario': 'administrador'}
    )
    data_partida = models.DateField()
    horario_saida = models.TimeField()
    capacidade_maxima = models.PositiveIntegerField()

    @property
    def total_passageiros(self):
        return self.passagens.count()

    def __str__(self):
        return f"Viagem {self.rota} - {self.data_partida} às {self.horario_saida}"


class Passagem(models.Model):
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='passagens')
    passageiro = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='minhas_passagens')
    numero_bilhete = models.CharField(max_length=20, unique=True)
    data_emissao = models.DateTimeField(auto_now_add=True)
    ponto_embarque = models.CharField(max_length=100)
    ponto_desembarque = models.CharField(max_length=100)

    def __str__(self):
        return f"Bilhete {self.numero_bilhete} - {self.passageiro.nome}"
