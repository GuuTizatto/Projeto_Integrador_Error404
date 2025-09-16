# em gestao/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .models import Comodo, Tarefa, HistoricoExecucao

# --- VIEW DE CADASTRO ---
def pagina_cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'gestao/cadastro.html', context)

# --- VIEW DO PAINEL PRINCIPAL ---
@login_required
def painel_usuario(request):
    comodos = Comodo.objects.filter(usuario=request.user)

    context = {
        'comodos': comodos,
        'perfil': request.user.perfil
    }
    return render(request, 'gestao/painel.html', context)

# --- VIEW PARA CONCLUIR TAREFA ---
@login_required
def concluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, comodo__usuario=request.user)

    if request.method == 'POST':
        HistoricoExecucao.objects.create(tarefa=tarefa)

        tarefa.data_ultima_execucao = timezone.now()
        tarefa.save()

    return redirect('painel_usuario')# em gestao/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .models import Comodo, Tarefa, HistoricoExecucao

# --- VIEW DE CADASTRO ---
def pagina_cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'gestao/cadastro.html', context)

# --- VIEW DO PAINEL PRINCIPAL ---
@login_required
def painel_usuario(request):
    comodos = Comodo.objects.filter(usuario=request.user)

    context = {
        'comodos': comodos,
        'perfil': request.user.perfil
    }
    return render(request, 'gestao/painel.html', context)

# --- VIEW PARA CONCLUIR TAREFA ---
@login_required
def concluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, comodo__usuario=request.user)

    if request.method == 'POST':
        HistoricoExecucao.objects.create(tarefa=tarefa)

        tarefa.data_ultima_execucao = timezone.now()
        tarefa.save()

    return redirect('painel_usuario')