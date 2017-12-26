# -*- coding: utf-8 -*-

import locale

from .resources import *

resource_suffix = '_resources'

_all_languages = [name[:-len(resource_suffix)] for name, obj in globals().items()
    if name.endswith(resource_suffix) and isinstance(obj, dict) and 'language_name' in obj]
i18n_resources = {l: globals()[l + resource_suffix] for l in _all_languages}

_default_language = 'en'

if _default_language not in _all_languages:
    raise KeyError('Default language does not exist in the resource file!')
for l in _all_languages:
    if set(i18n_resources[l].keys()) != set(i18n_resources[_default_language].keys()):
        raise KeyError('Inconsistent keys between "%s" resources and "%s" resources.' % (l, _default_language))

class I18N:
    def __init__(self):
        default_locale = locale.getdefaultlocale()[0]
        self._language = default_locale if default_locale in _all_languages else _default_language

    @property
    def all_languages(self):
        return _all_languages

    @property
    def all_language_names(self):
        return [i18n_resources[l]['language_name'] for l in _all_languages]

    @property
    def default_language(self):
        return _default_language

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, new_language):
        if new_language not in _all_languages:
            raise NameError('Language %s does not exist in the resource file.' % (new_language))

        self._language = new_language

    def reset_default(self):
        self._language = _default_language

    def get(self, entry, language = None):
        if language is not None and language not in _all_languages:
            raise NameError('Language %s does not exist in the resource file.' % (language))

        return i18n_resources[language or self._language][entry]

    def __getitem__(self, entry):
        return self.get(entry)

    def __contains__(self, language):
        return language in _all_languages

i18n = I18N()
