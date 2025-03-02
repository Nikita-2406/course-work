from django.apps import AppConfig
# from backend.app.signals import create_admin_user


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals
