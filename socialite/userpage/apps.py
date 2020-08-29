from django.apps import AppConfig


class UserpageConfig(AppConfig):
    name = 'userpage'

    # Here import signals file from the application like below.
    def ready(self):
        import userpage.signals
