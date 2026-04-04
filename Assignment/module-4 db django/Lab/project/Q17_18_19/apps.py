from django.apps import AppConfig


class Q17_18_19Config(AppConfig):
    name = 'Q17_18_19'

    def ready(self):
        import Q17_18_19.signals
