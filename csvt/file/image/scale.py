from PIL import Image, ImageOps


def scale_to_min_size(image, min_width, min_height):
    """Returns an image, that isn't smaller than min_width and min_height.
    That means one side is exactly given value and the other is greater.

    This may only makes sense if the image is cut after it is scaled.
    """

    # resize proportinal
    width, height = image.size

    prop_x = float(min_width) / width
    prop_y = float(min_height) / height

    if prop_x < 1.5 > prop_y:
        if prop_x > prop_y:
            height = int(prop_x * height)
            if not height:
                height = 1
            image = image.resize((min_width, height), Image.ANTIALIAS)
        else:
            width = int(prop_y * width)
            if not width:
                width = 1
            image = image.resize((width, min_height), Image.ANTIALIAS)

    return image


def scale_to_max_size(image, max_width, max_height):
    """Returns an image, that isn't bigger than max_width and max_height.

    That means one side is exactly given value and the other is smaller. In
    other words the image fits at any rate in the given box max_width x
    max_height.
    """
    width, height = image.size

    prop_width = float(max_width) / width
    prop_height = float(max_height) / height

    prop_max = max(max_width, max_height) / max(width, height)
    if prop_max < 1.5:
        if prop_height < prop_width:
            width = int(prop_height * width)
            if not width:
                width = 1
            image = image.resize((width, max_height), Image.ANTIALIAS)
        else:
            height = int(prop_width * height)
            if not height:
                height = 1
            image = image.resize((max_width, height), Image.ANTIALIAS)

    return image


def scale_to_width(image, target_width):
    """Returns an image that has the exactly given width and scales height
    proportional.
    """
    width, height = image.size

    prop_width = float(target_width) / width
    new_height = int(prop_width * height)

    image = image.resize((target_width, new_height), Image.ANTIALIAS)

    return image


def scale_to_height(image, target_height):
    """Returns an image that has the exactly given height and scales width
    proportional.
    """
    width, height = image.size

    prop_height = float(target_height) / height
    new_width = int(prop_height * width)

    image = image.resize((new_width, target_height), Image.ANTIALIAS)

    return image


def crop_to_min_size_center(image, width, height):
    """
    """
    # width = max(*image.size)
    # height = width * 0.75
    image_width, image_height = image.size

    prop_x = float(width) / image_width
    prop_y = float(height) / image_height

    if prop_x < 1.5 > prop_y:
        return ImageOps.fit(
            image,
            (width, height),
            Image.ANTIALIAS, 0, (.5, .5)
        )
    else:
        return image


def get_main_color(file):
    """
    Наиболее часто встречающийся цвет в файле картинки
    """

    img = Image.open(file)
    # put a higher value if there are many colors in your image
    colors = img.getcolors(10000)
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present
    except TypeError:
        raise Exception("Too many colors in the image")
