from django.apps import AppConfig


class PersonConfig(AppConfig):
    name = 'person'

    # it calls signal for session validation
    def ready(self):
        import person.signals