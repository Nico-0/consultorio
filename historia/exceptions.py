
class GApiReqError(Exception):
    """Custom exception, errores vistos:
        HttpError 403: The user has exceeded their Drive storage quota: La cuenta de drive no tiene espacio disponible
        HttpError 404: "File not found: -DRIVE_FOLDER_ID-"""
    pass