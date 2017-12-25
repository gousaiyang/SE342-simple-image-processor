import json

from .util import file_content, write_file

config_filename = 'config.json'

def load_config():
    try:
        data = json.loads(file_content(config_filename))
        assert isinstance(data['recent_dir'], str)
        assert isinstance(data['language'], str)
        return data
    except:
        # TODO: log errors?
        return {'recent_dir': '.', 'language': ''}

def store_config(new_config):
    config = load_config()
    config.update(new_config)
    try:
        write_file(config_filename, json.dumps(config, indent = 4, ensure_ascii = False))
    except:
        # TODO: log errors?
        pass
