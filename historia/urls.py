from django.urls import path
from . import views


urlpatterns = [
    # path('index/', views.index, name='index'),  # pagina de prueba
    path('about/', views.about, name='about'),
    path('', views.consultorio, name='consultorio'),    # listado
    path('perfil/<int:persona_id>', views.perfil, name='perfil'),   # paciente individual
    path('backups/', views.backups, name='backups'),
    path('drivelogin/', views.drivelogin, name='drivelogin'),
    path('perfil/<int:persona_id>/comentarios', views.comentarios, name='comentarios'),
    path('perfil/<int:persona_id>/entrada', views.entrada, name='entrada'),
    path('perfil/<int:persona_id>/activo', views.activo, name='activo'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, 
                    document_root=settings.MEDIA_ROOT)