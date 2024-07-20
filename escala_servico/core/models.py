from django.db import models

class Militar(models.Model):
    nome = models.CharField(max_length=100)
    posto = models.CharField(max_length=50)
    data_entrada = models.DateField()
    suspenso_ate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

FUNCOES_CHOICES = [
    ('OFICIAL_DIA', 'Oficial de Dia'),
    ('ADJUNTO_OF_DIA', 'Adjunto ao Oficial de Dia'),
    ('COMANDANTE_GUARDA', 'Comandante da Guarda'),
    ('CABO_GUARDA', 'Cabo da Guarda'),
    ('CABO_GUARDA_PNR', 'Cabo da Guarda do PNR'),
]

TIPO_ESCALA = [
    ('preta', 'Preta'),
    ('vermelha', 'Vermelha'),
]

class Escala(models.Model):
    data = models.DateField()
    tipo = models.CharField(max_length=8, choices=TIPO_ESCALA)
    militar = models.ForeignKey(Militar, on_delete=models.CASCADE)
    funcao = models.CharField(max_length=20, choices=FUNCOES_CHOICES)

    def __str__(self):
        return f"{self.data} - {self.militar.nome} - {self.funcao}"
