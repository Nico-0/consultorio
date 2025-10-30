from django.apps import AppConfig


class HistoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'historia'

    def ready(self):
        print("--------------------------------------------------------------------------------------------")
        import historia.signals
        from .backup import initBackup, get_set_drive_folder
        get_set_drive_folder()
        initBackup()

