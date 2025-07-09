from django import forms
from historia.models import Persona


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'dni']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'nacimiento', 'dni', 'obraSocial', 'afiliado', 'telefono', 'localidad', ]
        widgets = {'nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

