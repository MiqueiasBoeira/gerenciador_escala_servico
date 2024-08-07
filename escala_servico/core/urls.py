# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gerar-previsao/', views.gerar_previsao_servico_view, name='gerar_previsao_servico'),
    path('visualizar-previsao/', views.visualizar_previsao, name='visualizar_previsao'),
    path('atualizar-previsao/', views.atualizar_previsao_servico, name='atualizar_previsao_servico'),
]
