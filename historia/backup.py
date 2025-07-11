#pip install google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from django.conf import settings

import os, sys
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from dateutil.relativedelta import relativedelta
import shutil

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
filename = "db.sqlite3"
BACKUP_TIMESTAMP = './last_backup.txt'

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : get_nameTime(),
        'parents' : [settings.DRIVE_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata, # nombre y carpeta
        media_body=filename # archivo a subir
    ).execute()

def get_nameTime():
    return timezone.now().strftime("%Y-%m-%d %H:%M:%S ").replace(":", ".")+filename

def get_last_backup_time():
    try:
        with open(BACKUP_TIMESTAMP, 'r') as f:
            return parse_datetime(f.read().strip())
    except FileNotFoundError:
        return None
    except Exception as e:
        print("⚠️🚨 Error reading backup time:", e)
        return None

def rutinaBackup():
    last_backup = get_last_backup_time()
    delta = relativedelta(timezone.now().replace(tzinfo=None), last_backup).days
    print("\nUltimo backup: ", last_backup, file=sys.stderr)
    if(delta > 6 or last_backup is None):
        hacerBackup()
    else:
        print("Dias desde el ultimo backup: ", delta, "\n", file=sys.stderr)

def hacerBackup():
    backupCompleto = True

    try:
        os.makedirs('./backups/', exist_ok=True)
        result = shutil.copy(filename, './backups/'+get_nameTime())
        print("Nuevo backup local: ", result, file=sys.stderr)
    except FileNotFoundError:
        backupCompleto = False
    
    # online
    try:
        upload_file()
    except FileNotFoundError:
        backupCompleto = False
        print("Falta la service account key", file=sys.stderr)
    except HttpError as err:
        backupCompleto = False
        #print(err.resp, file=sys.stderr)
        print(err.content, file=sys.stderr)


    # si se completaron backup local + online, registrar como backup realizado
    # falta considerar, si falla uno que no se haga el otro siempre
    if(backupCompleto):
        with open(BACKUP_TIMESTAMP, 'w') as f:
            f.write(str(timezone.now().strftime("%Y-%m-%d %H:%M:%S")))
        print("Backup completo\n", file=sys.stderr)
    else:
        print("Error de backup\n", file=sys.stderr)
    






