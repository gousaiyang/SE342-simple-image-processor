# -*- coding: utf-8 -*-

import platform

is_windows = platform.system() == 'Windows'

def file_content(filename, encoding = 'utf-8'):
    with open(filename, 'rb') as fin:
        content = fin.read()
    return content.decode(encoding)

def write_file(filename, content, encoding = 'utf-8'):
    with open(filename, 'wb') as fout:
        fout.write(content.encode(encoding))

def native_path_format(path):
    return path.replace('/', '\\') if is_windows else path
