import hashlib
from django import forms
from django.db import models
from django.db.models import Func, F
from django.db.models import Count, Q
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from parler.models import TranslatableModel, TranslatedFields

from constants import TAG_UPLOADS


def make_tags_choices():

    query = Image.objects.annotate(
        tag=Func(F("tags"), function="unnest"),
    )
    query = query.values_list("tag", flat=True).distinct()
    query = query.order_by("tag")

    for x in query:
        yield [x, x]


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


class UploadFile(models.Model):

    file = models.FileField(max_length=255)
    md5hash = models.CharField(max_length=32, editable=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calc_md5(self, file):
        md5 = hashlib.md5()
        for chunk in file.chunks():
            md5.update(chunk)
        return md5.hexdigest()

    def save(self, *args, **kwargs):
        if not self.pk or not self.md5hash:
            self.md5hash = self.calc_md5(self.file)
        super().save(*args, **kwargs)

    def links(self):
        return self.images.count()

    def thumb(self):
        cdn = (
            "https://2mv652sbu3.a.trbcdn.net/"
            "200x100_fit/"
            "media/"
        )
        return mark_safe(f"<img src={cdn}{self.file} alt='self.file' />")

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")


class Image(TranslatableModel):

    translations = TranslatedFields(
        alt=models.CharField(max_length=50)
    )

    name = models.CharField(_("Name"), max_length=50)

    file = models.ForeignKey(
        UploadFile,
        related_name="images",
        on_delete=models.DO_NOTHING,
    )

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


    def save(self, *args, **kwargs):
        if self.tags:
            self.tags = list({*self.tags})
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} / {}".format(self.tags_str(), self.alt)

    def tags_str(self):
        return " / ".join({*self.tags})

    def thumb(self):
        return self.file.thumb()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#  ~ class Profile(models.Model):
    #  ~ user = models.OneToOneField(settings.AUTH_USER_MODEL,
        #  ~ on_delete=models.SET_NULL, null=True,
    #  ~ )

    #  ~ GENDER_CHOICES = (
        #  ~ ('F', 'Female'),
        #  ~ ('M', 'Male')
        #  ~ )

    #  ~ date_of_birth = models.DateField(blank=True, null=True)

    #  ~ gender = models.CharField(max_length=1,
        #  ~ default='F',
        #  ~ blank=False,
        #  ~ choices=GENDER_CHOICES
        #  ~ )



#  ~ class Photos(models.Model):
    #  ~ user = models.ForeignKey(
        #  ~ Profile,
        #  ~ to_field='user',
        #  ~ null=True,
        #  ~ blank=True,
        #  ~ on_delete=models.SET_NULL
    #  ~ )
    #  ~ photo = models.ImageField(
        #  ~ upload_to='photos/%Y/%m/%d/',
        #  ~ blank=True
    #  ~ )
