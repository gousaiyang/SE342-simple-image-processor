# -*- coding: utf-8 -*-

def max_rect_2(rect1, rect2):
    return (max(rect1[0], rect2[0]), max(rect1[1], rect2[1]))

def point_in_rect(p, rect):
    return p[0] >= rect[0] and p[0] <= rect[2] and p[1] >= rect[1] and p[1] <= rect[3]

def get_window_size(window):
    window.update_idletasks()
    return window.winfo_width(), window.winfo_height()

def center_window(window):
    size = get_window_size(window)
    pos = (window.winfo_screenwidth() - size[0]) // 2, (window.winfo_screenheight() - size[1]) // 2
    window.geometry('%dx%d+%d+%d' % (size + pos))

def cursor_pos_toplevel(window):
    cursor_pos = window.winfo_pointerxy()
    return (cursor_pos[0] - window.winfo_rootx(), cursor_pos[1] - window.winfo_rooty())

def get_window_rect(window):
    size = get_window_size(window)
    toplevel = window.winfo_toplevel()
    nw_corner = (window.winfo_rootx() - toplevel.winfo_rootx(), window.winfo_rooty() - toplevel.winfo_rooty())
    return nw_corner + (nw_corner[0] + size[0], nw_corner[1] + size[1])

def try_pack_forget(window):
    if window.winfo_manager() == 'pack':
        window.pack_forget()
