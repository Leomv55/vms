from django.apps import AppConfig


class VendorPulseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_pulse"

    def ready(self):
        from .signals import create_performance_history # noqa
