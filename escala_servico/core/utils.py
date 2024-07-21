from datetime import date, timedelta
from .models import DiaNaoUtil, Militar, ServicoDiario
import calendar


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



# utils.py atualizado
from datetime import datetime, timedelta
from core.models import Militar, ServicoDiario, DiaNaoUtil


def gerar_previsao_servico():
    militares = Militar.objects.filter(status=True)
    hoje = datetime.now().date()
    _, ultimo_dia = calendar.monthrange(hoje.year, hoje.month)
    dias_mes = [hoje.replace(day=dia) for dia in range(1, ultimo_dia + 1)]

    calendario = {militar.nome: {dia: {"folga": 0, "tipo_dia": "útil"} for dia in dias_mes} for militar in militares}

    # Inicializar as folgas com valores atuais
    folgas = {militar.nome: {"folga_util": militar.folga_util, "folga_nao_util": militar.folga_nao_util} for militar in militares}

    for dia in dias_mes:
        dia_nao_util = DiaNaoUtil.objects.filter(data=dia).exists()
        for militar in militares:
            if dia_nao_util:
                folgas[militar.nome]["folga_nao_util"] += 1
                calendario[militar.nome][dia]["tipo_dia"] = "não útil"
                calendario[militar.nome][dia]["folga"] = folgas[militar.nome]["folga_nao_util"]
            else:
                folgas[militar.nome]["folga_util"] += 1
                calendario[militar.nome][dia]["tipo_dia"] = "útil"
                calendario[militar.nome][dia]["folga"] = folgas[militar.nome]["folga_util"]

        # Selecionar o militar com maior folga útil para o serviço
        militar_escalado = max(militares, key=lambda m: folgas[m.nome]["folga_util"])
        calendario[militar_escalado.nome][dia]["folga"] = 0  # Zerar a folga no dia do serviço
        folgas[militar_escalado.nome]["folga_util"] = 0  # Resetar a folga útil do militar escalado

    return calendario


