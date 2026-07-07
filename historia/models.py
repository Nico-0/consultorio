from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
import os
from django.conf import settings
from send2trash import send2trash

class Persona(models.Model):
    GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    GRUPOS = [
        ('A+', 'A Positivo'), ('A-', 'A Negativo'),
        ('B+', 'B Positivo'), ('B-', 'B Negativo'),
        ('AB+', 'AB Positivo'), ('AB-', 'AB Negativo'),
        ('O+', 'O Positivo'), ('O-', 'O Negativo'),
    ]
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
    sexo = models.CharField(max_length=1, choices=GENEROS, blank=True, default="")
    sangre = models.CharField(max_length=3, choices=GRUPOS, blank=True, default="")
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0) # 109.99 kg
    altura = models.DecimalField(max_digits=3, decimal_places=2, blank=True, default=0) # 2.00 m
    ocupacion = models.CharField(max_length=50, blank=True, default="")
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

    motivo_consulta = models.TextField(blank=True)
    medicamentos = models.TextField(blank=True)
    antec_medicos = models.TextField(blank=True)
    antec_oculares = models.TextField(blank=True)
    obs_segmento = models.TextField(blank=True)
    obs_generales = models.TextField(blank=True)

    cc_uso = models.JSONField(default=dict, blank=True)
    akr = models.JSONField(default=dict, blank=True)
    queratometria = models.JSONField(default=dict, blank=True)
    av_sc = models.JSONField(default=dict, blank=True)
    av_cc = models.JSONField(default=dict, blank=True)
    retinoscopia = models.JSONField(default=dict, blank=True)
    subjetivo = models.JSONField(default=dict, blank=True)
    add = models.JSONField(default=dict, blank=True)
    formula = models.JSONField(default=dict, blank=True)


    def __str__(self):
        return "Entrada " + str(self.fecha)

    class Meta:
        ordering = ['-fecha']

def directorio(instance, filename):
    # MEDIA_ROOT/paciente_<id>/<filename>
    return 'paciente_{0}/{1}'.format(instance.entrada.paciente.id, filename)

class Imagen(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='imagenes')
    archivo = models.ImageField(upload_to=directorio, null = True)

    @property
    def filename(self):
        return os.path.basename(self.archivo.name)

class Archivo(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to=directorio, null = True)

    @property
    def filename(self):
        return os.path.basename(self.archivo.name)

@receiver(post_delete, sender=Imagen)
@receiver(post_delete, sender=Archivo)
def delete_file(sender, instance, **kwargs):
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            new_path = os.path.join(settings.RESTORED_TRASH_PATH, os.path.basename(instance.archivo.path))
            os.rename(instance.archivo.path, new_path)  # delete file from trashed folder, keeps media folder clean when restoring file from trash bin 
            send2trash(new_path)