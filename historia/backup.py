#pip install google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

#pip install pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.conf import settings

import os, sys
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from dateutil.relativedelta import relativedelta
import shutil

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
filename = "db.sqlite3"
mimeType = 'application/x-7z-compressed'
BACKUP_TIMESTAMP = './last_backup.txt'

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file_service_account():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : get_nameTime(),
        'parents' : [settings.DRIVE_FOLDER_ID],
        'mimeType': mimeType
    }
    
    media_body = MediaFileUpload(filename, mimetype=mimeType)
    file = service.files().create(
        body=file_metadata, # nombre y carpeta
        media_body=media_body # archivo a subir
    ).execute()

def upload_file(filepath):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_metadata = {
        'title': os.path.basename(filepath),
        'parents': [{'id': settings.DRIVE_FOLDER_ID}]
    }

    gfile = drive.CreateFile(file_metadata)
    gfile.SetContentFile(filepath)
    gfile.Upload()

    print(f"Google Drive File ID: {gfile['id']}")


def get_nameTime():
    return timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S ").replace(":", ".")+filename

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
    delta = relativedelta(timezone.localtime(timezone.now()).replace(tzinfo=None), last_backup).days
    print("\nUltimo backup: ", last_backup, file=sys.stderr)
    if(delta > 6 or last_backup is None):
        hacerBackup()
    else:
        print("Dias desde el ultimo backup: ", delta, "\n", file=sys.stderr)

def hacerBackup():
    backupCompleto = True

    try:
        os.makedirs('./backups/', exist_ok=True)
        compressed = shutil.make_archive('./backups/'+get_nameTime(), "zip", ".", filename)
        print("Nuevo backup local: ", compressed, file=sys.stderr)
    except FileNotFoundError:
        backupCompleto = False
    
    # online
    try:
        upload_file(compressed)
    except FileNotFoundError:
        backupCompleto = False
        print("Falta la service account key", file=sys.stderr)
    except HttpError as err:
        backupCompleto = False
        #print(err.resp, file=sys.stderr)
        print(err.content, file=sys.stderr)
    # except ServerNotFoundError: ipconfig /flushdns


    # si se completaron backup local + online, registrar como backup realizado
    # falta considerar, si falla uno que no se haga el otro siempre
    if(backupCompleto):
        with open(BACKUP_TIMESTAMP, 'w') as f:
            f.write(str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")))
        print("Backup completo\n", file=sys.stderr)
    else:
        print("Error de backup\n", file=sys.stderr)
    






