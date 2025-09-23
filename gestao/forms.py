from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {
            "username": "Nome de Usuário",
        }
        help_texts = {
            "username": "",   # remove o texto padrão
        }