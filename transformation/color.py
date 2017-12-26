from util import *
from i18n import i18n

def get_band(im, band):
    bd = band.lower()
    if bd not in ['r', 'g', 'b']:
        raise ValueError(i18n['invalid_band'])

    if get_image_mode(im) != ImageMode.COLOR:
        raise TypeError(i18n['color_image_expected'])

    return (im if is_rgb_mode(im) else im.convert('RGB')).split()[{'r': 0, 'g': 1, 'b': 2}[bd]]
