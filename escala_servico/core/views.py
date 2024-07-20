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

    # Verificar se já existem entradas para os dias no intervalo
    dias = (fim - inicio).days + 1
    dias_existentes = ServicoDiario.objects.filter(data__range=[inicio, fim]).values_list('data', flat=True)
    dias_duplicados = set(dias_existentes)

    if dias_duplicados:
        mensagem = "Alguns dias já possuem escala gerada. Por favor, clique em atualizar escala de serviço."
        return render(request, 'core/gerar_previsao.html', {'mensagem': mensagem})

    # Lógica para gerar a previsão de serviço
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

    mensagem = "Previsão de serviço para os próximos 30 dias gerada com sucesso."
    return render(request, 'core/gerar_previsao.html', {'mensagem': mensagem})


def visualizar_previsao(request):
    inicio = date.today()
    fim = inicio + timedelta(days=30)
    previsao = ServicoDiario.objects.filter(data__range=[inicio, fim]).order_by('data', 'tipo_escala')
    return render(request, 'core/visualizar_previsao.html', {'previsao': previsao})


def atualizar_previsao_servico(request):
    inicio = date.today()
    fim = inicio + timedelta(days=30)

    # Lógica para atualizar a previsão de serviço
    dias = (fim - inicio).days + 1
    for dia in range(dias):
        data_servico = inicio + timedelta(days=dia)
        # Verificar se o dia já existe na tabela e se é um dia futuro
        if not ServicoDiario.objects.filter(data=data_servico).exists() and data_servico >= inicio:
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

    mensagem = "Previsão de serviço para os próximos 30 dias atualizada com sucesso."
    return render(request, 'core/gerar_previsao.html', {'mensagem': mensagem})
