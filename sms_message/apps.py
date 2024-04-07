from django.apps import AppConfig


class SmsMessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms_message'

    def ready(self) -> None:
        # TODO: It's a best practice to make this an independent app.
        # It currently relies on the other apps, so it's not possible to reuse it.
        import sms_message.signals
