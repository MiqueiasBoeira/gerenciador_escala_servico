from datetime import date, timedelta
from .models import DiaNaoUtil, Militar, ServicoDiario

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
    # Pegando todos os militares da escala de Oficial de Dia
    militares = Militar.objects.filter(status=True, tipo_escala='Oficial de Dia').order_by('-folga_util', '-folga_nao_util')
    hoje = datetime.now().date()
    previsao_ate = hoje + timedelta(days=30)

    # Inicializando folgas nulas como zero
    for militar in militares:
        militar.folga_util = 0 if militar.folga_util is None else militar.folga_util
        militar.folga_nao_util = 0 if militar.folga_nao_util is None else militar.folga_nao_util

    print(f"Militares iniciais: {[f'{m.nome} (folga útil: {m.folga_util}, folga não útil: {m.folga_nao_util})' for m in militares]}")

    # Gerando a previsão
    for dia in range((previsao_ate - hoje).days):
        data = hoje + timedelta(days=dia)
        tipo_dia = 'útil' if data.weekday() < 5 else 'não útil'
        dia_nao_util = DiaNaoUtil.objects.filter(data=data).exists()
        if dia_nao_util:
            tipo_dia = 'não útil'

        # Gerar previsão apenas para Oficial de Dia
        tipo_escala = 'Oficial de Dia'
        # Filtrar militares com folga maior que zero
        militares_disponiveis = [m for m in militares if (m.folga_util > 0 if tipo_dia == 'útil' else m.folga_nao_util > 0)]

        if not militares_disponiveis:
            # Se nenhum militar tem folga > 0, selecionar o primeiro da lista original
            militar_designado = militares[0]
        else:
            # Selecionar o militar com maior folga disponível
            militar_designado = militares_disponiveis[0]

        ServicoDiario.objects.create(
            tipo_escala=tipo_escala,
            data=data,
            militar=militar_designado,
            status=True,
            tipo_dia=tipo_dia
        )

        print(f"Designado: {militar_designado.nome} para {tipo_escala} em {data} (tipo de dia: {tipo_dia})")

        # Zerando a folga do militar de serviço e incrementando a folga dos outros
        for militar in militares:
            if militar == militar_designado:
                if tipo_dia == 'útil':
                    militar.folga_util = 0
                else:
                    militar.folga_nao_util = 0
            else:
                if tipo_dia == 'útil':
                    militar.folga_util += 1
                else:
                    militar.folga_nao_util += 1

        # Reordenando a lista de militares
        militares = sorted(militares, key=lambda m: (m.folga_util, m.folga_nao_util), reverse=True)
        print(f"Militares atualizados: {[f'{m.nome} (folga útil: {m.folga_util}, folga não útil: {m.folga_nao_util})' for m in militares]}")

    return "Previsão de serviço gerada com sucesso"