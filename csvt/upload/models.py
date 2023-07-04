import hashlib
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from parler.models import TranslatableModel, TranslatedFields

from constants import TAG_UPLOADS


def make_tags_choices():
    tags = set()
    for d in Image.objects.values("tags"):

        tags |= set(d["tags"])

    return [[x, x] for x in sorted(tags)]


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(models.CharField(max_length=..., choices=(...,)), default=[...])
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": make_tags_choices(),
            #  ~ "widget": dict(attrs=dict(style="width: 200px"), is_required=False),
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Image(TranslatableModel):
    file = models.ImageField()

    translations = TranslatedFields(
        alt = models.CharField(max_length=50)
    )

    name = models.CharField(_("Name"), max_length=50)

    md5hash = models.CharField(max_length=32, editable=False)

    #  ~ tags = ArrayField(
        #  ~ models.CharField(max_length=40, choices=TAG_UPLOADS),
        #  ~ default=list,
        #  ~ blank=True,
        #  ~ verbose_name=_("Tags"), size=10
    #  ~ )

    tags = ChoiceArrayField(
        models.CharField(
            max_length=40,
            #  ~ choices=TAG_UPLOADS,
            #  ~ default=['for_him', 'for_her']
        )
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
        #  ~ self.tags = list(set(*self.tags))
        if self.tags:
            self.tags = list({*self.tags})
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} / {}".format(self.tags_str(), self.alt)

    def tags_str(self):
        return " / ".join({*self.tags})
