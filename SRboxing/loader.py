# -*- encoding: utf-8 -*-
import json
import os


# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


_secrets = {}
_secret_path = os.path.join(os.path.dirname(__file__), 'secret.json')
if os.path.exists(_secret_path):
    with open(_secret_path) as f:
        _secrets = json.loads(f.read())


_service_configs = {}
_service_config_path = os.path.join(os.path.dirname(__file__), 'config.json')
if os.path.exists(_service_config_path):
    with open(_service_config_path) as f:
        _service_configs = json.loads(f.read())

class empty(object):
    pass


def load_credential(key, default=empty):
    """
    환경 변수를 불러옵니다. (1순위: secret.json)
    """
    if key in _secrets:
        return _secrets[key]
    elif key in _service_configs:
        return _service_configs[key]
    elif default == empty:
        error = 'Failed to load credential for key : "{}"; '.format(key)
        error += 'call load_credential("{}", default=...) to ignore this error.'.format(key)
        raise ImproperlyConfigured(error)
    else:
        return default

