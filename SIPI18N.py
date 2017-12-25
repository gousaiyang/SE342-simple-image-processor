# -*- coding: utf-8 -*-

import locale

from SIPI18NResources import *

resource_suffix = '_resources'

all_languages = [name[:-len(resource_suffix)] for name, obj in globals().items()
    if name.endswith(resource_suffix) and isinstance(obj, dict) and 'language_name' in obj]
i18n_resources = {l: globals()[l + resource_suffix] for l in all_languages}

default_language = 'en'

class I18N:
    def __init__(self):
        default_locale = locale.getdefaultlocale()[0]
        self.language = default_locale if default_locale in all_languages else default_language

    def get_all_languages(self):
        return all_languages

    def get_all_language_names(self):
        return [i18n_resources[l]['language_name'] for l in all_languages]

    def get_default_language(self):
        return default_language

    def get_language(self):
        return self.language

    def set_language(self, language):
        if language not in all_languages:
            raise NameError('Language %s does not exist in the resource file.' % (language))

        self.language = language

    def set_to_default_language(self):
        self.language = default_language

    def get(self, entry, language=None):
        if language is not None and language not in all_languages:
            raise NameError('Language %s does not exist in the resource file.' % (language))

        return i18n_resources[language or self.language][entry]

    def __contains__(self, language):
        return language in all_languages

i18n = I18N()
