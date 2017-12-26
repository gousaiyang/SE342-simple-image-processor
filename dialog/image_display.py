# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from util import *

class ImageDisplayFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        self.frame_upper = ttk.Frame(self.frame)
        self.frame_lower = ttk.Frame(self.frame)

        self.canvas = tk.Canvas(self.frame_upper, highlightthickness = 0)
        self.scroll_v = ttk.Scrollbar(self.frame_upper, orient = tk.VERTICAL)
        self.scroll_v.config(command = self.canvas.yview)
        self.scroll_h = ttk.Scrollbar(self.frame_lower, orient = tk.HORIZONTAL)
        self.scroll_h.config(command = self.canvas.xview)
        self.sizegrip = ttk.Sizegrip(self.frame_lower)
        self.canvas.config(xscrollcommand = self.scroll_h.set, yscrollcommand = self.scroll_v.set)
        self.canvas.bind('<Configure>', self.on_resize_canvas)

        self.image_frame = ttk.Frame(self.canvas)
        self.image_window = self.canvas.create_window(0, 0, window = self.image_frame, anchor = tk.NW)
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.bind('<Motion>', self.on_mouse_move)

        self.im = None
        self.imagetk = None
        self.scrollbar_info = None
        self.cursor_pos = None

    def pack_components(self, scrollbar_info):
        if self.scrollbar_info != scrollbar_info:
            self.scrollbar_info = scrollbar_info

            self.pack_forget_components()

            self.frame_upper.pack(fill = tk.BOTH, expand = 1)
            if scrollbar_info[1]:
                self.scroll_v.pack(side = tk.RIGHT, fill = tk.Y, expand = 0)
            self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
            if scrollbar_info[0]:
                self.frame_lower.pack(fill = tk.X, expand = 0)
                if scrollbar_info[1]:
                    self.sizegrip.pack(side = tk.RIGHT)
                self.scroll_h.pack(side = tk.BOTTOM, fill = tk.X, expand = 0)
            self.image_label.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

    def pack_forget_components(self):
        try_pack_forget(self.sizegrip)
        try_pack_forget(self.scroll_h)
        try_pack_forget(self.frame_lower)
        try_pack_forget(self.scroll_v)
        try_pack_forget(self.image_label)
        try_pack_forget(self.canvas)
        try_pack_forget(self.frame_upper)

    def pack(self, *args, **kw):
        self.frame.pack(*args, **kw)
        self.pack_components((True, True))

    def pack_forget(self):
        self.pack_forget_components()
        self.frame.pack_forget()
        self.scrollbar_info = None

    def update_size(self):
        canvas_size = get_window_size(self.canvas)
        image_size = self.im.size if self.im else (0, 0)
        self.pack_components((image_size[0] > canvas_size[0], image_size[1] > canvas_size[1]))
        canvas_size = get_window_size(self.canvas)
        new_canvas_scroll_size = max_rect_2(canvas_size, image_size)
        self.canvas.config(scrollregion = (0, 0) + new_canvas_scroll_size)
        self.image_frame.config(width = new_canvas_scroll_size[0], height = new_canvas_scroll_size[1])

    def update_image(self, im):
        self.im = im
        self.update_size()
        self.imagetk = ImageTk.PhotoImage(self.im)
        self.image_label.config(image = self.imagetk)
        self.canonical_im = canonical_mode(self.im)
        self.px = self.canonical_im.load()

    def on_resize_canvas(self, event):
        self.update_size()

    def on_mouse_move(self, event):
        self.cursor_pos = (event.x, event.y)

    @property
    def cursor_value(self):
        try:
            return self.px[self.cursor_pos]
        except:
            return None

    @property
    def image_rect(self):
        return get_window_rect(self.image_label)
