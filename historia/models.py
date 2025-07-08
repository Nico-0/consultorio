from django.db import models
from django.utils import timezone

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, blank=True, default="")
    edad = models.PositiveSmallIntegerField()
    nacimiento = models.DateField(default=timezone.now)
    dni = models.CharField(max_length=10, blank=True, default="")
    obraSocial = models.CharField(max_length=50, blank=True, default="")
    afiliado = models.CharField(max_length=50, blank=True, default="")
    telefono = models.CharField(max_length=30, blank=True, default="")
    localidad = models.CharField(max_length=50, blank=True, default="")
    comentarios = models.TextField(blank=True, default="")
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre + " " + self.apellido

    class Meta:
        ordering = ['-modificado']

class Entrada(models.Model):
    paciente = models.ForeignKey(Persona, on_delete=models.RESTRICT)
    fecha = models.DateField(default=timezone.now)
    comentarios = models.TextField(blank=True, default="")

    def __str__(self):
        return "Entrada " + self.fecha

    class Meta:
        ordering = ['-fecha']