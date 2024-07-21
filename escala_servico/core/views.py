from django.shortcuts import render
from core.models import Militar, ServicoDiario, DiaNaoUtil, FolgaDiaria
from core.utils import gerar_previsao_servico
from django.contrib import messages
from collections import defaultdict
import calendar
from datetime import datetime

def index(request):
    return render(request, 'core/index.html')

def gerar_previsao_servico_view(request):
    mensagem = ""
    try:
        mensagem = gerar_previsao_servico()
        messages.success(request, mensagem)
    except Exception as e:
        mensagem = f"Erro ao gerar previsão de serviço: {str(e)}"
        messages.error(request, mensagem)
    return render(request, 'core/gerar_previsao.html', {'mensagem': mensagem})

def visualizar_previsao(request):
    hoje = datetime.now().date()
    _, ultimo_dia = calendar.monthrange(hoje.year, hoje.month)
    dias_mes = [hoje.replace(day=dia) for dia in range(1, ultimo_dia + 1)]

    calendario = gerar_previsao_servico()

    calendario_template = [
        {"militar": militar, "dias": [{"data": dia, **calendario[militar][dia]} for dia in dias_mes]}
        for militar in calendario
    ]

    return render(request, 'core/visualizar_previsao.html', {
        'calendario': calendario_template,
        'dias_mes': dias_mes
    })

def atualizar_previsao_servico(request):
    mensagem = ""
    try:
        mensagem = gerar_previsao_servico()
        messages.success(request, mensagem)
    except Exception as e:
        mensagem = f"Erro ao atualizar previsão de serviço: {str(e)}"
        messages.error(request, mensagem)
    return render(request, 'core/gerar_previsao.html', {'mensagem': mensagem})