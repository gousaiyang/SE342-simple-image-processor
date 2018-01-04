# -*- coding: utf-8 -*-

import math
from enum import Enum
from PIL import Image

from util import *

class ContrastMode(Enum):
    LINEAR = 0
    PIECEWISE_LINEAR = 1
    LOGARITHMIC = 2
    EXPONENTIAL = 3

def contrast_linear_point_band(v, a, b, c, d):
    if v < a or v == 0:
        return c
    elif v > b or a == b:
        return d
    else:
        return (v - a) * (d - c) / (b - a) + c

def contrast_linear(im, a, b, c, d):
    assert isinstance(a, int)
    assert isinstance(b, int)
    assert isinstance(c, int)
    assert isinstance(d, int)
    assert a >= 0 and a <= 256
    assert b >= 0 and b <= 256
    assert c >= 0 and c <= 256
    assert d >= 0 and d <= 256
    assert a <= b
    assert c <= d

    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if mode == ImageMode.COLOR:
                pr, pg, pb = px[x, y]
                new_r = round(contrast_linear_point_band(pr, a, b, c, d))
                new_g = round(contrast_linear_point_band(pg, a, b, c, d))
                new_b = round(contrast_linear_point_band(pb, a, b, c, d))
                new_px[x, y] = (new_r, new_g, new_b)
            else:
                new_px[x, y] = round(contrast_linear_point_band(px[x, y], a, b, c, d))

    return new_im

def contrast_piecewise_point_band(v, a, b, c, d):
    if v == 0:
        return 0
    elif v < a:
        return v * c / a
    elif v < b:
        return (v - a) * (d - c) / (b - a) + c
    elif v != 255:
        return (v - b) * (255 - d) / (255 - b) + d
    else:
        return 255

def contrast_piecewise(im, a, b, c, d):
    assert isinstance(a, int)
    assert isinstance(b, int)
    assert isinstance(c, int)
    assert isinstance(d, int)
    assert a >= 0 and a <= 255
    assert b >= 0 and b <= 255
    assert c >= 0 and c <= 255
    assert d >= 0 and d <= 255
    assert (a == 0) ^ (c != 0)
    assert (b == 255) ^ (d != 255)
    assert a <= b
    assert c <= d

    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if mode == ImageMode.COLOR:
                pr, pg, pb = px[x, y]
                new_r = round(contrast_piecewise_point_band(pr, a, b, c, d))
                new_g = round(contrast_piecewise_point_band(pg, a, b, c, d))
                new_b = round(contrast_piecewise_point_band(pb, a, b, c, d))
                new_px[x, y] = (new_r, new_g, new_b)
            else:
                new_px[x, y] = round(contrast_piecewise_point_band(px[x, y], a, b, c, d))

    return new_im

def contrast_logarithmic_point_band(v, a, b):
    return a + b * math.log(v + 1)

def contrast_logarithmic(im, a, b):
    assert isinstance(a, (float, int))
    assert isinstance(b, (float, int))
    assert a >= 0 and a <= 255
    assert b >= 0

    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if mode == ImageMode.COLOR:
                pr, pg, pb = px[x, y]
                new_r = min(round(contrast_logarithmic_point_band(pr, a, b)), 255)
                new_g = min(round(contrast_logarithmic_point_band(pg, a, b)), 255)
                new_b = min(round(contrast_logarithmic_point_band(pb, a, b)), 255)
                new_px[x, y] = (new_r, new_g, new_b)
            else:
                new_px[x, y] = min(round(contrast_logarithmic_point_band(px[x, y], a, b)), 255)

    return new_im

def contrast_exponential_point_band(v, a, b):
    return b ** (v - a) - 1

def contrast_exponential(im, a, b):
    assert isinstance(a, (float, int))
    assert isinstance(b, (float, int))
    assert a >= 0 and a <= 255
    assert b >= 0

    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if mode == ImageMode.COLOR:
                pr, pg, pb = px[x, y]
                new_r = max(min(round(contrast_exponential_point_band(pr, a, b)), 255), 0)
                new_g = max(min(round(contrast_exponential_point_band(pg, a, b)), 255), 0)
                new_b = max(min(round(contrast_exponential_point_band(pb, a, b)), 255), 0)
                new_px[x, y] = (new_r, new_g, new_b)
            else:
                new_px[x, y] = max(min(round(contrast_exponential_point_band(px[x, y], a, b)), 255), 0)

    return new_im
