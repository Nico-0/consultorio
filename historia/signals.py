from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entrada

@receiver(post_save, sender=Entrada)
def update_persona_timestamp(sender, instance, **kwargs):
    persona = instance.paciente
    persona.save(update_fields=['modificado'])