# -*- coding: utf-8 -*-

from math import radians, sin, cos
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

def rotate_point(p, a):
    x = p[0]
    y = p[1]
    ca = cos(a)
    sa = sin(a)
    return (x * ca - y * sa, y * ca + x * sa)

def rotate_point_inverse(p, a):
    x = p[0]
    y = p[1]
    ca = cos(a)
    sa = sin(a)
    return (x * ca + y * sa, y * ca - x * sa)

def rotate_rect_info(size, a):
    w = size[0]
    h = size[1]
    p0 = (0, 0)
    p1 = (w, 0)
    p2 = (w, h)
    p3 = (0, h)
    p0r = rotate_point(p0, a)
    p1r = rotate_point(p1, a)
    p2r = rotate_point(p2, a)
    p3r = rotate_point(p3, a)
    max_x = max(p0r[0], p1r[0], p2r[0], p3r[0])
    min_x = min(p0r[0], p1r[0], p2r[0], p3r[0])
    max_y = max(p0r[1], p1r[1], p2r[1], p3r[1])
    min_y = min(p0r[1], p1r[1], p2r[1], p3r[1])
    new_w = max_x - min_x
    new_h = max_y - min_y
    return (round(new_w), round(new_h), min_x, min_y)

def rotation_nearest(im, *, degree = 0):
    assert isinstance(degree, (float, int))
    assert degree >= -180 and degree <= 180

    a = radians(degree)
    new_width, new_height, x_shift, y_shift = rotate_rect_info(im.size, a)
    mode = get_image_mode(im)

    new_im = Image.new('RGBA' if mode == ImageMode.COLOR else canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(new_width):
        for y in range(new_height):
            pox, poy = rotate_point_inverse((x + x_shift, y + y_shift), a)
            if mode == ImageMode.COLOR:
                new_px[x, y] = get_px_wrapper_rgba(px, im.size, (int(pox), int(poy)))
            else:
                new_px[x, y] = get_px_wrapper(px, im.size, (int(pox), int(poy)))

    return new_im

def rotation_bilinear(im, *, degree = 0):
    assert isinstance(degree, (float, int))
    assert degree >= -180 and degree <= 180

    a = radians(degree)
    new_width, new_height, x_shift, y_shift = rotate_rect_info(im.size, a)
    mode = get_image_mode(im)

    new_im = Image.new('RGBA' if mode == ImageMode.COLOR else canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(new_width):
        for y in range(new_height):
            pox, poy = rotate_point_inverse((x + x_shift, y + y_shift), a)

            i = int(pox)
            u = pox - i
            j = int(poy)
            v = poy - j
            c1 = (1 - u) * (1 - v)
            c2 = (1 - u) * v
            c3 = u * (1 - v)
            c4 = u * v

            if mode == ImageMode.COLOR:
                p1 = get_px_wrapper_rgb(px, im.size, (i, j))
            else:
                p1 = get_px_wrapper(px, im.size, (i, j))

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
                alpha = 255 if point_in_image((i, j), im.size) else 0
                new_px[x, y] = (new_r, new_g, new_b, alpha)
            else:
                new_px[x, y] = round(c1 * p1 + c2 * p2 + c3 * p3 + c4 * p4)

    return new_im
