from django.db import models

class Militar(models.Model):
    TIPO_ESCALA_CHOICES = [
        ('Oficial de Dia', 'Oficial de Dia'),
        ('Adjunto', 'Adjunto ao Oficial de Dia'),
        ('Comandante da Guarda', 'Comandante da Guarda'),
        ('Cabo da Guarda', 'Cabo da Guarda'),
        ('Cabo da Guarda do PNR', 'Cabo da Guarda do PNR'),
    ]

    nome = models.CharField(max_length=100)
    tipo_escala = models.CharField(max_length=50, choices=TIPO_ESCALA_CHOICES)
    status = models.BooleanField(default=True)
    data_entrada = models.DateField()
    folga_util = models.IntegerField(default=0)
    folga_nao_util = models.IntegerField(default=0)
    indisponibilidades = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class ServicoDiario(models.Model):
    TIPO_ESCALA_CHOICES = [
        ('Oficial de Dia', 'Oficial de Dia'),
        ('Adjunto', 'Adjunto ao Oficial de Dia'),
        ('Comandante da Guarda', 'Comandante da Guarda'),
        ('Cabo da Guarda', 'Cabo da Guarda'),
        ('Cabo da Guarda do PNR', 'Cabo da Guarda do PNR'),
    ]

    TIPO_DIA_CHOICES = [
        ('util', 'Útil'),
        ('nao_util', 'Não Útil'),
    ]

    tipo_escala = models.CharField(max_length=50, choices=TIPO_ESCALA_CHOICES)
    data = models.DateField()
    militar = models.ForeignKey(Militar, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    tipo_dia = models.CharField(max_length=10, choices=TIPO_DIA_CHOICES)
    folga = models.IntegerField(default=0)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.data} - {self.tipo_escala} - {self.militar.nome}'



class DiaNaoUtil(models.Model):
    data = models.DateField()
    descricao = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.data} - {self.descricao}'

class FolgaDiaria(models.Model):
    data = models.DateField()
    militar = models.ForeignKey(Militar, on_delete=models.CASCADE)
    folga = models.IntegerField()
    tipo_dia = models.CharField(max_length=10)  # útil ou não útil