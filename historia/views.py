
"""
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")
"""
from django.shortcuts import render
from historia.models import Persona
from historia.forms import PersonaForm, PacienteForm, PacienteFullForm
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
import json
import os
import requests

def about(request):
    import subprocess
    import socket
    context = {}
    context['title'] = 'About'
    context['css'] = 'consultorio.css'
    context['activeC'] = True
    context['ip'] = socket.gethostbyname(socket.gethostname()) + ':8000'
    
    """ Opcion no usada, pero seria util en caso de a futuro no querer usar la api y comparar todo local
    gitcmderror = subprocess.run(['git', 'fetch'], capture_output=True, text=True, shell=True).returncode
    gitstatus = subprocess.run(['git', 'status'], capture_output=True, text=True, shell=True).stdout.splitlines()[1]
    if(gitstatus.startswith('Your branch is behind')):
        # Hay nueva version disponible
        context['botonUpdate'] = True # activar boton de update y su descripcion
    else:
        # Para Para 'Your branch is up to date' o cualquier error
        # Falta considerar 'HEAD detached at' (checkout de commit anterior)
        context['botonUpdate'] = False
    """
    
    context['botonUpdate'] = False
    gitcmd = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True, shell=True)
    if(gitcmd.returncode):
        context['version'] = context['botonText'] = 'Git no instalado'
    else:
        commitActual = gitcmd.stdout.strip()
        context['version'] = commitActual
        try: # fetch github commits api
            response = requests.get("https://api.github.com/repos/Nico-0/consultorio/commits")
            response.raise_for_status()
            data = response.json()
            ultimoCommit = data[0]['sha'][:7]
            if(commitActual == ultimoCommit):
                context['botonText'] = 'Última versión instalada'
            else:
                context['botonUpdate'] = True
                context['botonText'] = 'Actualizar a la última versión'
            commits = []
            for commit in data:
                commits.append({'fecha': commit['commit']['committer']['date'][:10], 'hash': commit['sha'][:7]})
            context['commits'] = commits

        except requests.exceptions.RequestException as e:
            context['error'] = f"Error de conexion: reinicie la pagina"#: {e}"
            context['botonText'] = 'Error de conexión'
    
    if request.method == 'POST': # todo ponerlo en una url mas descriptiva
        # actualizar programa
        if 'pull' in request.POST:
            subprocess.run(['git', 'pull'])
            subprocess.run(['python', 'manage.py', 'migrate'])
    
    return render(request, 'about.html', context)

def backups(request):
    context = {}
    context['title'] = 'Backups'
    context['css'] = 'consultorio.css'
    context['activeB'] = True
    from .backup import get_last_backup_time, hacerBackup
    from django.conf import settings
    context['backups'] = "\n".join(os.listdir('./backups')[::-1])
    context['lastBackup'] = get_last_backup_time()
    context['carpeta'] = settings.DRIVE_FOLDER_ID
    if request.method == 'POST':
        if 'generar' in request.POST:
            hacerBackup()
    return render(request, 'backups.html', context)

def consultorio(request):
    context = {}
    context['title'] = 'Consultorio'
    context['css'] = 'consultorio.css'
    context['js'] = 'consultorio.js'
    context['active'] = True
    context['personas'] = Persona.objects.filter(activo=True)
    context['form'] = PacienteForm()
    if request.method == 'POST':
        if 'cargar' in request.POST:
            form = PacienteForm(request.POST)
            # if form.is_valid()
            # persona = form.save(commit=False)
            # persona.save()
            if not form.is_valid():
                redirect = validar_form_dni(request, form)
                if redirect: return redirect
                #new_form = validar_form_email(request, form)
                #if new_form.data: form = new_form
            form.save()
    return render(request, 'consultorio.html', context)

def validar_form_dni(request, form):
    if 'dni' in form.errors: # captura solo error de dni
        # encontrar usuario existente y redireccionar
        input_dni = form.data.get('dni')
        persona_existente = get_object_or_404(Persona, dni=input_dni)
        messages.warning(request, 'Paciente existente encontrado con DNI: '+input_dni)
        return redirect('/perfil/'+str(persona_existente.id))
    print(form.errors)

def validar_form_email(request, form): #validacion en caso de cambiar email a models.EmailField
    if 'email' in form.errors: # parece que del frontend no valida que se incluya .com
        mutable_post = request.POST.copy()
        email = mutable_post.get('email', '')
        email += '.com'
        mutable_post['email'] = email
        return PersonaForm(mutable_post) #crea correctamente el objeto, pero el form.save() no guarda ni email ni apellido ¿?

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
            context['entradaHoy'] = entradas[0].comentarios # toma la ultima porque el modelo tiene ordering '-fecha'

    form = PacienteFullForm(instance=persona)
    context['form'] = form
    if request.method == 'POST':
        if 'cargar' in request.POST:
            form = PacienteFullForm(request.POST, instance=persona)
            if not form.is_valid():
                redirect = validar_form_dni(request, form)
                if redirect: return redirect
            print(form.errors)
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

def entrada(request, persona_id): # solo se puede modificar la entrada de hoy
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

def activo(request, persona_id):
    if request.method == 'POST':
        try:
            paciente = Persona.objects.get(id=persona_id)
            paciente.activo = not paciente.activo
            paciente.save()
        except Persona.DoesNotExist:
            return JsonResponse({'status': 'persona not found'}, status=404)
    return redirect('/perfil/'+str(persona_id))

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