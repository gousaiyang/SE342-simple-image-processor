# -*- coding: utf-8 -*-

from PIL import Image

from util import *
from i18n import i18n
from .arithmetic import *

@check_image_mode(ImageMode.BINARY)
def check_binary_image(im):
    pass

def check_binary_se(se):
    if not isinstance(se, list):
        return False

    a = len(se)
    b = None

    for item in se:
        if not isinstance(item, list):
            return False

        l = len(item)

        if b is None:
            b = l
        elif b != l:
            return False

        for subitem in item:
            if subitem not in [0, 1, -1]: # -1 stands for "don't care" for hit-and-miss
                return False

    return bool(a % 2) and b is not None and bool(b % 2)

def check_grayscale_se(se):
    if not isinstance(se, list):
        return False

    a = len(se)
    b = None

    for item in se:
        if not isinstance(item, list):
            return False

        l = len(item)

        if b is None:
            b = l
        elif b != l:
            return False

        for subitem in item:
            if subitem not in range(256):
                return False

    return bool(a % 2) and b is not None and bool(b % 2)

def get_se_center(se):
    return (len(se) // 2, len(se[0]) // 2)

binary_se_example = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

@check_image_mode(ImageMode.BINARY)
def binary_dilation(im, se):
    if not check_binary_se(se):
        raise TypeError(i18n['invalid_se'])

    scx, scy = get_se_center(se)

    new_im = Image.new('1', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            found = False
            for i in range(-scx, scx + 1):
                for j in range(-scy, scy + 1):
                    if se[scx + i][scy + j] == 1 and get_px_wrapper(px, im.size, (x + i, y + j)):
                        new_px[x, y] = 255
                        found = True
                        break
                if found:
                    break
            if not found:
                new_px[x, y] = 0

    return new_im

@check_image_mode(ImageMode.BINARY)
def binary_erosion(im, se):
    if not check_binary_se(se):
        raise TypeError(i18n['invalid_se'])

    scx, scy = get_se_center(se)

    new_im = Image.new('1', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            found = False
            for i in range(-scx, scx + 1):
                for j in range(-scy, scy + 1):
                    if se[scx + i][scy + j] == 1 and not get_px_wrapper(px, im.size, (x + i, y + j)):
                        new_px[x, y] = 0
                        found = True
                        break
                if found:
                    break
            if not found:
                new_px[x, y] = 255

    return new_im

@check_image_mode(ImageMode.BINARY)
def binary_opening(im, se):
    return binary_dilation(binary_erosion(im, se), se)

@check_image_mode(ImageMode.BINARY)
def binary_closing(im, se):
    return binary_erosion(binary_dilation(im, se), se)

@check_image_mode(ImageMode.BINARY)
def binary_hit_and_miss(im, se):
    if not check_binary_se(se):
        raise TypeError(i18n['invalid_se'])

    scx, scy = get_se_center(se)

    new_im = Image.new('1', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            found = False
            for i in range(-scx, scx + 1):
                for j in range(-scy, scy + 1):
                    v = get_px_wrapper(px, im.size, (x + i, y + j))
                    s = se[scx + i][scy + j]
                    if (s == 1 and not v) or (s == 0 and v):
                        new_px[x, y] = 0
                        found = True
                        break
                if found:
                    break
            if not found:
                new_px[x, y] = 255

    return new_im

binary_thinning_se_example = [[0, 0, 0], [-1, 1, -1], [1, 1, 1]]

@check_image_mode(ImageMode.BINARY)
def binary_thinning(im, se):
    return image_subtraction(im, binary_hit_and_miss(im, se))

binary_thickening_se_example = [[1, 1, -1], [1, 0, -1], [1, -1, 0]]

@check_image_mode(ImageMode.BINARY)
def binary_thickening(im, se):
    return image_addition(im, binary_hit_and_miss(im, se))

@check_image_mode(ImageMode.BINARY)
def binary_empty(im):
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if px[x, y]:
                return False

    return True

def binary_create_empty(size):
    new_im = Image.new('1', size)
    new_px = new_im.load()

    for x in range(size[0]):
        for y in range(size[1]):
            new_px[x, y] = 0

    return new_im

@check_image_mode(ImageMode.BINARY)
def binary_distance_transform(im):
    new_im = Image.new('L', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    width = im.size[0]
    height = im.size[1]
    matrix = [[None] * height for _ in range(width)]

    for x in range(width):
        for y in range(height):
            matrix[x][y] = int(bool(px[x, y]))

    max_v = 0

    updating = True
    while updating:
        updating = False
        for x in range(width):
            for y in range(height):
                v_old = matrix[x][y]
                if v_old > max_v:
                    max_v = v_old
                if v_old:
                    p1 = matrix[x - 1][y] if x > 0 else 255
                    p2 = matrix[x + 1][y] if x < width - 1 else 255
                    p3 = matrix[x][y - 1] if y > 0 else 255
                    p4 = matrix[x][y + 1] if y < height - 1 else 255
                    v_new = min(min(p1, p2, p3, p3) + 1, 255)
                    if v_new != v_old:
                        updating = True
                    matrix[x][y] = v_new

    for x in range(width):
        for y in range(height):
            new_px[x, y] = round(matrix[x][y] * 255 / max_v) # scaling

    return new_im

binary_simple_se_example = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

skeleton_last_sts = []
skeleton_last_se = None
skeleton_last_size = None

@check_image_mode(ImageMode.BINARY)
def binary_skeletonization(im, se):
    ret_im = im
    et = im

    global skeleton_last_sts, skeleton_last_se, skeleton_last_size
    skeleton_last_sts = []
    skeleton_last_se = se
    skeleton_last_size = im.size

    while True:
        et = binary_erosion(et, se)
        if binary_empty(et):
            break
        st = image_subtraction(et, binary_opening(et, se))
        skeleton_last_sts.append(st)
        ret_im = image_addition(ret_im, st)

    return ret_im

def binary_skeleton_done():
    return bool(skeleton_last_se)

def binary_skeleton_reconstruct():
    if not binary_skeleton_done():
        return

    ret_im = binary_create_empty(skeleton_last_size)

    for k, st in enumerate(skeleton_last_sts):
        et = st

        for i in range(k):
            et = binary_dilation(et, skeleton_last_se)

        ret_im = image_addition(ret_im, et)

    return ret_im

def binary_equal(im1, im2):
    if im1.size != im2.size:
        return False

    px1 = canonical_mode(im1).load()
    px2 = canonical_mode(im2).load()

    for x in range(im1.size[0]):
        for y in range(im1.size[1]):
            if px1[x, y] != px2[x, y]:
                return False

    return True

def binary_morph_reconstruct(img, imf, se, *, dilation):
    if get_image_mode(imf) != ImageMode.BINARY:
        raise TypeError(i18n['some_image_mode_expected'] % i18n['binary'])
    if get_image_mode(img) != ImageMode.BINARY:
        raise TypeError(i18n['some_image_mode_expected'] % i18n['binary'])
    if not check_binary_se(se):
        raise TypeError(i18n['invalid_se'])

    imd = imf

    while True:
        imd_old = imd
        if dilation:
            imd = image_multiplication(binary_dilation(imd, se), img)
        else:
            imd = image_addition(binary_erosion(imd, se), img)
        if binary_equal(imd_old, imd):
            break

    return imd

grayscale_se_example = [[10, 10, 10], [10, 10, 10], [10, 10, 10]]

@check_image_mode(ImageMode.GRAYSCALE)
def grayscale_dilation(im, se):
    if not check_grayscale_se(se):
        raise TypeError(i18n['invalid_se'])

    scx, scy = get_se_center(se)

    new_im = Image.new('L', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            max_v = 0

            for i in range(-scx, scx + 1):
                for j in range(-scy, scy + 1):
                    v = min(se[scx + i][scy + j] + get_px_wrapper(px, im.size, (x - i, y - j)), 255)
                    if v > max_v:
                        max_v = v

            new_px[x, y] = max_v

    return new_im

@check_image_mode(ImageMode.GRAYSCALE)
def grayscale_erosion(im, se):
    if not check_grayscale_se(se):
        raise TypeError(i18n['invalid_se'])

    scx, scy = get_se_center(se)

    new_im = Image.new('L', im.size)
    new_px = new_im.load()
    px = canonical_mode(im).load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            min_v = 256

            for i in range(-scx, scx + 1):
                for j in range(-scy, scy + 1):
                    v = max(get_px_wrapper(px, im.size, (x + i, y + j)) - se[scx + i][scy + j], 0)
                    if v < min_v:
                        min_v = v

            new_px[x, y] = min_v

    return new_im

@check_image_mode(ImageMode.GRAYSCALE)
def grayscale_opening(im, se):
    return grayscale_dilation(grayscale_erosion(im, se), se)

@check_image_mode(ImageMode.GRAYSCALE)
def grayscale_closing(im, se):
    return grayscale_erosion(grayscale_dilation(im, se), se)

def grayscale_min(im1, im2):
    new_width = min(im1.size[0], im2.size[0])
    new_height = min(im1.size[1], im2.size[1])

    new_im = Image.new('L', (new_width, new_height))
    new_px = new_im.load()
    px1 = canonical_mode(im1).load()
    px2 = canonical_mode(im2).load()

    for x in range(new_width):
        for y in range(new_height):
            new_px[x, y] = min(px1[x, y], px2[x, y])

    return new_im

def grayscale_max(im1, im2):
    new_width = max(im1.size[0], im2.size[0])
    new_height = max(im1.size[1], im2.size[1])

    new_im = Image.new('L', (new_width, new_height))
    new_px = new_im.load()
    px1 = canonical_mode(im1).load()
    px2 = canonical_mode(im2).load()

    for x in range(new_width):
        for y in range(new_height):
            v1 = get_px_wrapper(px1, im1.size, (x, y))
            v2 = get_px_wrapper(px2, im2.size, (x, y))
            new_px[x, y] = max(v1, v2)

    return new_im

def grayscale_morph_reconstruct(img, imf, se, *, dilation):
    if get_image_mode(imf) != ImageMode.GRAYSCALE:
        raise TypeError(i18n['some_image_mode_expected'] % i18n['grayscale'])
    if get_image_mode(img) != ImageMode.GRAYSCALE:
        raise TypeError(i18n['some_image_mode_expected'] % i18n['grayscale'])
    if not check_grayscale_se(se):
        raise TypeError(i18n['invalid_se'])

    imd = imf

    while True:
        imd_old = imd
        if dilation:
            imd = grayscale_min(grayscale_dilation(imd, se), img)
        else:
            imd = grayscale_max(grayscale_erosion(imd, se), img)
        if binary_equal(imd_old, imd):
            break

    return imd
