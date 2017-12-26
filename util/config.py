# -*- coding: utf-8 -*-

import json

from i18n import i18n
from .file_util import file_content, write_file
from .log import logger

config_filename = 'config.json'

def load_config():
    try:
        data = json.loads(file_content(config_filename))
        assert isinstance(data['recent_dir'], str)
        assert isinstance(data['language'], str)
        return data
    except:
        logger.warning(i18n['load_config_failed'])
        return {'recent_dir': '.', 'language': ''}

def store_config(new_config):
    config = load_config()
    config.update(new_config)
    try:
        write_file(config_filename, json.dumps(config, indent = 4, ensure_ascii = False))
    except:
        logger.exception(i18n['store_config_failed'], config_filename)
