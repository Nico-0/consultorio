from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),  # pagina de prueba
    path('about/', views.about, name='about'),  # pagina de prueba 2
    path('', views.consultorio, name='consultorio'),    # listado
    path('perfil/<int:persona_id>', views.perfil, name='perfil'),   # paciente individual
    path('perfil/<int:persona_id>/comentarios', views.comentarios, name='comentarios'),
    path('perfil/<int:persona_id>/entrada', views.entrada, name='entrada'),
]