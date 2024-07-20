from django.contrib import admin
from .models import Militar, Escala

@admin.register(Militar)
class MilitarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'posto', 'data_entrada', 'suspenso_ate')
    list_filter = ('posto', 'suspenso_ate')

@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = ('data', 'tipo', 'militar', 'funcao')
    list_filter = ('tipo', 'funcao')
