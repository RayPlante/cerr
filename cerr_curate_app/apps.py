""" Apps file for setting core main registry app package when app is ready
"""
import sys

from django.apps import AppConfig

from cerr_curate_app import discover


class InitApp(AppConfig):
    """Cerr curate app application settings"""

    name = "cerr_curate_app"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "makemigrations" not in sys.argv:
            if "migrate" not in sys.argv:
                # Init registry
                discover.init_cerr()
