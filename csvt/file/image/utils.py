# coding=utf-8
from cStringIO import StringIO
from os.path import join
import urllib
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from core.utils import get_default_settings
from file.image.scale import scale_to_max_size
from file.image.thumbs import generate_thumb
from file.settings import POS_TR, POS_BR, POS_BL

from PIL import Image, ImageDraw, ImageFont


def get_image_font(font_name, font_size):
    font_file_path = join(settings.FONTS_PATH, font_name)
    return ImageFont.truetype(font_file_path, font_size)


def upload_from_url(url, width, height, type="jpg"):
    """
    Загружает файл
    и возвращает готовый для записи объект ImageField
    """

    result = urllib.urlretrieve(url)
    file = generate_thumb(open(result[0]), (width, height), type)
    file.seek(0)
    image = Image.open(file)

    # Convert to RGB if necessary
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    temp_handle = StringIO()
    image.save(temp_handle, format="JPEG")
    temp_handle.seek(0)

    if type == "jpg":
        type = "jpeg"

    return SimpleUploadedFile(
        "foo.jpg",
        temp_handle.read(),
        content_type="image/" + type
    )


def draw_logo(image, position, max_width=100, max_heihgt=100):
    """
    Рисует логотип на изображении
    position - IMG_POS /core/settings.py
    max_width ширина миниатюры,
    max_heihgt = высота миниатюры
    """
    logo = get_default_settings().logo
    logo.seek(0)
    logo = Image.open(logo)

    new_logo_image = scale_to_max_size(logo, (max_width, max_heihgt))

    wi, hi = image.size
    wl, hl = new_logo_image.size
    marginx, marginy = 10, 10

    # Если справа
    if position in (POS_TR, POS_BR):
        logox = wi - marginx - wl
    else:
        logox = marginx

    # Если снизу
    if position in (POS_BL, POS_BR):
        logoy = hi - marginy - hl
    else:
        logoy = marginy

    image.paste(new_logo_image, (logox, logoy), new_logo_image)
    return image


def draw_text(image, text, coord, color, font_name, font_size, bg=True):
    """
    image - image
    text - text
    font_type  - one of "normal", "italic", "bold"
    coord - (x,y)
    font_size - font size
    color - (r, g, b)
    bg - рисовать подложку
    """

    draw = ImageDraw.Draw(image)
    font = get_image_font(font_name, font_size)

    if bg:
        lightness = color[0] + color[1] + color[2]
        # Если цвет ближе к светлому, то подложка - темная и наоборот
        if lightness > 384:
            fill_bg = (0, 0, 0)
            bg_move = -1  # Сдвигаем подложку влево и вверх
        else:
            fill_bg = (255, 255, 255)
            bg_move = 1  # Сдвигаем подложку вправо и вниз и вверх
        x, y = coord
        draw.text(  # Подложка
            (x + bg_move, y + bg_move),
            text, font=font,
            fill=fill_bg
        )

    draw.text(coord, text, font=font, fill=color)
    return image
