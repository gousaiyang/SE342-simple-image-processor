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
        self.w1 = 200
        self.w2 = 5

    def init_widgets(self):
        self.h_label = ttk.Label(self.window, text = i18n['H'])
        self.h_label.place(x = self.x1, y = self.y1)
        self.h_scale_var = tk.DoubleVar()
        self.h_scale_var.set(0)
        self.h_scale = ttk.Scale(self.window, from_ = -180, to = 180, length = self.w1, variable = self.h_scale_var,
            command = self.on_h_scale_change)
        self.h_scale.place(x = self.x2, y = self.y1)
        self.h_entry_var = tk.StringVar()
        self.h_entry_var.set('0')
        self.h_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.h_entry_var)
        self.h_entry.bind('<Return>', self.on_h_entry_change)
        self.h_entry.place(x = self.x3, y = self.y1)

        self.s_label = ttk.Label(self.window, text = i18n['S'])
        self.s_label.place(x = self.x1, y = self.y2)
        self.s_scale_var = tk.DoubleVar()
        self.s_scale_var.set(0)
        self.s_scale = ttk.Scale(self.window, from_ = -100, to = 100, length = self.w1, variable = self.s_scale_var,
            command = self.on_s_scale_change)
        self.s_scale.place(x = self.x2, y = self.y2)
        self.s_entry_var = tk.StringVar()
        self.s_entry_var.set('0')
        self.s_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.s_entry_var)
        self.s_entry.bind('<Return>', self.on_s_entry_change)
        self.s_entry.place(x = self.x3, y = self.y2)

        self.l_label = ttk.Label(self.window, text = i18n['L'])
        self.l_label.place(x = self.x1, y = self.y3)
        self.l_scale_var = tk.DoubleVar()
        self.l_scale_var.set(0)
        self.l_scale = ttk.Scale(self.window, from_ = -100, to = 100, length = self.w1, variable = self.l_scale_var,
            command = self.on_l_scale_change)
        self.l_scale.place(x = self.x2, y = self.y3)
        self.l_entry_var = tk.StringVar()
        self.l_entry_var.set('0')
        self.l_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.l_entry_var)
        self.l_entry.bind('<Return>', self.on_l_entry_change)
        self.l_entry.place(x = self.x3, y = self.y3)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        self.parent.im = transformation.HSL_adjust(self.old_im, h_adj = self.new_h, s_adj = self.new_s / 100,
            l_adj = self.new_l / 100, cache = self.cache)

    def on_h_entry_change(self, event = None):
        try:
            h = float(self.h_entry_var.get())
            assert h >= -180 and h <= 180
            self.new_h = h
        except:
            pass
        else:
            self.h_scale_var.set(self.new_h)
            self.update_image_show()
        finally:
            self.h_entry_var.set(display_adjust_value(self.new_h))

    def on_h_scale_change(self, event = None):
        self.new_h = self.h_scale_var.get()
        self.h_entry_var.set(display_adjust_value(self.new_h))
        self.update_image_show()

    def on_s_entry_change(self, event = None):
        try:
            s = float(self.s_entry_var.get())
            assert s >= -100 and s <= 100
            self.new_s = s
        except:
            pass
        else:
            self.s_scale_var.set(self.new_s)
            self.update_image_show()
        finally:
            self.s_entry_var.set(display_adjust_value(self.new_s))

    def on_s_scale_change(self, event = None):
        self.new_s = self.s_scale_var.get()
        self.s_entry_var.set(display_adjust_value(self.new_s))
        self.update_image_show()

    def on_l_entry_change(self, event = None):
        try:
            l = float(self.l_entry_var.get())
            assert l >= -100 and l <= 100
            self.new_l = l
        except:
            pass
        else:
            self.l_scale_var.set(self.new_l)
            self.update_image_show()
        finally:
            self.l_entry_var.set(display_adjust_value(self.new_l))

    def on_l_scale_change(self, event = None):
        self.new_l = self.l_scale_var.get()
        self.l_entry_var.set(display_adjust_value(self.new_l))
        self.update_image_show()

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
