# gestao/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q, Sum 
from .models import Comodo, Tarefa, HistoricoExecucao 
from .forms import CustomUserCreationForm 
import datetime 

# --- VIEW DE CADASTRO PADRÃO ---
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

# --- VIEW DO PAINEL PRINCIPAL (Original) ---
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

# --- VIEW DE REGISTRO CUSTOMIZADO ---
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


# --- VIEW DE DASHBOARD (Implementação Dinâmica FINAL e Corrigida) ---
@login_required 
def dashboard_view(request):
    user = request.user
    
    # 1. Métricas Chave (Tarefas)
    tarefas_do_usuario = Tarefa.objects.filter(comodo__usuario=user)
    
    # Contagem total de execuções
    completed_activities = HistoricoExecucao.objects.filter(
        tarefa__comodo__usuario=user
    ).count()

    # CORREÇÃO DE FIELDERROR: Usando o campo 'ativa' para contar pendentes
    # (Assumindo que ativa=True significa que a tarefa precisa ser feita)
    pending_activities = tarefas_do_usuario.filter(ativa=True).count()
    
    # Métrica Horas Utilizando o Sistema (Estimativa)
    executions_count = completed_activities
    total_hours = round(executions_count * 0.25, 1)

    # 3. Dados para o Gráfico (Últimos 7 Dias)
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=6)
    
    # CORREÇÃO DE FIELDERROR: Usando 'data_conclusao' em vez de 'data_execucao'
    activities_by_day = HistoricoExecucao.objects.filter(
        tarefa__comodo__usuario=user,
        data_conclusao__date__gte=start_date # <--- Corrigido
    ).extra({'data_dia': "date(data_conclusao)"}).values('data_dia').annotate( # <--- Corrigido
        count=Count('id')
    ).order_by('data_dia')

    # Prepara os labels (datas) e os dados (contagem)
    date_range = [start_date + datetime.timedelta(days=i) for i in range(7)]
    chart_data_map = {date.strftime('%Y-%m-%d'): 0 for date in date_range}
    
    for item in activities_by_day:
        date_str = item['data_dia'].strftime('%Y-%m-%d')
        chart_data_map[date_str] = item['count']
        
    chart_labels = [date.strftime('%d/%m') for date in date_range] 
    chart_data = list(chart_data_map.values())

    context = {
        'total_hours': total_hours,
        'completed_activities': completed_activities,
        'pending_activities': pending_activities,
        
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        
        'username': user.username,
        'perfil': getattr(user, 'perfil', None),
    }
    # ATENÇÃO: Verifique se o nome do seu template é 'gestao/dashboard.html' ou 'gestao/dashboard/index.html'
    # Vamos manter 'gestao/dashboard/index.html' como padrão, mas verifique se o caminho está correto.
    return render(request, 'gestao/dashboard.html', context)