from django import forms
from historia.models import Persona, Imagen


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'dni']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellido', 'nombre', 'nacimiento', 'dni', 'obraSocial', 'afiliado', 'email']
        widgets = {'nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
        
class PacienteFullForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellido', 'nombre', 'nacimiento', 'dni', 'obraSocial', 'afiliado', 'obraSocial2', 'afiliado2', 'email', 'telefono', 'localidad', 'extras']
        widgets = {'nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}

class ImagenUploadForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Imagen
        fields = ['imagen', 'fecha']