# -*- coding: utf-8 -*-

from enum import Enum

from i18n import i18n

class ImageMode(Enum):
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

def is_rgb_mode(im):
    return im.mode == 'RGB'

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
