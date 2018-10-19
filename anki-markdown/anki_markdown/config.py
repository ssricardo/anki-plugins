# -*- coding: utf-8 -*-
# Handles Configuration reading, saving and the integration with the config UI
# Contains model, service and view controller for Config
#
# This files is part of anki-web-browser addon
# @author ricardo saturnino
# -------------------------------------------------------

from .core import Feedback

import os
import json
import re
import shutil

currentLocation = os.path.dirname(os.path.realpath(__file__))
# CONFIG_FILE = 'config.json'

# ---------------------------------- Model ------------------------------

class ConfigHolder:

    def __init__(self, keepBrowserOpened = False, browserAlwaysOnTop = False, providers = [], **kargs):
        pass

# ------------------------------ Service class --------------------------
class ConfigService:
    """
        Responsible for reading and storing configurations
    """
    pass        

# ------------------------------ View Controller --------------------------

class ConfigController:
    pass

# -----------------------------------------------------------------------------
# global instances

service = ConfigService()