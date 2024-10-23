from django.db import models
from django.contrib.auth.models import User

class Peluche(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='peluches/')

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Peluche, through='ItemCarrito')

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    peluche = models.ForeignKey(Peluche, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

class Mensaje(models.Model):
    remitente = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_enviado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.remitente} a {self.destinatario} - {self.fecha_enviado}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username