# -*- coding: utf-8 -*-

import math

import tkinter as tk
from tkinter import ttk

from util import *
from i18n import i18n

def display_scale_value(scale):
    return '%d' % (round(scale * 100))

class ScalingDialog:
    def __init__(self, parent, scale_func, scale_method_name):
        self.init_state(parent, scale_func, scale_method_name)
        self.init_window()
        self.init_coords()
        self.init_widgets()

    def init_state(self, parent, scale_func, scale_method_name):
        self.parent = parent
        self.scale_func = scale_func
        self.scale_method_name = scale_method_name
        self.old_im = parent.im
        self.x_scale = 1
        self.y_scale = 1
        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(i18n['scaling'] + ' - ' + self.scale_method_name)
        self.window.geometry('350x150')
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.window.bind('<Escape>', self.on_cancel)
        center_window(self.window)
        self.window.grab_set()

    def init_coords(self):
        self.x1 = 10
        self.x2 = 80
        self.x3 = 285
        self.x4 = 328
        self.bottom_x1 = 82
        self.bottom_x2 = 182
        self.yd = 30
        self.y1 = 20
        self.y2 = self.y1 + self.yd
        self.bottom_y = 100
        self.w1 = 200
        self.w2 = 5

    def init_widgets(self):
        self.x_scale_label = ttk.Label(self.window, text = i18n['horizontal'])
        self.x_scale_label.place(x = self.x1, y = self.y1)
        self.x_scale_scale_var = tk.DoubleVar()
        self.x_scale_scale_var.set(0)
        self.x_scale_scale = ttk.Scale(self.window, from_ = -5, to = 5, length = self.w1, variable = self.x_scale_scale_var,
            command = self.on_x_scale_scale_change)
        self.x_scale_scale.place(x = self.x2, y = self.y1)
        self.x_scale_entry_var = tk.StringVar()
        self.x_scale_entry_var.set(display_scale_value(self.x_scale))
        self.x_scale_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.x_scale_entry_var)
        self.x_scale_entry.bind('<Return>', self.on_x_scale_entry_change)
        self.x_scale_entry.place(x = self.x3, y = self.y1)
        self.x_percent_label = ttk.Label(self.window, text = '%')
        self.x_percent_label.place(x = self.x4, y = self.y1)

        self.y_scale_label = ttk.Label(self.window, text = i18n['vertical'])
        self.y_scale_label.place(x = self.x1, y = self.y2)
        self.y_scale_scale_var = tk.DoubleVar()
        self.y_scale_scale_var.set(0)
        self.y_scale_scale = ttk.Scale(self.window, from_ = -5, to = 5, length = self.w1, variable = self.y_scale_scale_var,
            command = self.on_y_scale_scale_change)
        self.y_scale_scale.place(x = self.x2, y = self.y2)
        self.y_scale_entry_var = tk.StringVar()
        self.y_scale_entry_var.set(display_scale_value(self.y_scale))
        self.y_scale_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.y_scale_entry_var)
        self.y_scale_entry.bind('<Return>', self.on_y_scale_entry_change)
        self.y_scale_entry.place(x = self.x3, y = self.y2)
        self.y_percent_label = ttk.Label(self.window, text = '%')
        self.y_percent_label.place(x = self.x4, y = self.y2)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        self.parent.im = self.scale_func(self.old_im, x_scale = self.x_scale, y_scale = self.y_scale)

    def on_x_scale_entry_change(self, event = None):
        try:
            xs = float(self.x_scale_entry_var.get())
            assert xs >= 20 and xs <= 500
            self.x_scale = xs / 100
        except:
            pass
        else:
            self.x_scale_scale_var.set(math.log(self.x_scale, 5) * 5)
            self.update_image_show()
        finally:
            self.x_scale_entry_var.set(display_scale_value(self.x_scale))

    def on_x_scale_scale_change(self, event = None):
        self.x_scale = 5 ** (self.x_scale_scale_var.get() / 5)
        self.x_scale_entry_var.set(display_scale_value(self.x_scale))
        self.update_image_show()

    def on_y_scale_entry_change(self, event = None):
        try:
            ys = float(self.y_scale_entry_var.get())
            assert ys >= 20 and ys <= 500
            self.y_scale = ys / 100
        except:
            pass
        else:
            self.y_scale_scale_var.set(math.log(self.y_scale, 5) * 5)
            self.update_image_show()
        finally:
            self.y_scale_entry_var.set(display_scale_value(self.y_scale))

    def on_y_scale_scale_change(self, event = None):
        self.y_scale = 5 ** (self.y_scale_scale_var.get() / 5)
        self.y_scale_entry_var.set(display_scale_value(self.y_scale))
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
