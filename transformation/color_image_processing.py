# -*- coding: utf-8 -*-

from PIL import Image

from util import *
from i18n import i18n

@check_image_mode(ImageMode.COLOR)
def get_band(im, band):
    bd = band.lower()
    if bd not in ['r', 'g', 'b']:
        raise ValueError(i18n['invalid_band'])

    return canonical_mode(im).split()[{'r': 0, 'g': 1, 'b': 2}[bd]]

@check_image_mode(ImageMode.COLOR)
def color2grayscale(im):
    new_im = Image.new('L', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            new_px[x, y] = round(px[x, y][0] * 0.299 + px[x, y][1] * 0.587 + px[x, y][2] * 0.114)

    return new_im
