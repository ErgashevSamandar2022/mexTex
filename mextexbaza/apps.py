from django.apps import AppConfig


class MextexbazaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mextexbaza'
def ready(self):
    import mextexbaza.signals