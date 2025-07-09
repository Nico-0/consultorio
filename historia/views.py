
"""
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")
"""
from django.shortcuts import render
from historia.models import Persona
from historia.forms import PersonaForm, PacienteForm
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import JsonResponse
import json

def about(request):
    context = {}
    context['title'] = 'About'
    return render(request, 'about.html', context)

def consultorio(request):
    context = {}
    context['title'] = 'Consultorio'
    context['css'] = 'consultorio.css'
    context['js'] = 'consultorio.js'
    context['active'] = True
    context['personas'] = Persona.objects.all()
    context['form'] = PacienteForm()
    if request.method == 'POST':
        if 'cargar' in request.POST:
            form = PacienteForm(request.POST)
            # if form.is_valid()
            # persona = form.save(commit=False)
            # persona.save()
            form.save()
    return render(request, 'consultorio.html', context)

def perfil(request, persona_id):
    context = {}
    context['title'] = 'Perfil'
    context['css'] = 'perfil.css'
    context['js'] = 'perfil.js'
    persona = get_object_or_404(Persona, id=persona_id)
    context['persona'] = persona
    entradas = persona.entrada_set.all()
    context['entradas'] = entradas
    diaHoy = timezone.localdate()
    context['edadHoy'] = relativedelta(diaHoy, persona.nacimiento).years
    context['diaHoy'] = diaHoy
    if(entradas): 
        if((entradas[0]).fecha == diaHoy):
            context['entradaHoy'] = entradas[0].comentarios

    form = PacienteForm(instance=persona)
    context['form'] = form
    if request.method == 'POST':
        if 'cargar' in request.POST:
            form = PacienteForm(request.POST, instance=persona)
            form.save()
    return render(request, 'perfil.html', context)

def comentarios(request, persona_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_value = data.get('value')

        try:
            paciente = Persona.objects.get(id=persona_id)
            paciente.comentarios = new_value
            paciente.save()
            return JsonResponse({'status': 'success'})
        except Persona.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=404)

    return JsonResponse({'error': 'invalid method'}, status=405)

def entrada(request, persona_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_value = data.get('value')
        diaHoy = timezone.localdate()
        persona = Persona.objects.get(id=persona_id)

        from historia.models import Entrada
        try:
            entrada, created = Entrada.objects.get_or_create(paciente=persona, fecha=diaHoy, defaults={"comentarios": ""})
            entrada.comentarios = new_value
            entrada.save()
            return JsonResponse({'status': 'success'})
        except Persona.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=404)

    return JsonResponse({'error': 'invalid method'}, status=405)

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