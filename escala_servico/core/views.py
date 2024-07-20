from django.shortcuts import render
from .models import Militar, Escala
from .utils import gerar_previsao_escala

def home(request):
    militares = Militar.objects.all()
    escalas = Escala.objects.all()
    previsao = gerar_previsao_escala()

    context = {
        'militares': militares,
        'escalas': escalas,
        'previsao': previsao,
        'militar_mais_folgado_preta': sorted(militares, key=lambda m: (m.folgas.filter(tipo='preta').count(), m.nome))[0],
        'militar_mais_folgado_vermelha': sorted(militares, key=lambda m: (m.folgas.filter(tipo='vermelha').count(), m.nome))[0],
    }
    return render(request, 'home.html', context)
