# Testing code for notemenu module

import unittest
import sys
import os
from anki_mocks_test import *

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from src.provider_selection import ProviderSelectionController

from PyQt5.QtWidgets import QMenu, QAction, QApplication

class FakeBrowser:
    def open(self, website, query):
        pass


class Tester(unittest.TestCase):

    def test_providers(self):
        sc = ProviderSelectionController()
        try:
            sc.showCustomMenu(None, FakeBrowser.open) # no parent
        except AttributeError:
            pass

    def test_showMenu(self):
        sc = ProviderSelectionController()
        class Parent(QMenu):
            done = False
            def addMenu(self, m):
                self.done = True

        p = Parent()
        sc.showCustomMenu(p, FakeBrowser.open)
        self.assertTrue(p.done)

    def selectedWithText(self):
        return 'teste'


if __name__ == '__main__':
    # searching.mw = mw
    app = QApplication(sys.argv)
    
    unittest.main()