# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

import transformation
from util import *
from i18n import i18n

class ThresholdAdjustDialog:
    def __init__(self, parent):
        self.init_state(parent)
        self.init_window()
        self.init_coords()
        self.init_widgets()
        self.update_image_show()

    def init_state(self, parent):
        self.parent = parent
        self.old_im = parent.im
        self.low_th = 128
        self.high_th = 256
        self.apply = None

    def init_window(self):
        self.window = tk.Toplevel(self.parent.window)
        self.window.title(i18n['manual_two_thresholds'])
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
        self.low_th_label = ttk.Label(self.window, text = i18n['low_threshold'])
        self.low_th_label.place(x = self.x1, y = self.y1)
        self.low_th_scale_var = tk.IntVar()
        self.low_th_scale_var.set(self.low_th)
        self.low_th_scale = ttk.Scale(self.window, from_ = 0, to = 256, length = self.w1, variable = self.low_th_scale_var,
            command = self.on_low_th_scale_change)
        self.low_th_scale.place(x = self.x2, y = self.y1)
        self.low_th_entry_var = tk.StringVar()
        self.low_th_entry_var.set(str(self.low_th))
        self.low_th_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.low_th_entry_var)
        self.low_th_entry.bind('<Return>', self.on_low_th_entry_change)
        self.low_th_entry.place(x = self.x3, y = self.y1)

        self.high_th_label = ttk.Label(self.window, text = i18n['high_threshold'])
        self.high_th_label.place(x = self.x1, y = self.y2)
        self.high_th_scale_var = tk.IntVar()
        self.high_th_scale_var.set(self.high_th)
        self.high_th_scale = ttk.Scale(self.window, from_ = 0, to = 256, length = self.w1, variable = self.high_th_scale_var,
            command = self.on_high_th_scale_change)
        self.high_th_scale.place(x = self.x2, y = self.y2)
        self.high_th_entry_var = tk.StringVar()
        self.high_th_entry_var.set(str(self.high_th))
        self.high_th_entry = ttk.Entry(self.window, width = self.w2, textvariable = self.high_th_entry_var)
        self.high_th_entry.bind('<Return>', self.on_high_th_entry_change)
        self.high_th_entry.place(x = self.x3, y = self.y2)

        self.apply_button = ttk.Button(self.window, text = i18n['apply'], command = self.on_apply)
        self.apply_button.place(x = self.bottom_x1, y = self.bottom_y)

        self.cancel_button = ttk.Button(self.window, text = i18n['cancel'], command = self.on_cancel)
        self.cancel_button.place(x = self.bottom_x2, y = self.bottom_y)

    def update_image_show(self):
        self.parent.im = transformation.two_thresholds(self.old_im, self.low_th, self.high_th)

    def on_low_th_entry_change(self, event = None):
        try:
            lth = int(self.low_th_entry_var.get())
            assert lth >= 0 and lth <= 256
            self.low_th = lth
        except:
            pass
        else:
            self.low_th_scale_var.set(self.low_th)
            self.update_image_show()
        finally:
            self.low_th_entry_var.set(str(self.low_th))

    def on_low_th_scale_change(self, event = None):
        self.low_th = self.low_th_scale_var.get()
        self.low_th_entry_var.set(str(self.low_th))
        self.update_image_show()

    def on_high_th_entry_change(self, event = None):
        try:
            hth = int(self.high_th_entry_var.get())
            assert hth >= 0 and hth <= 256
            self.high_th = hth
        except:
            pass
        else:
            self.high_th_scale_var.set(self.high_th)
            self.update_image_show()
        finally:
            self.high_th_entry_var.set(str(self.high_th))

    def on_high_th_scale_change(self, event = None):
        self.high_th = self.high_th_scale_var.get()
        self.high_th_entry_var.set(str(self.high_th))
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
