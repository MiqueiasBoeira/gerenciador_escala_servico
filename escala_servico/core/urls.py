
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gerar-previsao/', views.gerar_previsao_servico, name='gerar_previsao_servico'),
    # Adicione mais rotas conforme necessário
]
