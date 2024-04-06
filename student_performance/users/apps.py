from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "student_performance.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import student_performance.users.signals  # noqa F401
        except ImportError:
            pass
