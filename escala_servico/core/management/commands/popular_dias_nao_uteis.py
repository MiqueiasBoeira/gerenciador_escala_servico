from django.core.management.base import BaseCommand
from core.utils import adicionar_finais_de_semana_e_feriados
from datetime import date

class Command(BaseCommand):
    help = 'Popula a tabela DiaNaoUtil com os finais de semana e feriados'

    def handle(self, *args, **kwargs):
        inicio = date(2024, 1, 1)
        fim = date(2024, 12, 31)
        adicionar_finais_de_semana_e_feriados(inicio, fim)
        self.stdout.write(self.style.SUCCESS('Tabela DiaNaoUtil populada com sucesso'))
