from datetime import datetime, timedelta
from .models import Militar, Escala, FUNCOES_CHOICES

def gerar_previsao_escala():
    hoje = datetime.now().date()
    dias = [hoje + timedelta(days=i) for i in range(14)]  # Gera a previsão para 14 dias

    militares = list(Militar.objects.all())
    previsao = []

    for dia in dias:
        if dia.weekday() < 5:
            tipo = 'preta'
        else:
            tipo = 'vermelha'

        for funcao in FUNCOES_CHOICES:
            militar = sorted(militares, key=lambda m: (m.folgas.filter(tipo=tipo).count(), m.nome))[0]
            Escala.objects.create(data=dia, tipo=tipo, militar=militar, funcao=funcao[0])
            previsao.append((dia, tipo, militar, funcao[1]))

    return previsao
