# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

from util import center_window, native_path_format, load_config, store_config
from i18n import i18n
from .display import ImageDisplayFrame

allowed_filetypes = [(i18n['image_files'], '*.bmp;*.jpg;*.jpeg;*.png;*.gif;*.tiff;*.webp'), (i18n['all_files'], '*.*')]

class MainDialog:
    def __init__(self):
        self.init_config()
        self.init_window()
        self.init_coords()
        self.init_widgets()

    def init_config(self):
        self.config = load_config()
        self.recent_dir = self.config['recent_dir']
        if self.config['language'] in i18n:
            i18n.language = self.config['language']
        self.current_file = ''

    def init_window(self):
        self.window = tk.Tk()
        self.window.withdraw()
        self.window.geometry('800x600')
        self.window.minsize(300, 300)
        center_window(self.window)
        self.window.deiconify()
        self.window.title(i18n['main_window_title'])
        self.window.protocol('WM_DELETE_WINDOW', self.on_close)
        self.window.bind('<Escape>', self.on_close)
        self.window.grab_set()

    def init_coords(self):
        pass

    def init_widgets(self):
        self.menu = tk.Menu(self.window)
        self.window.config(menu = self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = i18n['file'], menu = self.file_menu)
        self.file_menu.add_command(label = i18n['open'], command = self.open_file, accelerator = 'Ctrl+O')
        self.window.bind('<Control-o>', self.open_file)
        self.file_menu.add_command(label = i18n['save'], command = self.save_file, accelerator = 'Ctrl+S')
        self.window.bind('<Control-s>', self.save_file)
        self.file_menu.add_command(label = i18n['save_as'], command = self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = i18n['exit'], command = self.on_close, accelerator = 'Alt+F4')

        self.image_display = ImageDisplayFrame(self.window)
        self.image_display.pack()

        self.status_bar = tk.Label(self.window, text = '# Cursor pos and RGB here...', bd = 1, relief = tk.SUNKEN, anchor = tk.W)
        self.status_bar.pack(side = tk.BOTTOM, fill = tk.X)

    @property
    def im(self):
        return self.image_display.im

    @im.setter
    def im(self, new_im):
        self.image_display.update_image(new_im)

    def open_file(self, event = None):
        filepath = filedialog.askopenfilename(initialdir = self.recent_dir, filetypes = allowed_filetypes)
        if not filepath:
            return

        self.recent_dir = os.path.split(filepath)[0]
        store_config({'recent_dir': native_path_format(self.recent_dir)})
        try:
            im = Image.open(filepath)
        except:
            # TODO: log errors?
            messagebox.showerror(i18n['open_failed'], i18n['invalid_image'])
        else:
            self.current_file = filepath
            self.window.title(i18n['main_window_title'] + ' - ' + native_path_format(filepath))
            self.im = im

    def save_file(self, event = None):
        if not self.im:
            return # NOTE: Should we disable menu item?
        try:
            self.im.save(self.current_file)
        except:
            # TODO: log errors?
            messagebox.showerror(i18n['save_failed_title'],
                i18n['save_failed_content'] % (native_path_format(self.current_file)))

    def save_file_as(self, event = None):
        if not self.im:
            return
        current_dir, current_filename = os.path.split(self.current_file)
        filepath = filedialog.asksaveasfilename(initialdir = current_dir,
            initialfile = current_filename, filetypes = allowed_filetypes)
        if not filepath:
            return

        try:
            self.im.save(filepath)
        except:
            # TODO: log errors?
            messagebox.showerror(i18n['save_as_failed_title'], i18n['save_as_failed_content'] % (native_path_format(filepath)))

    def on_close(self, event = None):
        self.window.quit()

    def __call__(self):
        self.window.mainloop()
