# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from transformation import ContrastMode, contrast_linear, contrast_piecewise, contrast_logarithmic, contrast_exponential
from util import *
from i18n import i18n

def display_1000(v):
    return '%.3f' % (v / 1000)

class ContrastDialog:
    def __init__(self, parent, contrast_mode, contrast_mode_name):
        self.init_state(parent, contrast_mode, contrast_mode_name)
        self.init_window()
        self.init_coords()
        self.init_widgets()
        if not self.p4:
            self.update_image_show()

    def init_state(self, parent, contrast_mode, contrast_mode_name):
        self.parent = parent
        self.contrast_mode = contrast_mode
        self.contrast_mode_name = contrast_mode_name
        self.old_im = parent.im
        self.p4 = contrast_mode in [ContrastMode.LINEAR, ContrastMode.PIECEWISE_LINEAR]

        if contrast_mode == ContrastMode.LINEAR:
            self.a = 0
            self.a_min = 0
            self.a_max = 256
            self.b = 256
            self.b_min = 0
            self.b_max = 256
            self.c = 0
            self.c_min = 0
            self.c_max = 256
            self.d = 256
            self.d_min = 0
            self.d_max = 256
        elif contrast_mode == ContrastMode.PIECEWISE_LINEAR:
            self.a = 0
            self.a_min = 0
            self.a_max = 255
            self.b = 255
            self.b_min = 0
            self.b_max = 255
            self.c = 0
            self.c_min = 0
            self.c_max = 255
            self.d = 255
            self.d_min = 0
            self.d_max = 255
        elif contrast_mode == ContrastMode.LOGARITHMIC:
            self.a = 0
            self.a_min = 0
            self.a_max = 255
            self.b = 50
            self.b_min = 0
            self.b_max = 100
        else:
            self.a = 0
            self.a_min = 0
            self.a_max = 255
            self.b = 1050
            self.b_min = 1000
            self.b_max = 1100

        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(i18n['contrast_adjust'] + ' - ' + self.contrast_mode_name)
        self.window.geometry('340x%d' % (210 if self.p4 else 150))
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.window.bind('<Escape>', self.on_cancel)
        center_window(self.window)
        self.window.grab_set()

    def init_coords(self):
        self.x1 = 10
        self.x2 = 80
        self.x3 = 285
        self.bottom_x1 = 77
        self.bottom_x2 = 177
        self.yd = 30
        self.y1 = 20
        self.y2 = self.y1 + self.yd
        self.y3 = self.y1 + self.yd * 2
        self.y4 = self.y1 + self.yd * 3
        self.bottom_y = 70 + self.yd * (3 if self.p4 else 1)
        self.w1 = 200
        self.w2 = 5

    def init_widgets(self):
        self.a_label = ttk.Label(self.window, text = i18n['a'])
        self.a_label.place(x = self.x1, y = self.y1)
        self.a_scale_var = tk.IntVar()
        self.a_scale_var.set(self.a)
        self.a_scale = ttk.Scale(self.window, from_ = self.a_min, to = self.a_max, length = self.w1,
            variable = self.a_scale_var, command = self.on_a_scale_change)
        self.a_scale.place(x = self.x2, y = self.y1)
        self.a_entry_var = tk.StringVar()
        self.a_entry_var.set(str(self.a))
        self.a_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.a_entry_var)
        self.a_entry.bind('<Return>', self.on_a_entry_change)
        self.a_entry.place(x = self.x3, y = self.y1)

        self.b_label = ttk.Label(self.window, text = i18n['b'])
        self.b_label.place(x = self.x1, y = self.y2)
        self.b_scale_var = tk.IntVar()
        self.b_scale_var.set(self.b)
        self.b_scale = ttk.Scale(self.window, from_ = self.b_min, to = self.b_max, length = self.w1,
            variable = self.b_scale_var, command = self.on_b_scale_change)
        self.b_scale.place(x = self.x2, y = self.y2)
        self.b_entry_var = tk.StringVar()
        if self.contrast_mode == ContrastMode.EXPONENTIAL:
            self.b_entry_var.set(display_1000(self.b))
        else:
            self.b_entry_var.set(str(self.b))
        self.b_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.b_entry_var)
        self.b_entry.bind('<Return>', self.on_b_entry_change)
        self.b_entry.place(x = self.x3, y = self.y2)

        if self.p4:
            self.c_label = ttk.Label(self.window, text = i18n['c'])
            self.c_label.place(x = self.x1, y = self.y3)
            self.c_scale_var = tk.IntVar()
            self.c_scale_var.set(self.c)
            self.c_scale = ttk.Scale(self.window, from_ = self.c_min, to = self.c_max, length = self.w1,
                variable = self.c_scale_var, command = self.on_c_scale_change)
            self.c_scale.place(x = self.x2, y = self.y3)
            self.c_entry_var = tk.StringVar()
            self.c_entry_var.set(str(self.c))
            self.c_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.c_entry_var)
            self.c_entry.bind('<Return>', self.on_c_entry_change)
            self.c_entry.place(x = self.x3, y = self.y3)

            self.d_label = ttk.Label(self.window, text = i18n['d'])
            self.d_label.place(x = self.x1, y = self.y4)
            self.d_scale_var = tk.IntVar()
            self.d_scale_var.set(self.d)
            self.d_scale = ttk.Scale(self.window, from_ = self.d_min, to = self.d_max, length = self.w1,
                variable = self.d_scale_var, command = self.on_d_scale_change)
            self.d_scale.place(x = self.x2, y = self.y4)
            self.d_entry_var = tk.StringVar()
            self.d_entry_var.set(str(self.d))
            self.d_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.d_entry_var)
            self.d_entry.bind('<Return>', self.on_d_entry_change)
            self.d_entry.place(x = self.x3, y = self.y4)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        if self.contrast_mode == ContrastMode.LINEAR:
            self.parent.im = contrast_linear(self.old_im, self.a, self.b, self.c, self.d)
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR:
            self.parent.im = contrast_piecewise(self.old_im, self.a, self.b, self.c, self.d)
        elif self.contrast_mode == ContrastMode.LOGARITHMIC:
            self.parent.im = contrast_logarithmic(self.old_im, self.a, self.b)
        else:
            self.parent.im = contrast_exponential(self.old_im, self.a, self.b / 1000)

    def on_a_entry_change(self, event = None):
        try:
            na = int(self.a_entry_var.get())
            assert na >= self.a_min and na <= self.a_max
            if self.p4:
                assert na <= self.b
            if self.contrast_mode == ContrastMode.PIECEWISE_LINEAR:
                assert (na == 0) ^ (self.c != 0)
            self.a = na
        except:
            pass
        else:
            self.a_scale_var.set(self.a)
            self.update_image_show()
        finally:
            self.a_entry_var.set(str(self.a))

    def on_a_scale_change(self, event = None):
        self.a = self.a_scale_var.get()
        self.a_entry_var.set(str(self.a))
        if self.p4 and self.a > self.b:
            self.b_entry_var.set(str(self.a))
            self.on_b_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.a == 0 and self.c != 0:
            self.c_entry_var.set('0')
            self.on_c_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.a != 0 and self.c == 0:
            self.c_entry_var.set('1')
            self.on_c_entry_change()
        else:
            self.update_image_show()

    def on_b_entry_change(self, event = None):
        try:
            if self.contrast_mode == ContrastMode.EXPONENTIAL:
                nb = float(self.b_entry_var.get())
                assert nb >= self.b_min / 1000 and nb <= self.b_max / 1000
            else:
                nb = int(self.b_entry_var.get())
                assert nb >= self.b_min and nb <= self.b_max
            if self.p4:
                assert nb >= self.a
            if self.contrast_mode == ContrastMode.PIECEWISE_LINEAR:
                assert (nb == 255) ^ (self.d != 255)
            if self.contrast_mode == ContrastMode.EXPONENTIAL:
                self.b = nb * 1000
            else:
                self.b = nb
        except:
            pass
        else:
            self.b_scale_var.set(self.b)
            self.update_image_show()
        finally:
            if self.contrast_mode == ContrastMode.EXPONENTIAL:
                self.b_entry_var.set(display_1000(self.b))
            else:
                self.b_entry_var.set(str(self.b))

    def on_b_scale_change(self, event = None):
        self.b = self.b_scale_var.get()
        if self.contrast_mode == ContrastMode.EXPONENTIAL:
            self.b_entry_var.set(display_1000(self.b))
        else:
            self.b_entry_var.set(str(self.b))
        if self.p4 and self.b < self.a:
            self.a_entry_var.set(str(self.b))
            self.on_a_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.b == 255 and self.d != 255:
            self.d_entry_var.set('255')
            self.on_d_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.b != 255 and self.d == 255:
            self.d_entry_var.set('254')
            self.on_d_entry_change()
        else:
            self.update_image_show()

    def on_c_entry_change(self, event = None):
        try:
            nc = int(self.c_entry_var.get())
            assert nc >= self.c_min and nc <= self.c_max
            if self.p4:
                assert nc <= self.d
            if self.contrast_mode == ContrastMode.PIECEWISE_LINEAR:
                assert (nc == 0) ^ (self.a != 0)
            self.c = nc
        except:
            pass
        else:
            self.c_scale_var.set(self.c)
            self.update_image_show()
        finally:
            self.c_entry_var.set(str(self.c))

    def on_c_scale_change(self, event = None):
        self.c = self.c_scale_var.get()
        self.c_entry_var.set(str(self.c))
        if self.p4 and self.c > self.d:
            self.d_entry_var.set(str(self.c))
            self.on_d_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.c == 0 and self.a != 0:
            self.a_entry_var.set('0')
            self.on_a_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.c != 0 and self.a == 0:
            self.a_entry_var.set('1')
            self.on_a_entry_change()
        else:
            self.update_image_show()

    def on_d_entry_change(self, event = None):
        try:
            nd = int(self.d_entry_var.get())
            assert nd >= self.d_min and nd <= self.d_max
            if self.p4:
                assert nd >= self.c
            if self.contrast_mode == ContrastMode.PIECEWISE_LINEAR:
                assert (nd == 255) ^ (self.b != 255)
            self.d = nd
        except:
            pass
        else:
            self.d_scale_var.set(self.d)
            self.update_image_show()
        finally:
            self.d_entry_var.set(str(self.d))

    def on_d_scale_change(self, event = None):
        self.d = self.d_scale_var.get()
        self.d_entry_var.set(str(self.d))
        if self.p4 and self.d < self.c:
            self.c_entry_var.set(str(self.d))
            self.on_c_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.d == 255 and self.b != 255:
            self.b_entry_var.set('255')
            self.on_b_entry_change()
        elif self.contrast_mode == ContrastMode.PIECEWISE_LINEAR and self.d != 255 and self.b == 255:
            self.b_entry_var.set('254')
            self.on_b_entry_change()
        else:
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
