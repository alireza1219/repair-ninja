from django.apps import AppConfig


class RepairCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repair_core'

    def ready(self) -> None:
        import repair_core.signals.handlers
