# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

import transformation
from util import *
from i18n import i18n

def display_std_dev(v):
    return '%.1f' % (v)

class GaussianFilterDialog:
    def __init__(self, parent):
        self.init_state(parent)
        self.init_window()
        self.init_coords()
        self.init_widgets()
        self.update_image_show()

    def init_state(self, parent):
        self.parent = parent
        self.old_im = parent.im
        self.kw = 2
        self.std_dev = 1
        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(i18n['gaussian'])
        self.window.geometry('340x150')
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
        self.bottom_y = 100
        self.w1 = 200
        self.w2 = 5

    def init_widgets(self):
        self.kw_label = ttk.Label(self.window, text = i18n['kernel_width'])
        self.kw_label.place(x = self.x1, y = self.y1)
        self.kw_scale_var = tk.IntVar()
        self.kw_scale_var.set(self.kw)
        self.kw_scale = ttk.Scale(self.window, from_ = 0, to = 5, length = self.w1, variable = self.kw_scale_var,
            command = self.on_kw_scale_change)
        self.kw_scale.place(x = self.x2, y = self.y1)
        self.kw_entry_var = tk.StringVar()
        self.kw_entry_var.set(str(self.kw))
        self.kw_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.kw_entry_var)
        self.kw_entry.bind('<Return>', self.on_kw_entry_change)
        self.kw_entry.place(x = self.x3, y = self.y1)

        self.std_dev_label = ttk.Label(self.window, text = i18n['std_dev'])
        self.std_dev_label.place(x = self.x1, y = self.y2)
        self.std_dev_scale_var = tk.DoubleVar()
        self.std_dev_scale_var.set(self.std_dev)
        self.std_dev_scale = ttk.Scale(self.window, from_ = -0.1, to = 5, length = self.w1, variable = self.std_dev_scale_var,
            command = self.on_std_dev_scale_change)
        self.std_dev_scale.place(x = self.x2, y = self.y2)
        self.std_dev_entry_var = tk.StringVar()
        self.std_dev_entry_var.set(display_std_dev(self.std_dev))
        self.std_dev_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.std_dev_entry_var)
        self.std_dev_entry.bind('<Return>', self.on_std_dev_entry_change)
        self.std_dev_entry.place(x = self.x3, y = self.y2)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        self.parent.im = transformation.gaussian_filter(self.old_im, self.kw, self.std_dev)

    def on_kw_entry_change(self, event = None):
        try:
            nk = int(self.kw_entry_var.get())
            assert nk >= 0 and nk <= 5
            self.kw = nk
        except:
            pass
        else:
            self.kw_scale_var.set(self.kw)
            self.update_image_show()
        finally:
            self.kw_entry_var.set(str(self.kw))

    def on_kw_scale_change(self, event = None):
        self.kw = self.kw_scale_var.get()
        self.kw_entry_var.set(str(self.kw))
        self.update_image_show()

    def on_std_dev_entry_change(self, event = None):
        try:
            ns = float(self.std_dev_entry_var.get())
            assert ns >= 0.1 and ns <= 5
            self.std_dev = ns
        except:
            pass
        else:
            self.std_dev_scale_var.set(self.std_dev)
            self.update_image_show()
        finally:
            self.std_dev_entry_var.set(display_std_dev(self.std_dev))

    def on_std_dev_scale_change(self, event = None):
        self.std_dev = self.std_dev_scale_var.get()
        self.std_dev_entry_var.set(display_std_dev(self.std_dev))
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
