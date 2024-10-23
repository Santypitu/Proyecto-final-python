from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Mensaje, Profile

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico", help_text="Ingrese una direccion de correo electronico valida")
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="Tu contraseña debe tener al menos 8 caracteres y no puede ser completamente numérica."
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        help_text="Introduce de nuevo la misma contraseña para verificar."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
        }
        help_texts = {
            'username': 'Ingrese su nombre de usuario',
            'email': 'Ingrese una direccion de correo electronico valida'
        }
        error_messages = {
            'username': {
                'required': 'Por favor, introduce un nombre de usuario.',
            },
            'email': {
                'required': 'El correo electrónico es obligatorio.',
                'invalid': 'Por favor, introduce una dirección de correo válida.',
            },
        }

class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=254)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class MensajeForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(queryset=User.objects.all(), label="Destinatario")

    class Meta:
        model = Mensaje
        fields = ['destinatario', 'contenido']
        labels = {
            'contenido': 'Mensaje'
        }

class PerfilUsuarioForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email'] 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto_perfil'] 