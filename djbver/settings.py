from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string


DEFAULTS = {
    'SMS_VERIFY_CODE_EXPIRE': 10
}


def perform_import(val, setting_name):
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class DjbverSettings:
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'DJBVER', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid setting: '%s'" % attr)

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        if attr in self.import_strings:
            val = perform_import(val, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


djbver_settings = DjbverSettings(None, DEFAULTS)


def reload_djbver_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'DJBVER':
        djbver_settings.reload()

setting_changed.connect(reload_djbver_settings)
