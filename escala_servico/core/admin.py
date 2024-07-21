from django.contrib import admin
from .models import Militar, ServicoDiario, DiaNaoUtil, FolgaDiaria

# Registrar os modelos para que apareçam na interface de administração
admin.site.register(Militar)
admin.site.register(ServicoDiario)
admin.site.register(DiaNaoUtil)
admin.site.register(FolgaDiaria)

