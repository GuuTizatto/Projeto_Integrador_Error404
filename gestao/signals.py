# em gestao/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil, HistoricoExecucao
from datetime import date, timedelta

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=HistoricoExecucao)
def premiar_usuario_por_tarefa(sender, instance, created, **kwargs):
    if created:
        perfil = instance.tarefa.comodo.usuario.perfil

        # 1. Adicionar pontos
        perfil.pontos += 10

        # 2. Lógica para subir de nível (a cada 100 pontos)
        if perfil.pontos >= perfil.nivel * 100:
            perfil.nivel += 1

        # 3. Lógica da Sequência (Streak)
        hoje = date.today()
        ontem = hoje - timedelta(days=1)

        if perfil.data_ultima_atividade == ontem:
            perfil.streak_atual += 1
        elif perfil.data_ultima_atividade != hoje:
            perfil.streak_atual = 1

        perfil.data_ultima_atividade = hoje
        perfil.save()