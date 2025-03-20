from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Ton code ici
        import core.signals  # Importer les signaux pour qu'ils soient enregistrés
        pass




