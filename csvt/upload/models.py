from django.db import models
from django.utils.translation import gettext_lazy as _


class Image(models.Model):
    image = models.ImageField()
    alt = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Images")
        verbose_name_plural = _("Images")

