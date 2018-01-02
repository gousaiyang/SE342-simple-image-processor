# -*- coding: utf-8 -*-

from PIL import Image

from util import *

@check_image_mode(ImageMode.GRAYSCALE)
def grayscale_histogram(im):
    histogram = [0] * 256
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            histogram[px[x, y]] += 1

    return histogram

@check_image_mode(ImageMode.GRAYSCALE)
def otsu(im):
    new_im = Image.new('1', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    histogram = grayscale_histogram(im)
    total = im.size[0] * im.size[1]

    sum_v = 0
    for i in range(1, 256):
        sum_v += i * histogram[i]
    sumB = 0
    wB = 0
    wF = 0
    max_v = 0.0
    between = 0.0
    threshold1 = 0.0
    threshold2 = 0.0
    for i in range(256):
        wB += histogram[i]
        if wB == 0:
            continue
        wF = total - wB
        if wF == 0:
            break
        sumB += i * histogram[i]
        mB = sumB / wB
        mF = (sum_v - sumB) / wF
        between = wB * wF * (mB - mF) * (mB - mF)
        if between >= max_v:
            threshold1 = i
            if between > max_v:
                threshold2 = i
            max_v = between

    threshold = (threshold1 + threshold2) / 2

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            new_px[x, y] = 255 if px[x, y] >= threshold else 0

    return new_im
