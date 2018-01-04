# -*- coding: utf-8 -*-

import math
from PIL import Image

from util import *

def check_kernel(kernel):
    if not isinstance(kernel, list):
        return False

    a = len(kernel)

    for item in kernel:
        if not isinstance(item, list):
            return False
        if len(item) != a:
            return False
        for subitem in item:
            if not isinstance(subitem, (float, int)):
                return False

    return bool(a % 2)

def get_kernel_width(kernel):
    return len(kernel) // 2

def smooth_filter(im, kernel):
    if not check_kernel(kernel):
        raise TypeError(i18n['invalid_kernel'])

    kw = get_kernel_width(kernel)

    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if mode == ImageMode.COLOR:
                sr = 0
                sg = 0
                sb = 0
                for i in range(-kw, kw + 1):
                    for j in range(-kw, kw + 1):
                        r, g, b = get_px_wrapper_rgb(px, im.size, (x + i, y + j))
                        sr += r * kernel[kw + i][kw + j]
                        sg += g * kernel[kw + i][kw + j]
                        sb += b * kernel[kw + i][kw + j]
                sr = max(min(round(sr), 255), 0)
                sg = max(min(round(sg), 255), 0)
                sb = max(min(round(sb), 255), 0)
                new_px[x, y] = (sr, sg, sb)
            else:
                s = 0
                for i in range(-kw, kw + 1):
                    for j in range(-kw, kw + 1):
                        s += get_px_wrapper(px, im.size, (x + i, y + j)) * kernel[kw + i][kw + j]
                new_px[x, y] = max(min(round(s), 255), 0)

    return new_im

average_filter_kernel = [[1 / 9] * 3] * 3

def average_filter(im):
    return smooth_filter(im, average_filter_kernel)

def median_9(x1, x2, x3, x4, x5, x6, x7, x8, x9):
    li = [x1, x2, x3, x4, x5, x6, x7, x8, x9]
    li.sort()
    return li[4]

def median_filter(im):
    mode = get_image_mode(im)
    new_im = Image.new(canonical_mode_name(mode), im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if mode == ImageMode.COLOR:
                r1, g1, b1 = get_px_wrapper_rgb(px, im.size, (x - 1, y - 1))
                r2, g2, b2 = get_px_wrapper_rgb(px, im.size, (x, y - 1))
                r3, g3, b3 = get_px_wrapper_rgb(px, im.size, (x + 1, y - 1))
                r4, g4, b4 = get_px_wrapper_rgb(px, im.size, (x - 1, y))
                r5, g5, b5 = get_px_wrapper_rgb(px, im.size, (x, y))
                r6, g6, b6 = get_px_wrapper_rgb(px, im.size, (x + 1, y))
                r7, g7, b7 = get_px_wrapper_rgb(px, im.size, (x - 1, y + 1))
                r8, g8, b8 = get_px_wrapper_rgb(px, im.size, (x, y + 1))
                r9, g9, b9 = get_px_wrapper_rgb(px, im.size, (x + 1, y + 1))
                nr = round(median_9(r1, r2, r3, r4, r5, r6, r7, r8, r9))
                ng = round(median_9(g1, g2, g3, g4, g5, g6, g7, g8, g9))
                nb = round(median_9(b1, b2, b3, b4, b5, b6, b7, b8, b9))
                new_px[x, y] = (nr, ng, nb)
            else:
                x1 = get_px_wrapper(px, im.size, (x - 1, y - 1))
                x2 = get_px_wrapper(px, im.size, (x, y - 1))
                x3 = get_px_wrapper(px, im.size, (x + 1, y - 1))
                x4 = get_px_wrapper(px, im.size, (x - 1, y))
                x5 = get_px_wrapper(px, im.size, (x, y))
                x6 = get_px_wrapper(px, im.size, (x + 1, y))
                x7 = get_px_wrapper(px, im.size, (x - 1, y + 1))
                x8 = get_px_wrapper(px, im.size, (x, y + 1))
                x9 = get_px_wrapper(px, im.size, (x + 1, y + 1))
                new_px[x, y] = round(median_9(x1, x2, x3, x4, x5, x6, x7, x8, x9))

    return new_im

def gaussian_kernel(kw, stdv):
    kernel = [[0] * (2 * kw + 1) for _ in range(2 * kw + 1)]
    s = 0

    for i in range(-kw, kw + 1):
        for j in range(-kw, kw + 1):
            v = math.e ** (-(i ** 2 + j ** 2) / (2 * stdv ** 2))
            s += v
            kernel[kw + i][kw + j] = v

    for i in range(-kw, kw + 1):
        for j in range(-kw, kw + 1):
            kernel[kw + i][kw + j] /= s

    return kernel

def gaussian_filter(im, kw, stdv):
    return smooth_filter(im, gaussian_kernel(kw, stdv))

sharpen_filter_kernel = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
