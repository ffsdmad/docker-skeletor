from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FileConfig(AppConfig):
    name = 'file'
    verbose_name = _('Files')
