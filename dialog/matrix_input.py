# -*- coding: utf-8 -*-

import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from util import *
from i18n import i18n

def validate_matrix(s):
    if not re.match(r'^[0-9\[\],. -]+$', s):
        return False

    try:
        eval(s)
    except:
        return False
    else:
        return True

class MatrixInputDialog:
    def __init__(self, parent, title, label_name, default_matrix, transform_func):
        self.init_state(parent, title, label_name, default_matrix, transform_func)
        self.init_window()
        self.init_coords()
        self.init_widgets()
        self.update_image_show()

    def init_state(self, parent, title, label_name, default_matrix, transform_func):
        self.parent = parent
        self.title = title
        self.label_name = label_name
        self.transform_func = transform_func
        self.old_im = parent.im
        self.matrix = default_matrix
        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(self.title)
        self.window.geometry('340x120')
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.window.bind('<Escape>', self.on_cancel)
        center_window(self.window)
        self.window.grab_set()

    def init_coords(self):
        self.x1 = 10
        self.x2 = 80
        self.bottom_x1 = 77
        self.bottom_x2 = 177
        self.y1 = 20
        self.bottom_y = 70
        self.w = 30

    def init_widgets(self):
        self.matrix_label = ttk.Label(self.window, text = self.label_name)
        self.matrix_label.place(x = self.x1, y = self.y1)
        self.matrix_entry_var = tk.StringVar()
        self.matrix_entry_var.set(str(self.matrix))
        self.matrix_entry = ttk.Entry(self.window, width = self.w, textvariable = self.matrix_entry_var)
        self.matrix_entry.bind('<Return>', self.on_matrix_entry_change)
        self.matrix_entry.place(x = self.x2, y = self.y1)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        try:
            self.parent.im = self.transform_func(self.old_im, self.matrix)
        except Exception as e:
            logger.exception(e)
            messagebox.showwarning(i18n['error'], str(e) or i18n['unknown_error'])

    def on_matrix_entry_change(self, event = None):
        try:
            nm = self.matrix_entry_var.get()
            assert validate_matrix(nm)
            self.matrix = eval(nm)
        except:
            pass
        else:
            self.update_image_show()
        finally:
            self.matrix_entry_var.set(str(self.matrix))

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
