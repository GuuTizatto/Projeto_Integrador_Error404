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

    # ATUALIZAÇÃO: Redireciona de volta para a página de detalhes do cômodo
    return redirect('detalhe_comodo', comodo_id=tarefa.comodo.id)

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

    # ATUALIZAÇÃO: Redireciona de volta para a página de detalhes do cômodo
    return redirect('detalhe_comodo', comodo_id=tarefa.comodo.id)

@login_required
def detalhe_comodo(request, comodo_id):
    # Busca o cômodo específico, garantindo que ele pertence ao usuário logado
    comodo_selecionado = get_object_or_404(Comodo, id=comodo_id, usuario=request.user)

    # Busca todos os outros cômodos para exibir na barra lateral
    todos_os_comodos = Comodo.objects.filter(usuario=request.user)

    context = {
        'comodo': comodo_selecionado,
        'comodos_sidebar': todos_os_comodos,
    }
    return render(request, 'gestao/detalhe_comodo.html', context)

@login_required
def deletar_tarefa(request, tarefa_id):
    # Busca a tarefa, garantindo que pertence ao usuário logado
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, comodo__usuario=request.user)
    comodo_id = tarefa.comodo.id # Guarda o ID do comodo antes de deletar

    if request.method == 'POST':
        tarefa.delete()

    return redirect('detalhe_comodo', comodo_id=comodo_id)