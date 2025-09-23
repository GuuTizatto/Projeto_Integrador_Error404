# em gestao/urls.py

from django.urls import path
# ESTA LINHA ESTAVA FALTANDO 👇
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Nossas URLs existentes
    path('painel/', views.painel_usuario, name='painel_usuario'),
    path('tarefa/<int:tarefa_id>/concluir/', views.concluir_tarefa, name='concluir_tarefa'),

    # URLS DE CADASTRO E LOGIN
    path('cadastro/', views.pagina_cadastro, name='cadastro'),
    
    # Agora o 'auth_views' é reconhecido pelo Python
    path('login/', auth_views.LoginView.as_view(
        template_name='gestao/login.html'
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ), name='logout'),
]