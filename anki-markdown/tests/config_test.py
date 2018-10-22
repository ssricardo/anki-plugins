# -*- coding: utf-8 -*-
# Related to converter

# This files is part of anki-markdown addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import unittest
from anki_markdown.config import ConfigKey, ConfigService 

def f_num(k: str):
    return 7

def f_ok(k: str):
    if k == ConfigKey.SHOW_MARKDOWN_BUTTON:
        return False
    else:
        return 'Ctrl+W'

class Tester(unittest.TestCase):

    def test_funcNotSet(self):
        self.assertEqual('Ctrl+Shift+M', ConfigService.read(ConfigKey.SHORTCUT, str))
        self.assertEqual(True, ConfigService.read(ConfigKey.SHOW_MARKDOWN_BUTTON, bool))

    def test_funcWrongType(self):
        ConfigService._f = f_num

        self.assertEqual('Ctrl+Shift+M', ConfigService.read(ConfigKey.SHORTCUT, str))
        self.assertEqual(True, ConfigService.read(ConfigKey.SHOW_MARKDOWN_BUTTON, bool))

    def test_ok(self):
        ConfigService._f = f_ok

        self.assertEqual('Ctrl+W', ConfigService.read(ConfigKey.SHORTCUT, str))
        self.assertFalse(ConfigService.read(ConfigKey.SHOW_MARKDOWN_BUTTON, bool))

print('Running... ', __file__)
unittest.main()