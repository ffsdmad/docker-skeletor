# -*- coding:utf-8 -*-
from datetime import date, datetime
import time
import hashlib
import os
import random
import socket
import urllib

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pytils.translit import slugify


class DuplicateRemovableSystemStorage(FileSystemStorage):
    def get_available_name(self, name):
        """
        Удалить файл, если он существует
        """
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name


def make_upload_images_path(instance, filename, **kwargs):
    """
    Создает путь для сохранения файлов изображений
    Имя файла - на основе текущей даты
    """
    return make_upload_path(filename, date_filename, datetime.now(), folder="images")


def make_upload_files_path(instance, filename, **kwargs):
    """
    Создает путь для сохранения файлов изображений
    Имя файла - на основе текущей даты
    """
    return make_upload_path(filename, slugify_filename, datetime.now(), folder="files")


###########################################################################
def dummy_filename(*args):
    return args[0]


def slugify_filename(*args):
    name, ext = os.path.splitext(args[0])
    if not ext:
        ext = ""
    return "%s%s" % (slugify(name), ext)


def unique_filename(filename):
    fileName, fileExtension = os.path.splitext(filename)
    if not fileExtension:
        fileExtension = ".no"
    return "%s%s" % (guid(), fileExtension)


def date_filename(filename, date_time):
    if not isinstance(date_time, datetime): return None
    fileName, fileExtension = os.path.splitext(filename)
    if not fileExtension:
        fileExtension = ".no"
    return "%s%s" % (datetime.strftime(date_time, "%Y%m%d%H%M%S"), fileExtension)

########################################################################

def make_unique_path(instance, filename, **kwargs):
    """
    Создает путь для сохранения файла
    Имя файла - случайное
    """
    return make_upload_path(filename, unique_filename)


def make_date_current_path(instance, filename, **kwargs):
    """
    Создает путь для сохранения файла
    Имя файла формируется на основе параметра created инстанса
    """
    return make_upload_path(filename, date_filename, datetime.now())


def make_slugify_path(instance, filename, **kwargs):
    """
    Создает путь для сохранения файла
    Имя файла транслитеруется
    """
    return make_upload_path(filename, slugify_filename)


def make_direct_path(instance, filename, **kwargs):
    """
    Создает путь для сохранения файла
    Имя файла не изменяется относительно загружаемого
    """
    return make_upload_path(filename, dummy_filename)


def make_upload_path(filename, func, *args, **kwargs):
    """Создает путь для сохранения файла
    Имя файла формируется в зависимости от функции func
    Путь - в зависимости от текущей даты
    func - функция дополнительной обработки имени файла
    """
    folder = kwargs.pop("folder", "files")

    upload_dir = date.today().strftime(settings.UPLOAD_PATH)
    upload_path = os.path.join(folder, upload_dir)
    upload_full_path = os.path.join(settings.MEDIA_ROOT, folder, upload_dir)
    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    return "%s/%s" % (upload_path, func(filename, *args, **kwargs))


def guid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t = long(time.time() * 1000)
    r = long(random.random() * 100000000000000000)
    try:
        a = socket.gethostbyname(socket.gethostname())
    except:
        # if we can"t get a network address, just imagine one
        a = random.random() * 100000000000000000
    data = str(t) + " " + str(r) + " " + str(a) + " " + str(args)
    data = hashlib.md5(data).hexdigest()

    return data


def iq_quote(string, encoding="utf-8"):
    """Перекодирует строку, затем квотирует (" "="%20"
    """
    return urllib.quote(string.encode(encoding))

