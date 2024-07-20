import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escala_servico.settings')
django.setup()

from core.models import Militar

militares = [
    {'nome': '2º Ten Diniz', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '1º Ten Nogueira Machado', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '1º Ten Matheus Borges', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '1º Ten Miquéias', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '1º Ten Trindade', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '1º Ten Roduit', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '2º Ten Nunes', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '1º Ten Felipe', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': '2º Ten Lando', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': 'Asp Estevam', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': 'Asp Borges', 'tipo': 'OFICIAL_DIA', 'ativo': True},
    {'nome': 'Asp Silva Alves', 'tipo': 'OFICIAL_DIA', 'ativo': True},
]

for militar_data in militares:
    Militar.objects.create(**militar_data)

print("Banco de dados populado com sucesso!")
