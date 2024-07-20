from django.shortcuts import render
from core.models import Militar, ServicoDiario, DiaNaoUtil
from core.utils import gerar_previsao_servico
from django.contrib import messages

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
    previsao = ServicoDiario.objects.all().order_by('data')
    return render(request, 'core/visualizar_previsao.html', {'previsao': previsao})

def atualizar_previsao_servico(request):
    mensagem = ""
    try:
        mensagem = gerar_previsao_servico()
        messages.success(request, mensagem)
    except Exception as e:
        mensagem = f"Erro ao atualizar previsão de serviço: {str(e)}"
        messages.error(request, mensagem)
    return render(request, 'core/gerar_previsao.html', {'mensagem': mensagem})
