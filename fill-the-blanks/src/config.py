# -*- coding: utf-8 -*-
# Handles Configuration reading, saving and the integration with the config UI
# Contains model, service and view controller for Config
#
# This files is part of fill-the-blanks addon
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

# ------------------------------ Service class --------------------------
DEFAULT_CONFIG = {
    ConfigKey.SHORTCUT: 'Ctrl+Shift+...'
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
