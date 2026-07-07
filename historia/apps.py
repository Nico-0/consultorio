from django.apps import AppConfig
import os
from django.conf import settings

class HistoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'historia'

    def ready(self):
        print("--------------------------------------------------------------------------------------------")
        os.makedirs(settings.BACKUP_LOCATION, exist_ok=True)
        os.makedirs(settings.RESTORED_TRASH_PATH, exist_ok=True)
        import historia.signals
        from .backup import initBackup, get_set_drive_folder
        get_set_drive_folder()
        initBackup()


def flavor(request):
    return {'APP_FLAVOR': settings.APP_FLAVOR}