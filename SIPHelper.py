# -*- coding: utf-8 -*-

import platform

is_windows = platform.system() == 'Windows'

def max_rect_2(rect1, rect2):
    return (max(rect1[0], rect2[0]), max(rect1[1], rect2[1]))

def get_window_size(window):
    window.update_idletasks()
    return window.winfo_width(), window.winfo_height()

def center_window(window):
    size = get_window_size(window)
    pos = (window.winfo_screenwidth() - size[0]) // 2, (window.winfo_screenheight() - size[1]) // 2
    window.geometry("%dx%d+%d+%d" % (size + pos))

def native_path_format(path):
    return path.replace('/', '\\') if is_windows else path
