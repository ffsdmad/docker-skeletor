# coding=utf-8
from file.utils import DuplicateRemovableSystemStorage

FILE_STORAGE = DuplicateRemovableSystemStorage()

POS_TL = 0
POS_TR = 1
POS_BR = 2
POS_BL = 3
POS_C = 4

IMG_POS = [
    (POS_TL, "Слева вверху"),
    (POS_TR, "Справа вверху"),
    (POS_BR, "Справа внизу"),
    (POS_BL, "Слева внизу"),
    (POS_C, "По центру"),
]

MIME_WORD = 1
MIME_EXCEL = 2
MIME_PDF = 3
MIME_TXT = 4
MIME_ZIP = 5

MIMES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": MIME_WORD,
    "application/pdf": MIME_PDF,
    "application/msword": MIME_WORD,
    "application/vnd.oasis.opendocument.text": MIME_WORD,
    "application/rtf": MIME_WORD,
    "text/plain": MIME_TXT,
    "application/vnd.ms-excel": MIME_EXCEL,
    "application/vnd.oasis.opendocument.spreadsheet": MIME_EXCEL,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": MIME_EXCEL,
    "application/zip": MIME_ZIP
}

CROP_MINI = 0
CROP_ALL = 1
CROP_NONE = 2

CROP_PARAMS = (
    (CROP_ALL, "Резать все миниатюры под размер"),
    (CROP_MINI, "Резать все, кроме самой большой"),
    (CROP_NONE, "Оставить, как есть"),
)
