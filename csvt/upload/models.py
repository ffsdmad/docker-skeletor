import os
import hashlib
import datetime
from django import forms
from django.db import models
from django.db.models import Func, F
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage

from csvt import clean_url_cache


class DuplicateRemovableSystemStorage(FileSystemStorage):
    def get_available_name(self, name, *args, **kwargs):
        """
        Удалить файл, если он существует
        """
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name


def make_tags_choices():

    query = Image.objects.annotate(
        tag=Func(F("tags"), function="unnest"),
    )
    query = query.values_list("tag", flat=True).distinct()
    query = query.order_by("tag")

    for x in query:
        yield [x, x]


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        return super(ArrayField, self).formfield(**kwargs)


def make_images_file_name(instance, filename):
    dt = datetime.datetime.now()
    _name, _ext = os.path.splitext(filename)
    _dir = os.path.join(
        #  ~ settings.MEDIA_ROOT,
        "uploads",
        "images",
        str(dt.year),
        str(dt.month),
        str(dt.day)
    )
    _name = "{}{}".format(instance.md5hash, _ext)
    return os.path.join(_dir.lower(), _name.lower())


class UploadFile(models.Model):

    file = models.FileField(
        max_length=255,
        upload_to=make_images_file_name,
        storage=DuplicateRemovableSystemStorage
    )
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

    def image(self):
        if self.file:
            cdn = (
                "https://2mv652sbu3.a.trbcdn.net"
                "/200x100_fit/"
                "/media/"
            )
            return f"{cdn}{self.file}"

    def clean_cache(self):
        image_url = self.image()
        image_url = image_url.replace("https:", "http:")
        return clean_url_cache(image_url)

    def thumb(self):
        return mark_safe(
            f"""<img width='200'
            src='{self.image()}?V=2'
            alt='{self.file}' />"""
        )

    def delete(self, *args, **kwargs):
        print("delete!!! "*5)
        try:
            self.file.delete(save=True)  # Удаление файла
        except Exception as error:
            print(error)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ("-pk", )
        verbose_name = _("File")
        verbose_name_plural = _("Files")


class Image(models.Model):

    alt = models.CharField(max_length=50, null=True)

    name = models.CharField(_("Name"), max_length=50, editable=False)

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
        ordering = ("-pk", )
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
