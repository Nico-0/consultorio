# Consultorio

## Run the program

- Disable debug mode in `consultorio/settings.py`

- pip install django
- `python manage.py runserver`
- `python manage.py makemigrations`
- `python manage.py migrate`

## Configure backups

- `pip install pydrive`

- In any Google Cloud project [configure Auth Platform](https://console.cloud.google.com/auth/branding). It's needed even for a local app of a single user.
- [Enable Google Drive API](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com) and [create OAuth credentials](https://console.cloud.google.com/apis/credentials)
- Set authorized origins to `http://localhost:8080` and authorized redirect to `http://localhost:8080/`
- Download and place `client_secrets.json` at the root of this server.
- [Create a new test user](https://console.cloud.google.com/auth/audience) with your desired email.
- Copy the ID of any Drive folder from the URL, and place it in `DRIVE_FOLDER_ID` inside `consultorio/settings.py`.

### (Deprecated) Configure backups with service account (missing shared drive)

- `pip install google-api-python-client`

- In any Google Cloud project enable Google Drive API and [create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts).
- Place `service_account.json` at the root of this server.
- In any Google Drive folder, share editor permissions with the service account's email.
- Copy the ID of the folder from the URL, and place it in `DRIVE_FOLDER_ID` inside `consultorio/settings.py`.


