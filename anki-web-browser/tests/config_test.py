# -*- coding: utf-8 -*-
# Related to config_controller
# Test code for config modules

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../anki_web_browser')

import unittest
import config as cc

from PyQt4 import QtGui
app = QtGui.QApplication(sys.argv)

class ConfigServiceTester(unittest.TestCase):

    _tested = cc.ConfigService()

    def test_loadOK(self):
        cc.currentLocation = os.path.dirname(os.path.realpath(__file__))
        os.remove(cc.currentLocation + '/' + cc.CONFIG_FILE)
        config = self._tested.load()
        self.assertIsNotNone(config)
        self.assertEqual(config.keepBrowserOpened, True)
        self.assertEqual(config.browserAlwaysOnTop, False)
        self.assertEqual(4, len(config.providers))


    def test_loadNoFile(self):
        try:
            config = self._tested.load(False)
            self.fail() # exception expected
        except:
            pass


    def test_loadAndSave(self):
        cc.currentLocation = os.path.dirname(os.path.realpath(__file__))
        config = self._tested.load(False)
        providers = config.providers
        providers.append(cc.ConfigHolder.Provider('Yahoo', 'https://www.yahoo.com/{}'))
        config.keepBrowserOpened = True
        self._tested._config = config

        return  # should not change the real file. Would break future tests
        self._tested.save()

    def test_validation(self):
        c = cc.ConfigHolder(browserAlwaysOnTop=True)
        self._tested.validate(c)
        try:
            c2 = 'Error'
            self._tested.validate(c2)
            self.fail() # exception expected
        except:
            pass
        
        try:
            c2 = cc.ConfigHolder()
            c2.providers = ['Oh no!']
            self._tested.validate(c2)
            self.fail() # exception expected
        except:
            pass

        try:
            c2 = cc.ConfigHolder(keepBrowserOpened='Now as string')
            self._tested.validate(c2)
            self.fail() # exception expected
        except:
            pass


class ConfigControllerTester(unittest.TestCase):

    cc.currentLocation = os.path.dirname(os.path.realpath(__file__))
    _tested = cc.ConfigController(None)
    
    def test_ItemSelection(self):
        self._tested.onSelectItem()
        self.assertTrue(self._tested._hasSelection)
        self._tested.onUnSelectItem()
        self.assertFalse(self._tested._hasSelection)


    def test_hasChanges(self):
        self._tested.onChangeItem()
        self.assertEqual(True, self._tested._pendingChanges)



if __name__ == '__main__':
    if '-view' in sys.argv:        
        main = QtGui.QMainWindow()
        view = cc.ConfigController(main)
        view.open()
        sys.exit(app.exec_())
    else:
        unittest.main()