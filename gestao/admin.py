# em gestao/admin.py

from django.contrib import admin
from .models import Perfil, Conquista, Comodo, Tarefa, HistoricoExecucao

admin.site.register(Perfil)
admin.site.register(Conquista)
admin.site.register(Comodo)
admin.site.register(Tarefa)
admin.site.register(HistoricoExecucao)