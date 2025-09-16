# em gestao/models.py

from django.db import models
from django.contrib.auth.models import User

# --- MODELOS DE GAMIFICAÇÃO ---

class Conquista(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título da Conquista")
    descricao = models.TextField(verbose_name="Descrição")
    icone = models.CharField(max_length=100, help_text="Ex: 'fa-trophy'", verbose_name="Ícone")

    def __str__(self):
        return self.titulo

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    pontos = models.IntegerField(default=0, verbose_name="Pontos de Experiência")
    nivel = models.IntegerField(default=1, verbose_name="Nível")
    conquistas = models.ManyToManyField(Conquista, blank=True)
    streak_atual = models.IntegerField(default=0, verbose_name="Sequência Atual (dias)")
    data_ultima_atividade = models.DateField(null=True, blank=True, verbose_name="Data da Última Atividade")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

# --- MODELOS PRINCIPAIS DA APLICAÇÃO ---

class Comodo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comodos')
    nome = models.CharField(max_length=100, verbose_name="Nome do Cômodo")
    icone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ícone")

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    comodo = models.ForeignKey(Comodo, on_delete=models.PROTECT, related_name='tarefas')
    titulo = models.CharField(max_length=200, verbose_name="Título da Tarefa")
    frequencia = models.CharField(max_length=100, verbose_name="Quando Fazer / Frequência")
    data_ultima_execucao = models.DateTimeField(null=True, blank=True, verbose_name="Última Execução")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")

    def __str__(self):
        return f"{self.titulo} ({self.comodo.nome})"

class HistoricoExecucao(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.PROTECT, related_name='historico')
    data_conclusao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Conclusão")

    def __str__(self):
        return f"Tarefa '{self.tarefa.titulo}' concluída em {self.data_conclusao.strftime('%d/%m/%Y')}"