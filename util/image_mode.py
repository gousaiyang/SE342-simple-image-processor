# -*- coding: utf-8 -*-

import functools
from enum import IntEnum

from i18n import i18n

class ImageMode(IntEnum):
    INVALID = 0
    BINARY = 1
    GRAYSCALE = 2
    COLOR = 3

def get_image_mode(im):
    if im.mode in ['RGB', 'RGBA', 'CMYK', 'YCbCr', 'LAB', 'HSV', 'I', 'F', 'RGBX', 'RGBa']:
        return ImageMode.COLOR
    elif im.mode in ['L', 'P', 'LA']:
        return ImageMode.GRAYSCALE
    elif im.mode == '1':
        return ImageMode.BINARY
    else:
        return ImageMode.INVALID

def canonical_mode(im):
    mode = get_image_mode(im)
    if mode == ImageMode.COLOR:
        return im.convert('RGB')
    elif mode == ImageMode.GRAYSCALE:
        return im.convert('L')
    elif mode == ImageMode.BINARY:
        return im
    else:
        raise TypeError(i18n['invalid_image'])
        return None

def check_image_mode(mode):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(im, *args, **kw):
            if get_image_mode(im) != mode:
                if mode in [ImageMode.BINARY, ImageMode.GRAYSCALE, ImageMode.COLOR]:
                    expected_mode_name = [i18n['binary'], i18n['grayscale'], i18n['color']][mode - 1]
                    error_message = i18n['some_image_mode_expected'] % (expected_mode_name)
                else:
                    error_message = i18n['invalid_image']
                raise TypeError(error_message)
            return func(im, *args, **kw)
        return wrapper
    return decorator
