#pip install google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

#pip install pydrive
from pydrive.auth import GoogleAuth, RefreshError, AuthenticationError
from pydrive.drive import GoogleDrive
from httplib2 import ServerNotFoundError
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
DRIVE_LOGIN = False

'''
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
'''

def check_creds():
    try:
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("credentials.json")
        gauth.Authorize()
        login_completed()
        return gauth
    except AuthenticationError: 
        print("No se pudo autenticar con Gdrive")

def auth():
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() # abre ventana y bloquea el programa
        login_completed()
    except RefreshError:
        os.remove("./credentials.json")
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
    return gauth    

def upload_file(filepath, gauth):
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
        print("⚠️🚨 Error reading backup time file:", e)
        return None

def rutinaBackup():
    days_local_freq = 1
    days_online_freq = 2
    backupFile = None

    # backup local
    try:
        last_backup = timezone.datetime.fromtimestamp(os.path.getmtime("backups/"))
    except FileNotFoundError:
        last_backup = None
    now = timezone.localtime(timezone.now()).replace(tzinfo=None)
    delta = relativedelta(now, last_backup).days
    if(delta > days_local_freq or last_backup is None):
        backupFile = backupLocal()
    else:
        print("Dias desde el ultimo backup local: ", delta)

    # checkear el login
    creds = check_creds()

    if(creds is not None):
        # rutina backup online
        last_backup = get_last_backup_time()
        delta = relativedelta(now, last_backup).days
        print("\nUltimo backup online: ", last_backup, file=sys.stderr)
        if(delta > days_online_freq or last_backup is None):
            backupOnline(backupFile, creds)
        else:
            print("Dias desde el ultimo backup online: ", delta, "\n", file=sys.stderr)

def backupLocal():
    try:
        os.makedirs('./backups/', exist_ok=True)
        compressed = shutil.make_archive('./backups/'+get_nameTime(), "zip", ".", filename)
        print("Nuevo backup local: ", compressed, file=sys.stderr)
        return compressed
    except FileNotFoundError:
        print("FileNotFoundError en backup local")


def backupOnline(backupFile, creds):
    backupCompleto = False
    try:
        if(backupFile is None):
            backupFile = backupLocal()
        upload_file(backupFile, creds)
        backupCompleto = True
    except FileNotFoundError:
        print("FileNotFoundError", file=sys.stderr)
    except ServerNotFoundError:
        print("ServerNotFoundError")
    except HttpError as err:
        #print(err.resp, file=sys.stderr)
        print(err.content, file=sys.stderr)
    # except ServerNotFoundError: ipconfig /flushdns

    # guardar hora de ultimo backup online
    if(backupCompleto):
        with open(BACKUP_TIMESTAMP, 'w') as f:
            f.write(str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")))
        print("Backup online completo\n", file=sys.stderr)
    else:
        print("Error de backup online\n", file=sys.stderr)
    
def forzarBackup():
    gauth = auth()
    backupOnline(None, gauth)

def login_completed():
    global DRIVE_LOGIN; DRIVE_LOGIN = True

def session_status(request):
    return {
        "drive_session": DRIVE_LOGIN,
    }





