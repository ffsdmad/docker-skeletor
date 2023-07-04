# coding=utf-8
import re
from math import sqrt

re_color = re.compile('#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})')


def hex2rgb(color):
    """
    Возвращает RGB представление цвета, заданного в шестнадцатиричном формате
    color - Цвет формата #FFFFFF
    return (x,y,z)
    """
    return tuple(int(x, 16) for x in re_color.match(color).groups())


def rgb2hex(color):
    """
    Возвращает шестнадцатиричное представление цвета,
    заданного в формате (x,y,z)
    color - Цвет формата (x,y,z)
    return #FFFFFF
    """

    res = '#'
    if not isinstance(color, tuple):
        return None
    for c in color:
        chex = '%X' % c
        if len(chex) == 1:
            chex += chex
        res += chex
    return res


def similarity(color1, color2):
    """Computes the pearson correlation coefficient for two colors. The result
    will be between 1.0 (very similar) and -1.0 (no similarity)."""

    c1 = hex2rgb(color1)
    c2 = hex2rgb(color2)

    s1 = sum(c1)
    s2 = sum(c2)
    sp1 = sum(map(lambda c: pow(c, 2), c1))
    sp2 = sum(map(lambda c: pow(c, 2), c2))
    sp = sum(map(lambda x: x[0] * x[1], zip(c1, c2)))

    try:
        return (
            (sp - (s1 * s2 / 3.0)) /
            sqrt(
                (sp1 - pow(s1, 2) / 3.0) *
                (sp2 - pow(s2, 2) / 3.0)
            )
        )
    except Exception:
        return -1.0
