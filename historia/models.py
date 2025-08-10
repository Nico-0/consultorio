from django.db import models
from django.utils import timezone

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nacimiento = models.DateField(default=timezone.now)
    dni = models.CharField(max_length=10, blank=True, null=True, unique=True)
    obraSocial = models.CharField(max_length=50, blank=True, default="")
    obraSocial2 = models.CharField(max_length=50, blank=True, default="")
    afiliado = models.CharField(max_length=50, blank=True, default="")
    afiliado2 = models.CharField(max_length=50, blank=True, default="")
    telefono = models.CharField(max_length=30, blank=True, default="")
    localidad = models.CharField(max_length=50, blank=True, default="")
    email = models.CharField(max_length=50, blank=True, default="") #EmailField tiene validaciones incompletas
    extras = models.CharField(max_length=50, blank=True, default="")
    comentarios = models.TextField(blank=True, default="")
    modificado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " " + self.apellido

    class Meta:
        ordering = ['-modificado']

class Entrada(models.Model):
    paciente = models.ForeignKey(Persona, on_delete=models.RESTRICT)
    fecha = models.DateField(default=timezone.now)
    comentarios = models.TextField(blank=True, default="")

    def __str__(self):
        return "Entrada " + str(self.fecha)

    class Meta:
        ordering = ['-fecha']

def directorio(instance, filename):
    # MEDIA_ROOT/paciente_<id>/<filename>
    return 'paciente_{0}/{1}'.format(instance.entrada.paciente.id, filename)

class Imagen(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to=directorio, null = True)