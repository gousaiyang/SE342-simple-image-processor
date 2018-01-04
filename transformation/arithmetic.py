# -*- coding: utf-8 -*-

from PIL import Image

from util import *

@check_image_mode_2
def image_addition(im1, im2):
    mode = get_image_mode(im1)
    new_width = max(im1.size[0], im2.size[0])
    new_height = max(im1.size[1], im2.size[1])

    new_im = Image.new(canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px1 = canonical_mode(im1).load()
    px2 = canonical_mode(im2).load()

    for x in range(new_width):
        for y in range(new_height):
            if mode == ImageMode.COLOR:
                v1r, v1g, v1b = get_px_wrapper_rgb(px1, im1.size, (x, y))
                v2r, v2g, v2b = get_px_wrapper_rgb(px2, im2.size, (x, y))
                new_px[x, y] = (min(v1r + v2r, 255), min(v1g + v2g, 255), min(v1b + v2b, 255))
            else:
                v1 = get_px_wrapper(px1, im1.size, (x, y))
                v2 = get_px_wrapper(px2, im2.size, (x, y))
                new_px[x, y] = min(v1 + v2, 255)

    return new_im

@check_image_mode_2
def image_subtraction(im1, im2):
    mode = get_image_mode(im1)
    new_width = im1.size[0]
    new_height = im1.size[1]

    new_im = Image.new(canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px1 = canonical_mode(im1).load()
    px2 = canonical_mode(im2).load()

    for x in range(new_width):
        for y in range(new_height):
            if mode == ImageMode.COLOR:
                v1r, v1g, v1b = get_px_wrapper_rgb(px1, im1.size, (x, y))
                v2r, v2g, v2b = get_px_wrapper_rgb(px2, im2.size, (x, y))
                new_px[x, y] = (max(v1r - v2r, 0), max(v1g - v2g, 0), max(v1b - v2b, 0))
            else:
                v1 = get_px_wrapper(px1, im1.size, (x, y))
                v2 = get_px_wrapper(px2, im2.size, (x, y))
                new_px[x, y] = max(v1 - v2, 0)

    return new_im

@check_image_mode_2
def image_multiplication(im1, im2):
    mode = get_image_mode(im1)
    new_width = min(im1.size[0], im2.size[0])
    new_height = min(im1.size[1], im2.size[1])

    new_im = Image.new(canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px1 = canonical_mode(im1).load()
    px2 = canonical_mode(im2).load()

    for x in range(new_width):
        for y in range(new_height):
            if mode == ImageMode.COLOR:
                v1r, v1g, v1b = get_px_wrapper_rgb(px1, im1.size, (x, y))
                v2r, v2g, v2b = get_px_wrapper_rgb(px2, im2.size, (x, y))
                new_px[x, y] = (min(round(v1r * v2r / 255), 255), min(round(v1g * v2g / 255), 255),
                    min(round(v1b * v2b / 255), 255))
            else:
                v1 = get_px_wrapper(px1, im1.size, (x, y))
                v2 = get_px_wrapper(px2, im2.size, (x, y))
                new_px[x, y] = min(round(v1 * v2 / 255), 255)

    return new_im

def image_inverse(im):
    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if mode == ImageMode.COLOR:
                r, g, b = px[x, y]
                new_px[x, y] = (255 - r, 255 - g, 255 - b)
            else:
                new_px[x, y] = 255 - px[x, y]

    return new_im

def image_crop(im, left, top, right, bottom):
    width = im.size[0]
    height = im.size[1]

    assert isinstance(left, int)
    assert isinstance(top, int)
    assert isinstance(right, int)
    assert isinstance(bottom, int)
    assert left >= 0 and left < width
    assert top >= 0 and top < height
    assert right >= 0 and right < width
    assert bottom >= 0 and bottom < height
    assert left <= right
    assert top <= bottom

    new_width = right - left
    new_height = bottom - top

    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), (new_width, new_height))
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(new_width):
        for y in range(new_height):
            new_px[x, y] = px[x + left, y + top]

    return new_im
