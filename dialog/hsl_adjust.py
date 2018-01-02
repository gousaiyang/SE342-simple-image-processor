# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

import transformation
from util import *
from i18n import i18n

def display_adjust_value(value):
    v = round(value)
    return '0' if v == 0 else '%+d' % (v)

class HSLAdjustDialog:
    def __init__(self, parent):
        self.init_state(parent)
        self.init_window()
        self.init_coords()
        self.init_widgets()

    def init_state(self, parent):
        self.parent = parent
        self.old_im = parent.im
        self.cache = transformation.RGB2HSL_cache(self.old_im)
        self.new_h = 0
        self.new_s = 0
        self.new_l = 0
        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(i18n['HSL_adjusting'])
        self.window.geometry('340x180')
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.window.bind('<Return>', self.on_apply)
        self.window.bind('<Escape>', self.on_cancel)
        center_window(self.window)
        self.window.grab_set()

    def init_coords(self):
        self.x1 = 20
        self.x2 = 80
        self.x3 = 285
        self.bottom_x1 = 77
        self.bottom_x2 = 177
        self.yd = 30
        self.y1 = 20
        self.y2 = self.y1 + self.yd
        self.y3 = self.y1 + self.yd * 2
        self.bottom_y = 130
        self.w = 200

    def init_widgets(self):
        self.h_label = ttk.Label(self.window, text = i18n['H'])
        self.h_label.place(x = self.x1, y = self.y1)
        self.h_scale = ttk.Scale(self.window, from_ = -180, to = 180, length = self.w, command = self.on_h_change)
        self.h_scale.place(x = self.x2, y = self.y1)
        self.h_value_label = ttk.Label(self.window, text = '0')
        self.h_value_label.place(x = self.x3, y = self.y1)

        self.s_label = ttk.Label(self.window, text = i18n['S'])
        self.s_label.place(x = self.x1, y = self.y2)
        self.s_scale = ttk.Scale(self.window, from_ = -100, to = 100, length = self.w, command = self.on_s_change)
        self.s_scale.place(x = self.x2, y = self.y2)
        self.s_value_label = ttk.Label(self.window, text = '0')
        self.s_value_label.place(x = self.x3, y = self.y2)

        self.l_label = ttk.Label(self.window, text = i18n['L'])
        self.l_label.place(x = self.x1, y = self.y3)
        self.l_scale = ttk.Scale(self.window, from_ = -100, to = 100, length = self.w, command = self.on_l_change)
        self.l_scale.place(x = self.x2, y = self.y3)
        self.l_value_label = ttk.Label(self.window, text = '0')
        self.l_value_label.place(x = self.x3, y = self.y3)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def on_h_change(self, event = None):
        self.new_h = float(event)
        self.h_value_label.config(text = display_adjust_value(self.new_h))
        self.parent.im = transformation.HSL_adjust(self.old_im, h_adj = self.new_h, cache = self.cache)

    def on_s_change(self, event = None):
        self.new_s = float(event)
        self.s_value_label.config(text = display_adjust_value(self.new_s))
        self.parent.im = transformation.HSL_adjust(self.old_im, s_adj = self.new_s / 100, cache = self.cache)

    def on_l_change(self, event = None):
        self.new_l = float(event)
        self.l_value_label.config(text = display_adjust_value(self.new_l))
        self.parent.im = transformation.HSL_adjust(self.old_im, l_adj = self.new_l / 100, cache = self.cache)

    def on_apply(self, event = None):
        self.apply = True
        self.window.quit()
        self.window.destroy()

    def on_cancel(self, event = None):
        self.apply = False
        self.window.quit()
        self.window.destroy()

    def __call__(self):
        self.window.mainloop()
