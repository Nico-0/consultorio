#pip install pydrive
from pydrive.auth import GoogleAuth, RefreshError, AuthenticationError
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError
from httplib2 import ServerNotFoundError
from django.conf import settings
from .exceptions import GApiReqError

import os, sys
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from dateutil.relativedelta import relativedelta
import shutil
import hashlib
import json

DATABASE = settings.DATABASE
filename = DATABASE.name
BASE_DIR = settings.BASE_DIR
mimeType = 'application/x-7z-compressed'
BACKUP_TIMESTAMP_FILE = BASE_DIR / 'last_backup.txt'
TEMP_CREDENTIALS_FILE = BASE_DIR / 'credentials.json'
BACKUP_LOCATION = settings.BACKUP_LOCATION
days_local_freq = settings.DAYS_LOCAL_FREQ
days_online_freq = settings.DAYS_ONLINE_FREQ

DRIVE_LOGIN = False


def check_creds():
    try:
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(TEMP_CREDENTIALS_FILE)
        gauth.Authorize()
        return gauth
    except AuthenticationError: 
        print("No se pudo autenticar con Gdrive")

def auth():
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() # abre ventana y bloquea el programa
    except RefreshError:
        os.remove(TEMP_CREDENTIALS_FILE)
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
        with open(BACKUP_TIMESTAMP_FILE, 'r') as f:
            timestamp = f.readline().strip()
            hash = f.readline().strip()            
            return parse_datetime(timestamp), hash
    except FileNotFoundError:
        return None, None
    except Exception as e:
        print("⚠️🚨 Error reading backup time file:", e)
        return None, None

def initBackup():
    creds = check_creds()
    try:
        rutinaBackup(creds)
    except (GApiReqError, ServerNotFoundError) as e:
        print(e)

def initNoBackup():
    creds = check_creds()
    if(creds is not None): 
        login_completed()

def checkBackup():
    gauth = auth()
    rutinaBackup(gauth)

def rutinaBackup(creds):
    backupFile = None
    newHash = None

    # backup local
    try:
        last_backup_file = os.listdir(BACKUP_LOCATION)[::-1][0]
        last_backup_hash = hashlib.md5(open(BACKUP_LOCATION / last_backup_file,'rb').read()).hexdigest()
        print(f"Ultimo backup local: {last_backup_file}, '{last_backup_hash}'")
        last_backup = timezone.datetime.fromtimestamp(os.path.getmtime(BACKUP_LOCATION / last_backup_file))
    except (FileNotFoundError, IndexError):
        last_backup = None
        last_backup_hash = None
    now = timezone.localtime(timezone.now()).replace(tzinfo=None)
    delta = relativedelta(now, last_backup).days
    if(delta > days_local_freq or last_backup is None):
        backupFile, newHash = backupLocal(last_backup_hash)
    else:
        print("Dias desde el ultimo backup local: ", delta, " freq: ", days_local_freq)


    if(creds is not None):
        # rutina backup online
        last_backup, last_hash = get_last_backup_time()
        delta = relativedelta(now, last_backup).days
        print(f"\nUltimo backup online: {last_backup}, '{last_hash}'")
        if(delta > days_online_freq or last_backup is None):
            backupOnline(backupFile, newHash, last_hash, creds)
        else:
            login_completed()
            print("Dias desde el ultimo backup online: ", delta, " freq: ", days_online_freq, "\n")

def backupLocal(last_backup_hash):
    try:
        compressed = shutil.make_archive(BACKUP_LOCATION / get_nameTime(), "zip", ".", DATABASE)
        new_backup_hash = hashlib.md5(open(compressed,'rb').read()).hexdigest()
        if((new_backup_hash != last_backup_hash) or last_backup_hash is None):
            print("Nuevo backup local: ", compressed, file=sys.stderr)
            return compressed, new_backup_hash
        else:
            os.remove(compressed)   #todo comprimir en memoria para no crear y borrar
            print('Backup duplicado, borrando '+new_backup_hash)
            return None, None
    except FileNotFoundError:
        print("FileNotFoundError en backup local")
        return None, None


def backupOnline(backupFile, newHash, lastHash, creds):
    backupCompleto = False
    try:
        if(backupFile is None):
            backupFile, newHash = backupLocal(lastHash)
        if(backupFile is not None):
            upload_file(backupFile, creds)
            backupCompleto = True
        login_completed()
    except FileNotFoundError:
        print("FileNotFoundError", file=sys.stderr)
    #except ServerNotFoundError as e: # ipconfig /flushdns
    except ApiRequestError as e:
        raise GApiReqError(json.loads(e.args[0].content.decode("utf-8"))["error"]["message"])
    

    # guardar hora de ultimo backup online
    if(backupCompleto):
        with open(BACKUP_TIMESTAMP_FILE, 'w') as f:
            f.write(str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")))
            f.write('\n' + newHash)
        print(f"Backup online completo: {backupFile}\n", file=sys.stderr)
    else:
        print("No realizado backup online\n", file=sys.stderr)
    
def forzarBackup():
    gauth = auth()
    backupOnline(None, None, None, gauth)

def login_completed():
    global DRIVE_LOGIN; DRIVE_LOGIN = True

def session_status(request):
    return {
        "drive_session": DRIVE_LOGIN,
    }


'''
#pip install google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
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
