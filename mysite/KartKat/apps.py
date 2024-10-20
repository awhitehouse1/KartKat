from django.apps import AppConfig


class KartkatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'KartKat'

    def ready(self):
        import KartKat.signals
