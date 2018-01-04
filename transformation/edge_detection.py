# -*- coding: utf-8 -*-

from PIL import Image

from util import *
from .arithmetic import image_addition
from .filter import do_filter

sobel_horizontal_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobel_vertical_kernel = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

def sobel(im):
    imx = do_filter(im, sobel_horizontal_kernel)
    imy = do_filter(im, sobel_vertical_kernel)
    return image_addition(imx, imy)

laplacian_kernel = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

def laplacian(im):
    return do_filter(im, laplacian_kernel)
