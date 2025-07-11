# Consultorio

## Run the program

- Disable debug mode in `consultorio/settings.py`

- `python manage.py runserver`
- `python manage.py makemigrations`
- `python manage.py migrate`

## Configure backups

- `pip install google-api-python-client`

- In any Google Cloud project enable Google Drive API and [create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts).
- Place `service_account.json` at the root of this server.
- In any Google Drive folder, share editor permissions with the service account's email.
- Copy the ID of the folder from the URL, and place it in `DRIVE_FOLDER_ID` inside `consultorio/settings.py`.