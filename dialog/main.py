# -*- coding: utf-8 -*-

import os
import functools
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from matplotlib import pyplot as plt

import transformation
from util import *
from i18n import i18n
from .image_display import ImageDisplayFrame
from .hsl_adjust import HSLAdjustDialog
from .threshold_adjust import ThresholdAdjustDialog
from .scaling import ScalingDialog
from .rotation import RotationDialog
from .contrast_adjust import ContrastDialog
from .gaussian_filter import GaussianFilterDialog
from .matrix_input import MatrixInputDialog

allowed_filetypes = [(i18n['image_files'], '*.bmp;*.jpg;*.jpeg;*.png;*.gif;*.tiff;*.webp'), (i18n['all_files'], '*.*')]

def show_image_mode(im):
    mode = get_image_mode(im)
    if mode in [ImageMode.BINARY, ImageMode.GRAYSCALE, ImageMode.COLOR]:
        return [i18n['binary'], i18n['grayscale'], i18n['color']][mode - 1] + '(%s)' % (im.mode)
    else:
        raise TypeError(i18n['invalid_image'])

def show_pixel_value(v, mode):
    return ('RGB(%d, %d, %d)' % (v)) if mode == ImageMode.COLOR else v

def transform_method(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        if not self.im:
            return

        try:
            r = func(self, *args, **kw)
        except Exception as e:
            logger.exception(e)
            messagebox.showwarning(i18n['error'], str(e) or i18n['unknown_error'])
        else:
            self.im = self.version.current_version
            self.update_title()
            self.update_status_bar()
            return r
    return wrapper

class MainDialog:
    def __init__(self):
        self.init_config()
        self.init_state()
        self.init_window()
        self.init_coords()
        self.init_widgets()

    def init_config(self):
        self.config = load_config()
        self.recent_dir = self.config['recent_dir']
        if self.config['language'] in i18n:
            i18n.language = self.config['language']

    def init_state(self):
        self.current_file = ''
        self.version = Version()

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

        self.edit_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = i18n['edit'], menu = self.edit_menu)
        self.edit_menu.add_command(label = i18n['undo'], command = self.undo, accelerator = 'Ctrl+Z')
        self.window.bind('<Control-z>', self.undo)
        self.edit_menu.add_command(label = i18n['redo'], command = self.redo, accelerator = 'Ctrl+Y')
        self.window.bind('<Control-y>', self.redo)

        self.transformation_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = i18n['transformation'], menu = self.transformation_menu)
        self.color_image_processing_menu = tk.Menu(self.transformation_menu, tearoff = False)
        self.transformation_menu.add_cascade(label = i18n['color_image_processing'], menu = self.color_image_processing_menu)
        self.split_rgb_menu = tk.Menu(self.color_image_processing_menu, tearoff = False)
        self.color_image_processing_menu.add_cascade(label = i18n['split_rgb'], menu = self.split_rgb_menu)
        self.split_rgb_menu.add_command(label = i18n['R'], command = functools.partial(self.split_rgb, band = 'R'))
        self.split_rgb_menu.add_command(label = i18n['G'], command = functools.partial(self.split_rgb, band = 'G'))
        self.split_rgb_menu.add_command(label = i18n['B'], command = functools.partial(self.split_rgb, band = 'B'))
        self.color_image_processing_menu.add_command(label = i18n['color2grayscale'], command = self.color2grayscale)
        self.color_image_processing_menu.add_command(label = i18n['HSL_adjusting'], command = self.HSL_adjust)
        self.binarization_menu = tk.Menu(self.transformation_menu, tearoff = False)
        self.transformation_menu.add_cascade(label = i18n['binarization'], menu = self.binarization_menu)
        self.binarization_menu.add_command(label = i18n['otsu'], command = self.otsu)
        self.binarization_menu.add_command(label = i18n['manual_two_thresholds'], command = self.two_thresholds)
        self.arith_geo_menu = tk.Menu(self.transformation_menu, tearoff = False)
        self.transformation_menu.add_cascade(label = i18n['arith_geo'], menu = self.arith_geo_menu)
        self.arith_geo_menu.add_command(label = i18n['addition'], command = self.addition)
        self.arith_geo_menu.add_command(label = i18n['subtraction'], command = self.subtraction)
        self.arith_geo_menu.add_command(label = i18n['multiplication'], command = self.multiplication)
        ### TODO: add cropping
        self.scaling_menu = tk.Menu(self.arith_geo_menu, tearoff = False)
        self.arith_geo_menu.add_cascade(label = i18n['scaling'], menu = self.scaling_menu)
        self.scaling_menu.add_command(label = i18n['nearest'], command = self.scaling_nearest)
        self.scaling_menu.add_command(label = i18n['bilinear'], command = self.scaling_bilinear)
        self.rotation_menu = tk.Menu(self.arith_geo_menu, tearoff = False)
        self.arith_geo_menu.add_cascade(label = i18n['rotation'], menu = self.rotation_menu)
        self.rotation_menu.add_command(label = i18n['nearest'], command = self.rotation_nearest)
        self.rotation_menu.add_command(label = i18n['bilinear'], command = self.rotation_bilinear)
        self.contrast_menu = tk.Menu(self.transformation_menu, tearoff = False)
        self.transformation_menu.add_cascade(label = i18n['contrast_adjust'], menu = self.contrast_menu)
        self.contrast_menu.add_command(label = i18n['linear'], command = self.contrast_linear)
        self.contrast_menu.add_command(label = i18n['piecewise_linear'], command = self.contrast_piecewise)
        self.contrast_menu.add_command(label = i18n['logarithmic'], command = self.contrast_logarithmic)
        self.contrast_menu.add_command(label = i18n['exponential'], command = self.contrast_exponential)
        self.contrast_menu.add_command(label = i18n['histogram_display'], command = self.histogram_display)
        self.contrast_menu.add_command(label = i18n['histogram_equalization'], command = self.histogram_equalization)
        self.filter_menu = tk.Menu(self.transformation_menu, tearoff = False)
        self.transformation_menu.add_cascade(label = i18n['smooth_filter'], menu = self.filter_menu)
        self.filter_menu.add_command(label = i18n['average'], command = self.average_filter)
        self.filter_menu.add_command(label = i18n['median'], command = self.median_filter)
        self.filter_menu.add_command(label = i18n['gaussian'], command = self.gaussian_filter)
        self.filter_menu.add_command(label = i18n['custom_filter'], command = self.custom_filter)

        self.detection_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = i18n['detection'], menu = self.detection_menu)

        self.help_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = i18n['help'], menu = self.help_menu)

        self.image_display = ImageDisplayFrame(self.window)
        self.image_display.pack(fill = tk.BOTH, expand = 1)

        self.status_bar = tk.Label(self.window, text = i18n['ready'], bd = 1, relief = tk.SUNKEN, anchor = tk.W)
        self.status_bar.pack(side = tk.BOTTOM, fill = tk.X)

        self.window.bind('<Motion>', self.on_mouse_move)

    @property
    def im(self):
        return self.image_display.im

    @im.setter
    def im(self, new_im):
        self.image_display.update_image(new_im)

    def update_title(self):
        new_title = i18n['main_window_title']
        if self.current_file:
            new_title += ' - ' + native_path_format(self.current_file)
            if self.version.unsaved:
                new_title += ' (*)'

        self.window.title(new_title)

    def update_status_bar(self):
        if not self.im:
            self.status_bar.config(text = i18n['ready'])
            return

        if point_in_rect(cursor_pos_toplevel(self.window), self.image_display.image_rect):
            cursor_pos = self.image_display.cursor_pos
            cursor_value = self.image_display.cursor_value
            image_mode = get_image_mode(self.im)
            if cursor_pos and cursor_value is not None:
                self.status_bar.config(text = i18n['status_bar_text'] % (show_image_mode(self.im),
                    cursor_pos[0], cursor_pos[1], show_pixel_value(cursor_value, image_mode)))
            else:
                self.status_bar.config(text = i18n['status_bar_text_short'] % (show_image_mode(self.im)))
        else:
            self.status_bar.config(text = i18n['status_bar_text_short'] % (show_image_mode(self.im)))

    def open_file(self, event = None):
        filepath = filedialog.askopenfilename(title = i18n['open'], initialdir = self.recent_dir,
            filetypes = allowed_filetypes)
        if not filepath:
            return

        self.recent_dir = os.path.split(filepath)[0]
        store_config({'recent_dir': native_path_format(self.recent_dir)})
        try:
            im = Image.open(filepath)
            assert get_image_mode(im) != ImageMode.INVALID
        except:
            logger.exception(i18n['invalid_image'])
            messagebox.showerror(i18n['open_failed'], i18n['invalid_image'])
        else:
            self.current_file = filepath
            self.version.init(im)
            self.im = self.version.current_version
            self.update_title()
            self.update_status_bar()

    def save_file(self, event = None):
        if not self.im or not self.version.unsaved:
            return

        try:
            self.im.save(self.current_file)
            self.version.save()
            self.update_title()
        except:
            error_content = i18n['save_failed_content'] % (native_path_format(self.current_file))
            logger.exception(error_content)
            messagebox.showerror(i18n['save_failed_title'], error_content)

    def save_file_as(self, event = None):
        if not self.im:
            return

        current_dir, current_filename = os.path.split(self.current_file)
        filepath = filedialog.asksaveasfilename(title = i18n['save_as'], initialdir = current_dir,
            initialfile = current_filename, filetypes = allowed_filetypes)
        if not filepath:
            return

        try:
            self.im.save(filepath)
            self.version.save(discard_old = True)
            self.current_file = filepath
            self.update_title()
        except:
            error_content = i18n['save_as_failed_content'] % (native_path_format(filepath))
            logger.exception(error_content)
            messagebox.showerror(i18n['save_as_failed_title'], error_content)

    def on_mouse_move(self, event = None):
        self.update_status_bar()

    @transform_method
    def undo(self, event = None):
        self.version.undo()

    @transform_method
    def redo(self, event = None):
        self.version.redo()

    @transform_method
    def split_rgb(self, event = None, *, band):
        self.version.add(transformation.get_band(self.im, band))

    @transform_method
    def color2grayscale(self, event = None):
        self.version.add(transformation.color2grayscale(self.im))

    @transform_method
    def HSL_adjust(self, event = None):
        transformation.check_color_image(self.im)
        had = HSLAdjustDialog(self)
        had()
        if had.apply:
            self.version.add(self.im)

    @transform_method
    def otsu(self, event = None):
        self.version.add(transformation.otsu(self.im))

    @transform_method
    def two_thresholds(self, event = None):
        transformation.check_grayscale_image(self.im)
        tad = ThresholdAdjustDialog(self)
        tad()
        if tad.apply:
            self.version.add(self.im)

    @transform_method
    def addition(self, event = None):
        filepath = filedialog.askopenfilename(title = i18n['select_another_image'], initialdir = self.recent_dir,
            filetypes = allowed_filetypes)
        if not filepath:
            return

        try:
            im = Image.open(filepath)
            assert get_image_mode(im) != ImageMode.INVALID
        except:
            logger.exception(i18n['invalid_image'])
            messagebox.showerror(i18n['open_failed'], i18n['invalid_image'])
        else:
            self.version.add(transformation.image_addition(self.im, im))

    @transform_method
    def subtraction(self, event = None):
        filepath = filedialog.askopenfilename(title = i18n['select_another_image'], initialdir = self.recent_dir,
            filetypes = allowed_filetypes)
        if not filepath:
            return

        try:
            im = Image.open(filepath)
            assert get_image_mode(im) != ImageMode.INVALID
        except:
            logger.exception(i18n['invalid_image'])
            messagebox.showerror(i18n['open_failed'], i18n['invalid_image'])
        else:
            self.version.add(transformation.image_subtraction(self.im, im))

    @transform_method
    def multiplication(self, event = None):
        filepath = filedialog.askopenfilename(title = i18n['select_another_image'], initialdir = self.recent_dir,
            filetypes = allowed_filetypes)
        if not filepath:
            return

        try:
            im = Image.open(filepath)
            assert get_image_mode(im) != ImageMode.INVALID
        except:
            logger.exception(i18n['invalid_image'])
            messagebox.showerror(i18n['open_failed'], i18n['invalid_image'])
        else:
            self.version.add(transformation.image_multiplication(self.im, im))

    @transform_method
    def scaling_nearest(self, event = None):
        sd = ScalingDialog(self, transformation.scaling_nearest, i18n['nearest'])
        sd()
        if sd.apply:
            self.version.add(self.im)

    @transform_method
    def scaling_bilinear(self, event = None):
        sd = ScalingDialog(self, transformation.scaling_bilinear, i18n['bilinear'])
        sd()
        if sd.apply:
            self.version.add(self.im)

    @transform_method
    def rotation_nearest(self, event = None):
        rd = RotationDialog(self, transformation.rotation_nearest, i18n['nearest'])
        rd()
        if rd.apply:
            self.version.add(self.im)

    @transform_method
    def rotation_bilinear(self, event = None):
        rd = RotationDialog(self, transformation.rotation_bilinear, i18n['bilinear'])
        rd()
        if rd.apply:
            self.version.add(self.im)

    @transform_method
    def contrast_linear(self, event = None):
        cd = ContrastDialog(self, transformation.ContrastMode.LINEAR, i18n['linear'])
        cd()
        if cd.apply:
            self.version.add(self.im)

    @transform_method
    def contrast_piecewise(self, event = None):
        cd = ContrastDialog(self, transformation.ContrastMode.PIECEWISE_LINEAR, i18n['piecewise_linear'])
        cd()
        if cd.apply:
            self.version.add(self.im)

    @transform_method
    def contrast_logarithmic(self, event = None):
        cd = ContrastDialog(self, transformation.ContrastMode.LOGARITHMIC, i18n['logarithmic'])
        cd()
        if cd.apply:
            self.version.add(self.im)

    @transform_method
    def contrast_exponential(self, event = None):
        cd = ContrastDialog(self, transformation.ContrastMode.EXPONENTIAL, i18n['exponential'])
        cd()
        if cd.apply:
            self.version.add(self.im)

    @transform_method
    def histogram_display(self, event = None):
        index = np.arange(256)
        plt.figure().canvas.set_window_title(i18n['histogram_display'])
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.bar(index, transformation.grayscale_histogram(self.im))
        plt.title(i18n['histogram_display'])
        plt.xlabel(i18n['grayscale_value'])
        plt.ylabel(i18n['count'])
        plt.show()

    @transform_method
    def histogram_equalization(self, event = None):
        self.version.add(transformation.histogram_equalization(self.im))

    @transform_method
    def average_filter(self, event = None):
        self.version.add(transformation.average_filter(self.im))

    @transform_method
    def median_filter(self, event = None):
        self.version.add(transformation.median_filter(self.im))

    @transform_method
    def gaussian_filter(self, event = None):
        gfd = GaussianFilterDialog(self)
        gfd()
        if gfd.apply:
            self.version.add(self.im)

    @transform_method
    def custom_filter(self, event = None):
        mid = MatrixInputDialog(self, i18n['custom_filter'], i18n['kernel'], transformation.sharpen_filter_kernel,
            transformation.smooth_filter)
        mid()
        if mid.apply:
            self.version.add(self.im)

    def on_close(self, event = None):
        if self.im and self.version.unsaved:
            message_prompt = i18n['unsaved_exit_prompt'] % (native_path_format(self.current_file))
            if not messagebox.askyesno(i18n['exit'], message_prompt, default = messagebox.NO):
                return

        self.window.quit()

    def __call__(self):
        self.window.mainloop()
