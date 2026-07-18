# Consultorio

## Installation

- [Install Git cli](https://git-scm.com/install) if support for the in-app update button is desired.
- [Install Python 3.14.6](https://www.python.org/downloads/release/python-3146/)
- `python -m venv venv`
- `venv\Scripts\activate`
- `pip install -r requirements.txt`

## Configure backups

- In any Google Cloud project [configure Auth Platform](https://console.cloud.google.com/auth/branding). It's needed even for a local app of a single user.
- [Enable Google Drive API](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com) and [create OAuth credentials](https://console.cloud.google.com/apis/credentials)
- Set authorized origins to `http://localhost:8080` and authorized redirect to `http://localhost:8080/`
- Download and place `client_secrets.json` at the root of this server.
- [Create a new test user](https://console.cloud.google.com/auth/audience) with your desired email.
- Copy the ID of any Drive folder from the URL, and place it in `DRIVE_FOLDER_ID` inside `.env`.

## Run the program

- `python manage.py runserver 0.0.0.0:8000`
- Database and env files will be created on first run. Follow createsuperuser prompts.
- Setup app flavor, `OPTICAL` or `GENERAL` inside `.env`

### Run from Electron

- Open `electron` folder.
- `npm install`
- Run with `npm run consultorio`
- (Custom shortcut): `powershell.exe -WindowStyle Hidden -Command "npm --prefix C:\consultorio run consultorio"`

## Desktop Standalone (Windows)

### Compile with pyinstaller (bundles Python to the app)

- `pyinstaller pyinstaller.spec`
- Open `dist/manage` folder.
- Run with `manage.exe runserver 0.0.0.0:8000 --noreload`

### Compile with Electron Forge (bundles npm to the app)

- `npm run make`
- Check `out` folder for `consultorio.exe` or `Setup.exe`.

#### Autorun

> So far, this server is designed to run on the same computer as the client.
> Windows task scheduler:

- General -> Run logged or not. Trigger -> On boot.
- Start a program `cmd`
- Add Argument field: `/c python "C:\consultorio\manage.py" runserver 0.0.0.0:8000`
- Start in field: `C:\consultorio`


#### Pending

- Disable Django debug mode. WhiteNoise serves static files but does not serve media files.



