from datetime import date, timedelta
from .models import DiaNaoUtil, Militar

def adicionar_finais_de_semana_e_feriados(inicio, fim):
    dia_atual = inicio
    feriados = [
        {'data': date(2024, 1, 1), 'descricao': 'Ano Novo'},
        {'data': date(2024, 12, 25), 'descricao': 'Natal'},
        # Adicione mais feriados conforme necessário
    ]

    while dia_atual <= fim:
        if dia_atual.weekday() == 5 or dia_atual.weekday() == 6:  # 5 é sábado, 6 é domingo
            DiaNaoUtil.objects.get_or_create(data=dia_atual, defaults={'descricao': 'Final de semana'})
        for feriado in feriados:
            if feriado['data'] == dia_atual:
                DiaNaoUtil.objects.get_or_create(data=dia_atual, defaults={'descricao': feriado['descricao']})
        dia_atual += timedelta(days=1)

def atualizar_folgas():
    militares = Militar.objects.all()
    for militar in militares:
        militar.folga_util += 1  # Incrementa a folga útil
        militar.folga_nao_util += 1  # Incrementa a folga não útil
        militar.save()