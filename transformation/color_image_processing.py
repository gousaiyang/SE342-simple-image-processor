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

def RGB2HSL(r, g, b):
    assert isinstance(r, int)
    assert isinstance(g, int)
    assert isinstance(b, int)
    assert r >= 0 and r < 256
    assert g >= 0 and g < 256
    assert b >= 0 and b < 256

    r_v = r / 256
    g_v = g / 256
    b_v = b / 256

    max_v = max(r_v, g_v, b_v)
    min_v = min(r_v, g_v, b_v)

    if max_v == min_v:
        h = 0
    elif max_v == r_v and g_v >= b_v:
        h = 60 * (g_v - b_v) / (max_v - min_v)
    elif max_v == r_v and g_v < b_v:
        h = 60 * (g_v - b_v) / (max_v - min_v) + 360
    elif max_v == g_v:
        h = 60 * (b_v - r_v) / (max_v - min_v) + 120
    else: # max_v == b_v
        h = 60 * (r_v - g_v) / (max_v - min_v) + 240

    l = (max_v + min_v) / 2

    if max_v + min_v == 0 or max_v == min_v:
        s = 0
    elif l <= 0.5:
        s = (max_v - min_v) / (2 * l)
    else: # l > 0.5
        s = (max_v - min_v) / (2 - 2 * l)

    return (h, s, l)

def HSL2RGB(h, s, l):
    assert isinstance(h, (float, int))
    assert isinstance(s, (float, int))
    assert isinstance(l, (float, int))
    assert h >= 0 and h <= 360
    assert s >= 0 and s <= 1
    assert l >= 0 and l <= 1

    if h == 360:
        h = 0

    c = (1 - abs(2 * l - 1)) * s
    h2 = h / 60
    x = c * (1 - abs(h2 % 2 - 1))

    if h2 < 1:
        r1, g1, b1 = c, x, 0
    elif h2 < 2:
        r1, g1, b1 = x, c, 0
    elif h2 < 3:
        r1, g1, b1 = 0, c, x
    elif h2 < 4:
        r1, g1, b1 = 0, x, c
    elif h2 < 5:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    m = l - c / 2
    r = r1 + m
    g = g1 + m
    b = b1 + m

    r = min(round(r * 256), 255)
    g = min(round(g * 256), 255)
    b = min(round(b * 256), 255)

    return (r, g, b)

@check_image_mode(ImageMode.COLOR)
def RGB2HSL_cache(im):
    width = im.size[0]
    height = im.size[1]
    matrix = [[None] * width for _ in range(height)]
    px = canonical_mode(im).load()

    for x in range(width):
        for y in range(height):
            matrix[y][x] = RGB2HSL(*px[x, y])

    return matrix

@check_image_mode(ImageMode.COLOR)
def HSL_adjust(im, *, h_adj = 0, s_adj = 0, l_adj = 0, cache = None):
    assert isinstance(h_adj, (float, int))
    assert isinstance(s_adj, (float, int))
    assert isinstance(l_adj, (float, int))
    assert h_adj >= -180 and h_adj <= 180
    assert s_adj >= -1 and s_adj <= 1
    assert l_adj >= -1 and l_adj <= 1

    new_im = Image.new('RGB', im.size)
    new_px = new_im.load()
    if not cache:
        px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            h, s, l = cache[y][x] if cache else RGB2HSL(*px[x, y])
            h = (h + h_adj) % 360
            s = min(s * 50 ** s_adj, 1)
            l += l_adj * (l if l_adj < 0 else (1 - l))
            new_px[x, y] = HSL2RGB(h, s, l)

    return new_im
