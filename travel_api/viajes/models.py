from django.db import models
from django.contrib.auth.models import User

class Viaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)

class Destino(models.Model):
    viaje = models.ForeignKey(Viaje, related_name='destinos', on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

class Itinerario(models.Model):
    destino = models.ForeignKey(Destino, related_name='itinerarios', on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()

class Actividad(models.Model):
    itinerario = models.ForeignKey(Itinerario, related_name='actividades', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    hora = models.TimeField()
    costo = models.DecimalField(max_digits=8, decimal_places=2)
