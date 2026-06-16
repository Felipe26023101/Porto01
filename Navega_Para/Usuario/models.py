from django.db import models

class Usuario(models.Model):
    TIPO_CHOICES = [
        ('cliente', 'Passageiro'),
        ('guiche', 'Guichê / Operador'),
        ('administrador', 'Administrador'),
    ]

    nome = models.CharField(max_length=100)
    tipo_de_usuario = models.CharField(max_length=50, choices=TIPO_CHOICES)
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=20)
    senha = models.CharField(max_length=128, default="")  # senha criptografada

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_de_usuario_display()})"


class Rotas(models.Model):
    ponto_de_partida = models.CharField(max_length=100)
    ponto_de_chegada = models.CharField(max_length=100)
    dias_da_semana = models.CharField(max_length=50)
    horario_saida = models.TimeField()

    def __str__(self):
        return f"{self.ponto_de_partida} → {self.ponto_de_chegada}"

class Parada(models.Model):
    # Vincula a parada diretamente a uma Rota específica
    rota = models.ForeignKey(Rotas, on_delete=models.CASCADE, related_name='paradas')
    local_parada = models.CharField(max_length=255, verbose_name="Local da Parada")
    ordem = models.IntegerField(verbose_name="Ordem da Parada")
    horario_estimado = models.TimeField(verbose_name="Horário Estimado")

    def __str__(self):
        return f"{self.local_parada} ({self.rota})"

class Passagem(models.Model):
    rota = models.ForeignKey(Rotas, on_delete=models.CASCADE, verbose_name="Rota")
    passageiro = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Passageiro")

    numero_bilhete = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Número do Bilhete")
    ponto_embarque = models.CharField(max_length=255, verbose_name="Ponto de Embarque")

    def __str__(self):
        return f"Bilhete {self.numero_bilhete} - {self.passageiro.nome}"
