from os import listdir

from django.contrib.sites.models import Site
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteConf(models.Model):

    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, primary_key=True
    )

    title = models.CharField(max_length=150, blank=True)
    keywords = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=250, blank=True)

    is_public = models.BooleanField(_("Published"), default=True)

    template_name = models.CharField(
        max_length=250,
        verbose_name=_("Template name"),
        choices=(
            (f, f) for f in sorted(
                listdir(settings.BASE_DIR / "templates/")
            ) if f.split(".")[-1] in ("html", "vue")
        ),
        null=True,
        blank=True,
        default="base.html",
    )

    def __str__(self):
        return self.site.name
