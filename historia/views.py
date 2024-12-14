
"""
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")
"""
from django.shortcuts import render

def about(request):
    context = {}
    context['title'] = 'About'
    return render(request, 'about.html', context)

from historia.models import Persona
from historia.forms import PersonaForm

def index(request):
    context = {}
    form = PersonaForm()
    personas = Persona.objects.all()
    context['personas'] = personas
    context['title'] = 'Home'
    context['form'] = form
    # logica adicional si se entra a index con post
    if request.method == 'POST':
        if 'cargar' in request.POST:  # la request trae el name del boton presionado
            form = PersonaForm(request.POST)
            form.save()
        elif 'borrar' in request.POST:
            pk = request.POST.get('borrar') # obtener el value del boton
            persona = Persona.objects.get(id=pk)
            persona.delete()
    return render(request, 'index.html', context)