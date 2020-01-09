# -*- coding: utf-8 -*-
# Related to no_selection
# Test code for no selecion option

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import unittest
import src.no_selection as ns

from PyQt5 import QtWidgets
app = QtWidgets.QApplication(sys.argv)

class NoSelectionTester(unittest.TestCase):

    _tested = ns.NoSelectionViewAdapter

    # TODO...

    def test_loadOK(self):
        cc.currentLocation = os.path.dirname(os.path.realpath(__file__))
        os.remove(cc.currentLocation + '/' + cc.CONFIG_FILE)
        config = self._tested.load()
        self.assertIsNotNone(config)
        self.assertEqual(config.keepBrowserOpened, True)
        self.assertEqual(config.browserAlwaysOnTop, False)
        self.assertEqual(5, len(config.providers))

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
            # c2 = cc.ConfigHolder()
            # c2.providers = ['Oh no!']
            # self._tested.validate(c2)
            self.fail() # exception expected
        except:
            pass

        try:
            # c2 = cc.ConfigHolder(keepBrowserOpened='Now as string')
            # self._tested.validate(c2)
            self.fail() # exception expected
        except:
            pass



if __name__ == '__main__':
    if '-view' in sys.argv:        
        main = QtWidgets.QMainWindow()
        view = ns.NoSelectionController(main)
        view.setFields({
            1: "State",
            2: "City",
            3: "Stadion"
        })
        # view.open()
        view.open()
        sys.exit(app.exec_())
    else:
        unittest.main()