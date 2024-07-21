from django.core.management.base import BaseCommand
from core.models import Militar, ServicoDiario, DiaNaoUtil, FolgaDiaria
from datetime import datetime
import calendar
from collections import defaultdict

class Command(BaseCommand):
    help = 'Popula a tabela FolgaDiaria com os dados de folga dos militares'

    def handle(self, *args, **kwargs):
        militares = Militar.objects.filter(status=True)
        hoje = datetime.now().date()
        _, ultimo_dia = calendar.monthrange(hoje.year, hoje.month)
        dias_mes = [hoje.replace(day=dia) for dia in range(1, ultimo_dia + 1)]

        # Inicializar a estrutura de dados
        calendario = defaultdict(lambda: defaultdict(lambda: {"folga": None, "tipo_dia": "útil"}))

        # Preencher o calendário com os serviços diários
        previsao = ServicoDiario.objects.all().order_by('data')
        for servico in previsao:
            calendario[servico.militar.nome][servico.data] = {
                "folga": servico.folga,
                "tipo_dia": servico.tipo_dia
            }

        # Marcar os dias não úteis
        dias_nao_uteis = DiaNaoUtil.objects.filter(data__month=hoje.month)
        for dia in dias_nao_uteis:
            for militar in militares:
                calendario[militar.nome][dia.data]["tipo_dia"] = "não útil"

        # Popular a tabela FolgaDiaria
        FolgaDiaria.objects.all().delete()  # Limpar tabela existente
        for militar in militares:
            for dia in dias_mes:
                folga = calendario[militar.nome][dia]["folga"]
                tipo_dia = calendario[militar.nome][dia]["tipo_dia"]
                FolgaDiaria.objects.create(data=dia, militar=militar, folga=folga if folga is not None else 0, tipo_dia=tipo_dia)

        self.stdout.write(self.style.SUCCESS('Tabela FolgaDiaria populada com sucesso'))
