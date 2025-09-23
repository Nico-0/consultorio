from django import forms
from historia.models import Persona, Imagen, Archivo


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'dni']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellido', 'nombre', 'nacimiento', 'dni', 'sexo', 'obraSocial', 'afiliado', 'email']
        widgets = {'nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
        
class PacienteFullForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellido', 'nombre', 'nacimiento', 'dni', 'sexo', 'obraSocial', 'afiliado', 'obraSocial2', 'afiliado2',
                   'email', 'telefono', 'localidad', 'sangre', 'peso', 'altura', 'ocupacion', 'extras']
        widgets = {'nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
                   'peso': forms.NumberInput(attrs={'min': 0, 'max': '999'}),
                   'altura': forms.NumberInput(attrs={'min': 0, 'max': '9'}) # 'class': 'form-control'
                   }

class ImagenUploadForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Imagen
        fields = ['archivo', 'fecha']

class ArchivoUploadForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Archivo
        fields = ['archivo', 'fecha']