# -*- coding: utf-8 -*-

from PIL import Image

from util import *

def scaling_nearest(im, *, x_scale = 1, y_scale = 1):
    assert isinstance(x_scale, (float, int))
    assert isinstance(y_scale, (float, int))
    assert x_scale > 0
    assert y_scale > 0

    mode = get_image_mode(im)
    new_width = round(im.size[0] * x_scale)
    new_height = round(im.size[1] * y_scale)

    new_im = Image.new(canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(new_width):
        for y in range(new_height):
            new_px[x, y] = px[x // x_scale, y // y_scale]

    return new_im

def scaling_bilinear(im, *, x_scale = 1, y_scale = 1):
    assert isinstance(x_scale, (float, int))
    assert isinstance(y_scale, (float, int))
    assert x_scale > 0
    assert y_scale > 0

    mode = get_image_mode(im)
    new_width = round(im.size[0] * x_scale)
    new_height = round(im.size[1] * y_scale)

    new_im = Image.new(canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(new_width):
        for y in range(new_height):
            i = x // x_scale
            u = x / x_scale - i
            j = y // y_scale
            v = y / y_scale - j
            c1 = (1 - u) * (1 - v)
            c2 = (1 - u) * v
            c3 = u * (1 - v)
            c4 = u * v
            p1 = px[i, j]
            p2 = px[i, j + 1] if point_in_image((i, j + 1), im.size) else p1
            p3 = px[i + 1, j] if point_in_image((i + 1, j), im.size) else p1
            p4 = px[i + 1, j + 1] if point_in_image((i + 1, j + 1), im.size) else p1
            if mode == ImageMode.COLOR:
                r1, g1, b1 = p1
                r2, g2, b2 = p2
                r3, g3, b3 = p3
                r4, g4, b4 = p4
                new_r = round(c1 * r1 + c2 * r2 + c3 * r3 + c4 * r4)
                new_g = round(c1 * g1 + c2 * g2 + c3 * g3 + c4 * g4)
                new_b = round(c1 * b1 + c2 * b2 + c3 * b3 + c4 * b4)
                new_px[x, y] = (new_r, new_g, new_b)
            else:
                new_px[x, y] = round(c1 * p1 + c2 * p2 + c3 * p3 + c4 * p4)

    return new_im
