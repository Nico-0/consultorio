from django.apps import AppConfig
from django.db import connection
from django.core.management import call_command
from .backup import initBackup, get_set_drive_folder
from django.conf import settings
import os

class HistoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'historia'

    def ready(self):
        print("--------------------------------------------------------------------------------------------")
        migrate_if_empty()
        os.makedirs(settings.BACKUP_LOCATION, exist_ok=True)
        os.makedirs(settings.RESTORED_TRASH_PATH, exist_ok=True)
        import historia.signals
        get_set_drive_folder()
        initBackup()
    
def migrate_if_empty(): #TODO RuntimeWarning: Accessing the database during app initialization is discouraged.
    if not connection.introspection.table_names():
        call_command('migrate')
        call_command('createsuperuser')

def flavor(request):
    return {'APP_FLAVOR': settings.APP_FLAVOR}