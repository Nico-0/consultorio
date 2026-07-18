from django.apps import AppConfig
from django.db import connection
from django.db.backends.signals import connection_created
from django.core.management import call_command
from .backup import initBackup, initNoBackup
from django.conf import settings
import os, sys

class HistoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'historia'

    def ready(self):
        print("--------------------------------------------------------------------------------------------")
        if 'runserver' in sys.argv:
            #connection_created.connect(migrate_if_empty)   # blocks the program and the console can not be seen from electron
            if os.environ.get('RUN_MAIN') != 'true':
                print("Executes only on first run (and not on auto-reload)")
                os.makedirs(settings.BACKUP_LOCATION, exist_ok=True)
                os.makedirs(settings.RESTORED_TRASH_PATH, exist_ok=True)
                initBackup()
            else: initNoBackup()
    
def migrate_if_empty(sender, connection, **kwargs):
    if not connection.introspection.table_names():
        call_command('migrate')
        call_command('createsuperuser')#, interactive=False)

def flavor(request):
    return {'APP_FLAVOR': settings.APP_FLAVOR}