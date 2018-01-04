# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

import transformation
from util import *
from i18n import i18n

class CropDialog:
    def __init__(self, parent):
        self.init_state(parent)
        self.init_window()
        self.init_coords()
        self.init_widgets()

    def init_state(self, parent):
        self.parent = parent
        self.width = parent.im.size[0]
        self.height = parent.im.size[1]
        self.old_im = parent.im
        self.left = 0
        self.left_min = 0
        self.left_max = self.width - 1
        self.right = self.width - 1
        self.right_min = 0
        self.right_max = self.width - 1
        self.top = 0
        self.top_min = 0
        self.top_max = self.height - 1
        self.bottom = self.height - 1
        self.bottom_min = 0
        self.bottom_max = self.height - 1
        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(i18n['crop'])
        self.window.geometry('340x210')
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
        self.bottom_y = 70 + self.yd * 3
        self.w1 = 200
        self.w2 = 5

    def init_widgets(self):
        self.left_label = ttk.Label(self.window, text = i18n['left'])
        self.left_label.place(x = self.x1, y = self.y1)
        self.left_scale_var = tk.IntVar()
        self.left_scale_var.set(self.left)
        self.left_scale = ttk.Scale(self.window, from_ = self.left_min, to = self.left_max, length = self.w1,
            variable = self.left_scale_var, command = self.on_left_scale_change)
        self.left_scale.place(x = self.x2, y = self.y1)
        self.left_entry_var = tk.StringVar()
        self.left_entry_var.set(str(self.left))
        self.left_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.left_entry_var)
        self.left_entry.bind('<Return>', self.on_left_entry_change)
        self.left_entry.place(x = self.x3, y = self.y1)

        self.right_label = ttk.Label(self.window, text = i18n['right'])
        self.right_label.place(x = self.x1, y = self.y2)
        self.right_scale_var = tk.IntVar()
        self.right_scale_var.set(self.right)
        self.right_scale = ttk.Scale(self.window, from_ = self.right_min, to = self.right_max, length = self.w1,
            variable = self.right_scale_var, command = self.on_right_scale_change)
        self.right_scale.place(x = self.x2, y = self.y2)
        self.right_entry_var = tk.StringVar()
        self.right_entry_var.set(str(self.right))
        self.right_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.right_entry_var)
        self.right_entry.bind('<Return>', self.on_right_entry_change)
        self.right_entry.place(x = self.x3, y = self.y2)

        self.top_label = ttk.Label(self.window, text = i18n['top'])
        self.top_label.place(x = self.x1, y = self.y3)
        self.top_scale_var = tk.IntVar()
        self.top_scale_var.set(self.top)
        self.top_scale = ttk.Scale(self.window, from_ = self.top_min, to = self.top_max, length = self.w1,
            variable = self.top_scale_var, command = self.on_top_scale_change)
        self.top_scale.place(x = self.x2, y = self.y3)
        self.top_entry_var = tk.StringVar()
        self.top_entry_var.set(str(self.top))
        self.top_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.top_entry_var)
        self.top_entry.bind('<Return>', self.on_top_entry_change)
        self.top_entry.place(x = self.x3, y = self.y3)

        self.bottom_label = ttk.Label(self.window, text = i18n['bottom'])
        self.bottom_label.place(x = self.x1, y = self.y4)
        self.bottom_scale_var = tk.IntVar()
        self.bottom_scale_var.set(self.bottom)
        self.bottom_scale = ttk.Scale(self.window, from_ = self.bottom_min, to = self.bottom_max, length = self.w1,
            variable = self.bottom_scale_var, command = self.on_bottom_scale_change)
        self.bottom_scale.place(x = self.x2, y = self.y4)
        self.bottom_entry_var = tk.StringVar()
        self.bottom_entry_var.set(str(self.bottom))
        self.bottom_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.bottom_entry_var)
        self.bottom_entry.bind('<Return>', self.on_bottom_entry_change)
        self.bottom_entry.place(x = self.x3, y = self.y4)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        self.parent.im = transformation.image_crop(self.old_im, self.left, self.top, self.right, self.bottom)

    def on_left_entry_change(self, event = None):
        try:
            nleft = int(self.left_entry_var.get())
            assert nleft >= self.left_min and nleft <= self.left_max
            assert nleft <= self.right
            self.left = nleft
        except:
            pass
        else:
            self.left_scale_var.set(self.left)
            self.update_image_show()
        finally:
            self.left_entry_var.set(str(self.left))

    def on_left_scale_change(self, event = None):
        self.left = self.left_scale_var.get()
        self.left_entry_var.set(str(self.left))
        if self.left > self.right:
            self.right_entry_var.set(str(self.left))
            self.on_right_entry_change()
        else:
            self.update_image_show()

    def on_right_entry_change(self, event = None):
        try:
            nright = int(self.right_entry_var.get())
            assert nright >= self.right_min and nright <= self.right_max
            assert nright >= self.left
            self.right = nright
        except:
            pass
        else:
            self.right_scale_var.set(self.right)
            self.update_image_show()
        finally:
            self.right_entry_var.set(str(self.right))

    def on_right_scale_change(self, event = None):
        self.right = self.right_scale_var.get()
        self.right_entry_var.set(str(self.right))
        if self.right < self.left:
            self.left_entry_var.set(str(self.right))
            self.on_left_entry_change()
        else:
            self.update_image_show()

    def on_top_entry_change(self, event = None):
        try:
            ntop = int(self.top_entry_var.get())
            assert ntop >= self.top_min and ntop <= self.top_max
            assert ntop <= self.bottom
            self.top = ntop
        except:
            pass
        else:
            self.top_scale_var.set(self.top)
            self.update_image_show()
        finally:
            self.top_entry_var.set(str(self.top))

    def on_top_scale_change(self, event = None):
        self.top = self.top_scale_var.get()
        self.top_entry_var.set(str(self.top))
        if self.top > self.bottom:
            self.bottom_entry_var.set(str(self.top))
            self.on_bottom_entry_change()
        else:
            self.update_image_show()

    def on_bottom_entry_change(self, event = None):
        try:
            nbottom = int(self.bottom_entry_var.get())
            assert nbottom >= self.bottom_min and nbottom <= self.bottom_max
            assert nbottom >= self.top
            self.bottom = nbottom
        except:
            pass
        else:
            self.bottom_scale_var.set(self.bottom)
            self.update_image_show()
        finally:
            self.bottom_entry_var.set(str(self.bottom))

    def on_bottom_scale_change(self, event = None):
        self.bottom = self.bottom_scale_var.get()
        self.bottom_entry_var.set(str(self.bottom))
        if self.bottom < self.top:
            self.top_entry_var.set(str(self.bottom))
            self.on_top_entry_change()
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
