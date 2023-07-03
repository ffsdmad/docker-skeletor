import hashlib
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from parler.models import TranslatableModel, TranslatedFields

from constants import TAG_UPLOADS


class Image(TranslatableModel):
    file = models.ImageField()

    translations = TranslatedFields(
        alt = models.CharField(max_length=50)
    )

    md5hash = models.CharField(max_length=32, editable=False)

    tags = ArrayField(
        models.CharField(max_length=40, choices=TAG_UPLOADS),
        default=list,
        blank=True,
        verbose_name=_("Tags"), size=10
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Images")
        verbose_name_plural = _("Images")

    def calc_md5(self, file):
        md5 = hashlib.md5()
        for chunk in file.chunks():
            md5.update(chunk)
        return md5.hexdigest()

    def save(self, *args, **kwargs):
        if not self.pk or not self.md5hash:
            self.md5hash = self.calc_md5(self.file)
        super().save(*args, **kwargs)
