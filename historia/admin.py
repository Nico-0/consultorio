from django.contrib import admin
from .models import Persona, Entrada, Imagen, Archivo

admin.site.site_title = "Admin consultorio"
admin.site.site_header = "Administración de Consultorio"
admin.site.index_title = "Monitos días"

admin.site.register(Persona)
admin.site.register(Entrada)
admin.site.register(Imagen)
admin.site.register(Archivo)
