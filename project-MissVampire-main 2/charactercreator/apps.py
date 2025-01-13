from django.apps import AppConfig


class CharactercreatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charactercreator'

    def ready(self):
        # Import the signals here
        pass
