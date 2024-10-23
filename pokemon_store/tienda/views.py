from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import RegistroForm, AuthenticationForm, MensajeForm, PerfilUsuarioForm, ProfileForm
from .models import Peluche, Carrito, ItemCarrito, Mensaje, Profile

def index(request):
    peluches = Peluche.objects.all()
    return render(request, 'tienda/index.html', {'peluches': peluches})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Carrito.objects.create(usuario=user)
            login(request, user)
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'tienda/register.html', {'form': form})

@login_required
def carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.itemcarrito_set.all()
    total_precio = 0
    items_totales = []
    total_cantidad = 0 
    for item in items:
        total_por_item = item.cantidad * item.peluche.precio
        items_totales.append({
            'item': item,
            'total_por_item': total_por_item
        })
        total_precio += total_por_item
        total_cantidad += item.cantidad 
    return render(request, 'tienda/carrito.html', {'items_totales': items_totales, 'total_precio': total_precio, 'total_cantidad': total_cantidad})

@login_required
def agregar_al_carrito(request, peluche_id):
    peluche = get_object_or_404(Peluche, id=peluche_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, peluche=peluche)
    if not created:
        item.cantidad += 1
    item.save()

    return redirect('index')

@login_required
def quitar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect('carrito')

def sobre_mi(request):
    return render(request, 'tienda/sobre_mi.html')

class CustomLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'login.html'

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            return redirect('ver_mensajes')
    else:
        form = MensajeForm()
    return render(request, 'tienda/enviar_mensaje.html', {'form': form})

@login_required
def ver_mensajes(request):
    mensajes_recibidos = Mensaje.objects.filter(destinatario=request.user).order_by('-fecha_enviado')
    return render(request, 'tienda/ver_mensajes.html', {'mensajes': mensajes_recibidos})

@login_required
def perfil_usuario(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = PerfilUsuarioForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario de contraseña.')

    else:
        user_form = PerfilUsuarioForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'tienda/perfil.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })