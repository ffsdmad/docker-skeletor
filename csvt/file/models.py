import datetime
import os
import random

from django.db import models
from django.utils.safestring import mark_safe

from file.image.thumbs import ImageWithThumbsField
from file.settings import MIMES, MIME_WORD, MIME_EXCEL, MIME_PDF, MIME_TXT, MIME_ZIP, CROP_PARAMS, CROP_MINI
from file.utils import make_upload_files_path, make_upload_images_path


class Image(models.Model):
    """image с названиями и несколькими размерами.
    """
    title = models.CharField("Заголовок", blank=True, max_length=100)

    image = ImageWithThumbsField(
        verbose_name="Изображение",
        upload_to=make_upload_images_path,
        blank=True, null=True, max_length=255,
        sizes=((200, 150), (300, 225), (400, 300), (800, 800))
    )

    exturl = models.CharField("URL", blank=True, max_length=255)
    crop = models.PositiveSmallIntegerField(
        "Как резать миниатюры", choices=CROP_PARAMS, default=CROP_MINI
    )

    class Meta:
        #  ~ ordering = ("position", )
        verbose_name_plural = "Изображения"
        verbose_name = "Изображение"

    def __str__(self):
        return self.title or str(self.id)

    def save(self, *args, **kwargs):
        """Заполняет title.
        """

        # Если заполнен внешний адрес и нет изображениея, пытаемся скачать
        if self.exturl:
            self.image.exturl = self.exturl.strip()
            self.exturl = ""
            self.image.upload()

        super(Image, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            # Удаление файлов изображения и миниатюр с диска
            self.image.delete(save=True)
        except:
            pass
        super(Image, self).delete(*args, **kwargs)

    def images(self):
        return mark_safe(
            """<img src="{}" alt="{}"/>""".format(
                self.image.url_200x150, self.title
            )
        )

    def thumb(self):
        if self.image and os.path.exists(self.image.path) and self.image.file:
            return " | ".join([
                self.image.url_200x150,
                self.image.url_300x225,
                self.image.url_400x300,
                self.image.url_800x800
            ])
        return ""

    thumb.allow_tags = True


class File(models.Model):
    """ файл
    """

    title = models.CharField("Заголовок", blank=True, max_length=255)
    file = models.FileField(verbose_name="Файл", upload_to=make_upload_files_path, max_length=255, blank=True, null=True)

    mime = models.CharField("Mime", blank=True, max_length=255)
    ext = models.CharField("Тип", blank=True, max_length=50)

    size = models.IntegerField("Размер", blank=True, null=True)

    class Meta:
        #  ~ ordering = ("position", )
        verbose_name_plural = "Файлы"
        verbose_name = "Файл"

    def __unicode__(self):
        return self.title or u""

    def save(self, *args, **kwargs):
        """Заполняет title.
        """
        if self.file and self.file.name:
            split = os.path.splitext(self.file.name)
            if len(split) == 2:
                name, ext = split
                ext = ext.replace(".", "")
                if ext:
                    self.ext = ext
                else:
                    self.ext = "---"

            if not self.title:
                self.title = self.file.name


        if self.file.file and  hasattr(self.file.file, "content_type"):
            self.mime = self.file.file.content_type

        if self.file.size:
            self.size = self.file.size

        if not self.title:
            self.title = "%s" % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

        self.title = self.title[:255]
        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            self.file.delete(save=True)  # Удаление файла
        except:
            pass
        super(File, self).delete(*args, **kwargs)

    def get_icon(self):
        if not self.mime:
            return ""
        mime = MIMES.get(self.mime)
        if mime == MIME_WORD:
            return "fa-file-word-o"
        if mime == MIME_EXCEL:
            return " fa-file-excel-o"
        if mime == MIME_PDF:
            return "fa-file-pdf-o"
        if mime == MIME_TXT:
            return "fa-file-text"
        if mime == MIME_ZIP:
            return "fa-file-zip-o"
        return "fa-file"

    def url(self):
        return self.file.url

    url.allow_tags = True
