# Consultorio

## Run the program

- [Install Git cli](https://git-scm.com/install) if support for the in-app update button is desired.
- [Install Python 3.10.11](https://www.python.org/downloads/release/python-31011/)
- `pip install django`
- `pip install python-dateutil`
- `pip install pillow-heif`
- `pip install qrcode`
- `python manage.py makemigrations`
- `python manage.py migrate`

## Configure backups

- `pip install pydrive`

- In any Google Cloud project [configure Auth Platform](https://console.cloud.google.com/auth/branding). It's needed even for a local app of a single user.
- [Enable Google Drive API](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com) and [create OAuth credentials](https://console.cloud.google.com/apis/credentials)
- Set authorized origins to `http://localhost:8080` and authorized redirect to `http://localhost:8080/`
- Download and place `client_secrets.json` at the root of this server.
- [Create a new test user](https://console.cloud.google.com/auth/audience) with your desired email.
- Copy the ID of any Drive folder from the URL, and place it in `DRIVE_FOLDER_ID` inside `consultorio/settings.py` or inside `drive_folder_id.txt`.

## Run the program

- `python manage.py runserver 0.0.0.0:8000`

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


