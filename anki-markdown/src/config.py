# -*- coding: utf-8 -*-
# Handles Configuration reading, saving and the integration with the config UI
# Contains model, service and view controller for Config
#
# This files is part of anki-markdown-formatter addon
# @author ricardo saturnino
# -------------------------------------------------------

from .core import Feedback

import os
import json
import re
import shutil

currentLocation = os.path.dirname(os.path.realpath(__file__))


# ---------------------------------- Model ------------------------------

class ConfigKey:

    SHORTCUT = 'shortcut-menu'
    SHORTCUT_EDIT = 'shortcut-edit'
    SHOW_MARKDOWN_BUTTON = 'show-md-button'
    ENABLE_PREVIEW = 'enable-preview'
    DISABLE_MD_STYLE = 'disable-md-decorator'


# ------------------------------ Service class --------------------------
DEFAULT_CONFIG = {
    ConfigKey.SHORTCUT: 'Ctrl+Shift+M',
    ConfigKey.SHORTCUT_EDIT: 'Ctrl+Shift+K',
    ConfigKey.SHOW_MARKDOWN_BUTTON: True,
    ConfigKey.ENABLE_PREVIEW: True,
    ConfigKey.DISABLE_MD_STYLE: False
}

class ConfigService:
    """
        Responsible for reading and storing configurations
    """
    
    @staticmethod
    def _f(key):
        raise NotImplementedError()

    @classmethod
    def read(clz, key: str, expectedType):
        try:
            value = clz._f(key)
            if not (type(value) == expectedType):
                raise TypeError()
        except Exception as e:
            # print(e)
            value = None

        return value if (value is not None) else DEFAULT_CONFIG[key]


# -----------------------------------------------------------------------------
# global instances
