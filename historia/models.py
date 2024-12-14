from django.db import models


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-edad']