from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gerar-previsao/', views.gerar_previsao_servico, name='gerar_previsao_servico'),
    path('visualizar-previsao/', views.visualizar_previsao, name='visualizar_previsao'),
    # Adicione mais rotas conforme necessário
]
