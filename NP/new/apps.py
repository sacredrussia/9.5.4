from django.apps import AppConfig


class NewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'new'


    def ready(self):
        import new.signal
