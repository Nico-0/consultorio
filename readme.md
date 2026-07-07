# Consultorio

## Installation

- [Install Git cli](https://git-scm.com/install) if support for the in-app update button is desired.
- [Install Python 3.14.6](https://www.python.org/downloads/release/python-3146/)
- `python -m venv venv`
- `venv\Scripts\activate`
- `pip install -r requirements.txt`
- Rename `.env.example` to `.env`
- `python manage.py makemigrations` (already on repo)
- `python manage.py migrate`
- `python manage.py createsuperuser`

## Configure backups

- In any Google Cloud project [configure Auth Platform](https://console.cloud.google.com/auth/branding). It's needed even for a local app of a single user.
- [Enable Google Drive API](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com) and [create OAuth credentials](https://console.cloud.google.com/apis/credentials)
- Set authorized origins to `http://localhost:8080` and authorized redirect to `http://localhost:8080/`
- Download and place `client_secrets.json` at the root of this server.
- [Create a new test user](https://console.cloud.google.com/auth/audience) with your desired email.
- Copy the ID of any Drive folder from the URL, and place it in `DRIVE_FOLDER_ID` inside `.env` or inside `drive_folder_id.txt`.

## Run the program

- Setup app flavor, `OPTICAL` or `GENERAL` inside `.env`
- `python manage.py runserver 0.0.0.0:8000`

## Desktop Standalone (Windows)

#### Compile with pyinstaller (optional if desired to run from another computer without Python)

- `pyinstaller manage.py --onedir`
- Place all mentioned custom files next to `manage.exe` file and `_internal` folder. (The new root)
- Copy `consultorio` and `historia` folders into `_internal` folder.
- `manage.exe migrate`
- Run with `manage.exe runserver 0.0.0.0:8000 --noreload`

#### Run from Electron

- `npm install`
- Run with `npm run consultorio`
- (Custom shortcut): `powershell.exe -WindowStyle Hidden -Command "npm --prefix C:\consultorio run consultorio"`

#### (To do) Compile with Electron Forge

- (To test)

### Autorun

> So far, this server is designed to run on the same computer as the client.
> Windows task scheduler:

- General -> Run logged or not. Trigger -> On boot.
- Start a program `cmd`
- Add Argument field: `/c python "C:\consultorio\manage.py" runserver 0.0.0.0:8000`
- Start in field: `C:\consultorio`


### Pending testing

- Disable debug mode in `consultorio/settings.py`

### (Deprecated) Configure backups with service account (missing shared drive)

- `pip install google-api-python-client`

- In any Google Cloud project enable Google Drive API and [create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts).
- Place `service_account.json` at the root of this server.
- In any Google Drive folder, share editor permissions with the service account's email.
- Copy the ID of the folder from the URL, and place it in `DRIVE_FOLDER_ID` inside `consultorio/settings.py`.


