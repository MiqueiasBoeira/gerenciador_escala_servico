from django.shortcuts import render
from django.http import HttpResponse
from .utils import adicionar_finais_de_semana_e_feriados, atualizar_folgas
from .models import Militar, ServicoDiario
from datetime import date, timedelta


def index(request):
    return render(request, 'core/index.html')


def gerar_previsao_servico(request):
    inicio = date.today()
    fim = inicio + timedelta(days=30)  # Gera previsão para os próximos 30 dias
    adicionar_finais_de_semana_e_feriados(inicio, fim)
    atualizar_folgas()  # Atualiza as folgas antes de gerar a previsão

    # Lógica para gerar a previsão de serviço
    dias = (fim - inicio).days + 1
    for dia in range(dias):
        data_servico = inicio + timedelta(days=dia)
        militares = Militar.objects.filter(status=True).order_by('folga_util')
        if data_servico.weekday() < 5:  # Dias úteis
            for militar in militares:
                ServicoDiario.objects.create(
                    tipo_escala=militar.tipo_escala,
                    data=data_servico,
                    militar=militar,
                    status=True,
                    tipo_dia='util'
                )
                # Atualizar a folga do militar (exemplo simplificado)
                militar.folga_util = 0
                militar.save()
                break  # Atribuir serviço a apenas um militar por dia como exemplo
        else:  # Dias não úteis
            for militar in militares:
                ServicoDiario.objects.create(
                    tipo_escala=militar.tipo_escala,
                    data=data_servico,
                    militar=militar,
                    status=True,
                    tipo_dia='nao_util'
                )
                # Atualizar a folga do militar (exemplo simplificado)
                militar.folga_nao_util = 0
                militar.save()
                break  # Atribuir serviço a apenas um militar por dia como exemplo

    return render(request, 'core/gerar_previsao.html')


def visualizar_previsao(request):
    inicio = date.today()
    fim = inicio + timedelta(days=30)
    previsao = ServicoDiario.objects.filter(data__range=[inicio, fim]).order_by('data', 'tipo_escala')
    return render(request, 'core/visualizar_previsao.html', {'previsao': previsao})
