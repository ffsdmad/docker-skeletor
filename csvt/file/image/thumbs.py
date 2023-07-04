# python imports
import os
import requests
import tempfile
from PIL import Image
from io import BytesIO

# django imports
from django.core.files.base import ContentFile, File
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile

# lfs imports
from file.image.scale import (
    scale_to_min_size,
    crop_to_min_size_center,
    scale_to_max_size
)


def get_name_ext(url):
    pass


def generate_thumb(img, w, h, format, cut=True):
    """
    Generates a thumbnail image and returns
    a ContentFile object with the thumbnail

    Parameters:
    ===========
    img         File object

    thumb_size  desired thumbnail size, ie: (200,120)

    format      format of the original image ("jpeg","gif","png",...)
                (this format will be used for the generated thumbnail, too)

    crop        Crop image
    """
    img.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)

    # Convert to RGB if necessary
    # if image.mode not in ("L", "RGB"):
    # image = image.convert("RGB")

    if cut:
        new_image = crop_to_min_size_center(
            scale_to_min_size(image, w, h), w, h
        )
    else:
        new_image = scale_to_max_size(image, w, h)

    io = BytesIO()

    # PNG and GIF are the same, JPG is JPEG
    if format.upper() == "JPG":
        format = "JPEG"

    new_image.save(io, format)
    return ContentFile(io.getvalue())


class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """

    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)
        self.sizes = self.field.sizes

        if args:
            self.construct_crop(args[0])

        self.exturl = None
        if self.sizes:
            def get_size(self, size):
                if not self:
                    return ""
                else:
                    # self.url.rsplit(".",1)
                    split = os.path.splitext(self.url)
                    name, ext = None, None
                    if len(split) == 2:
                        name, ext = split
                        ext = ext.replace(".", "")
                    if len(split) == 1:
                        name = split[0]
                        ext = "jpg"

                    if len(split) == 0 or len(split) > 2:
                        raise ValueError(
                            "Url must contains name and ext #" + self.url
                        )

                    thumb_url = "%s.%sx%s.%s" % (name, w, h, ext)
                    return thumb_url

            for size in self.sizes:
                (w, h, cut) = size
                setattr(self, "url_%sx%s" % (w, h), get_size(self, size))

    def construct_crop(self, model_object):
        # model_object - объект модели,
        # который содержит это поле ImageWithThumbsFieldFile
        if not self.sizes:
            return
        num = 0
        count = len(self.sizes)
        sizes = list(self.sizes)
        for s in self.sizes:
            num += 1
            if len(s) < 3:  # Не присутствует параметр crop
                if model_object.__class__.__name__ == "Image":
                    crop_settings = model_object.crop
                    if crop_settings == 0:
                        crop = True if num < count else False
                    elif crop_settings == 1:
                        crop = True
                    else:
                        crop = False
                else:
                    crop = False  # По умолчанию не режем
                s += (crop, )
                sizes[num - 1] = s
        self.sizes = tuple(sizes)

    def save(self, name, content, save=True):

        super(ImageWithThumbsFieldFile, self).save(name, content, save)
        self.save_thumbs()

    def upload(self):
        """
        Если имя файла отсутствует, формируем из даты, расширение из адреса
        fullfilename - имя файла с расширением без пути
        """
        url = self.exturl

        if url:
            with requests.get(url, stream=True) as r:

                with tempfile.TemporaryFile(mode="w+b") as f:

                    for chunk in r.iter_content(1024):
                        f.write(chunk)

                    fname, ext = os.path.splitext(url)

                    print(fname, ext)

                    if not ext:
                        ext = ".jpg"

                    # Имеет значение только расширение для миниатюр,
                    # т.к. основное имя задается в make_upload_path

                    fullfilename = "%s%s" % (
                        fname,
                        ext
                    )

                    self.save(
                        fullfilename,
                        File(f),
                        save=False
                    )

    def delete(self, save=True):
        self.delete_thumbs()
        self.delete_image()
        super(ImageWithThumbsFieldFile, self).delete(save)

    # Сохраняет миниатюры на диске
    def save_thumbs(self):  # По умолчанию отрезаем
        if self.sizes:
            split = os.path.splitext(self.name)  # self.name.rsplit(".",1)\
            name, ext = None, None
            if len(split) == 2:
                name, ext = split
                ext = ext.replace(".", "")
            if len(split) == 1:
                name = split[0]
                ext = "jpg"

            if len(split) == 0 or len(split) > 2:
                raise ValueError("Url must contains name and ext #" + self.url)
            if name and ext:
                for size in self.sizes:
                    (w, h, cut) = size

                    thumb_name = "%s.%sx%s.%s" % (name, w, h, ext)

                    # Не отрезаем, если cut или последний  размер миниатюры
                    thumb_content = generate_thumb(
                        self.file, w, h, ext, cut=cut
                    )

                    thumb_name_ = self.storage.save(thumb_name, thumb_content)

                    if not thumb_name == thumb_name_:
                        raise ValueError(
                            "There is already a file named %s" % thumb_name
                        )

    # Удаляет основное изображение (файл) с диска
    def delete_image(self):
        name = self.name
        try:
            self.storage.delete(name)
        except Exception:
            pass

    # Удаляет миниатюры (файлы) с диска
    def delete_thumbs(self):
        if self.sizes:
            for size in self.sizes:
                (w, h, cut) = size
                split = os.path.splitext(self.name)
                if len(split) == 2:
                    name, ext = split
                    ext = ext.replace(".", "")
                    thumb_name = "%s.%sx%s.%s" % (name, w, h, ext)
                    try:
                        self.storage.delete(thumb_name)
                    except Exception:
                        pass


class ImageWithThumbsField(ImageField):
    """
    To do:
    ======
    Add method to regenerate thubmnails

    """
    attr_class = ImageWithThumbsFieldFile

    def __init__(
        self, name=None, width_field=None,
        height_field=None, sizes=None,
        max_length=255, **kwargs
    ):
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        self.sizes = sizes
        self.max_length = max_length
        super(ImageField, self).__init__(**kwargs)
