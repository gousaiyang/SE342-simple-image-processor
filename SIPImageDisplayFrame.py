import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from SIPHelper import max_rect_2, get_window_size

class ImageDisplayFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        self.frame_upper = ttk.Frame(self.frame)
        self.frame_lower = ttk.Frame(self.frame)

        # TODO: Auto hide scrollbars when unnecessary?
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

        self.im = None
        self.imagetk = None

    def pack(self):
        self.frame.pack(fill = tk.BOTH, expand = 1)
        self.frame_upper.pack(fill = tk.BOTH, expand = 1)
        self.scroll_v.pack(side = tk.RIGHT, fill = tk.Y, expand = 0)
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = 1)
        self.frame_lower.pack(fill = tk.X, expand = 0)
        self.sizegrip.pack(side = tk.RIGHT)
        self.scroll_h.pack(side = tk.BOTTOM, fill = tk.X, expand = 0)
        self.image_label.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

    def update_size(self):
        new_canvas_scroll_size = max_rect_2(get_window_size(self.canvas), self.im.size if self.im else (0, 0))
        self.canvas.config(scrollregion = (0, 0) + new_canvas_scroll_size)
        self.image_frame.config(width = new_canvas_scroll_size[0], height = new_canvas_scroll_size[1])

    def update_image(self, im):
        self.im = im
        self.update_size()
        self.imagetk = ImageTk.PhotoImage(self.im)
        self.image_label.config(image = self.imagetk)

    def on_resize_canvas(self, event):
        self.update_size()
