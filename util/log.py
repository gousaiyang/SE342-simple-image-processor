# -*- coding: utf-8 -*-

import logging

log_filename = 'error.log'

logger = logging.getLogger()
file_handler = logging.FileHandler(log_filename, 'a', 'utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
logger.addHandler(file_handler)
logger.setLevel(logging.WARN)
