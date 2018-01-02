# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from util import *
from i18n import i18n

class RotationDialog:
    def __init__(self, parent, rotate_func, rotate_method_name):
        self.init_state(parent, rotate_func, rotate_method_name)
        self.init_window()
        self.init_coords()
        self.init_widgets()

    def init_state(self, parent, rotate_func, rotate_method_name):
        self.parent = parent
        self.rotate_func = rotate_func
        self.rotate_method_name = rotate_method_name
        self.old_im = parent.im
        self.degree = 0
        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(i18n['rotation'] + ' - ' + self.rotate_method_name)
        self.window.geometry('340x120')
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
        self.y1 = 20
        self.bottom_y = 70
        self.w1 = 200
        self.w2 = 5

    def init_widgets(self):
        self.degree_label = ttk.Label(self.window, text = i18n['degree'])
        self.degree_label.place(x = self.x1, y = self.y1)
        self.degree_scale_var = tk.IntVar()
        self.degree_scale_var.set(self.degree)
        self.degree_scale = ttk.Scale(self.window, from_ = -180, to = 180, length = self.w1, variable = self.degree_scale_var,
            command = self.on_degree_scale_change)
        self.degree_scale.place(x = self.x2, y = self.y1)
        self.degree_entry_var = tk.StringVar()
        self.degree_entry_var.set(str(self.degree))
        self.degree_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.degree_entry_var)
        self.degree_entry.bind('<Return>', self.on_degree_entry_change)
        self.degree_entry.place(x = self.x3, y = self.y1)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        self.parent.im = self.rotate_func(self.old_im, degree = self.degree)

    def on_degree_entry_change(self, event = None):
        try:
            nd = int(self.degree_entry_var.get())
            assert nd >= -180 and nd <= 180
            self.degree = nd
        except:
            pass
        else:
            self.degree_scale_var.set(self.degree)
            self.update_image_show()
        finally:
            self.degree_entry_var.set(str(self.degree))

    def on_degree_scale_change(self, event = None):
        self.degree = self.degree_scale_var.get()
        self.degree_entry_var.set(str(self.degree))
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
