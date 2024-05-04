from django.apps import AppConfig


class VendorPulseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_pulse"

    def ready(self):
        from . import signals # noqa