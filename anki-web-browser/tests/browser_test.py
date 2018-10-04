# Testing code for browser module

import unittest
import sys
from anki_mocks_test import *
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import anki_web_browser.browser
from anki_web_browser.browser import AwBrowser
from PyQt5.QtWidgets import QMenu, QApplication
from PyQt5.QtCore import QPoint

class FakeBrowser:

    def page(self):        
        def currentFrame(self):
            def hitTestContent(self, evt):
                pass
            return self
        return self

class FakeEvent:
    def pos(self):
        return QPoint()

class Tester(unittest.TestCase):

    @classmethod
    def setUpClass(clz):
        pass

    def test_open(self):
        global mw
        b = AwBrowser(None)
        b.open('localhost/search?', 'ricardo')

    def test_unload(self):
        global mw
        b = AwBrowser(None)
        b.unload()

    def customSelected(self):
        return 'Selecionado!'

    def test_textSelection(self):
        return
        b = AwBrowser(None)
        b.setFields([
            {'name': 'Test'},
            {'name': 'Item2'}
        ])
        b.setSelectionListener(lambda a, b, c: print(a, b, c))
        b.selectedText = self.customSelected
        b.contextMenuEvent(FakeEvent())

    def test_setFields(self):
        b = AwBrowser(None)
        b.setFields(TestNote().fields)
        self.assertTrue(b._fields)

    def test_onContextMenu(self):
        b = AwBrowser(None)
        b.contextMenuEvent(FakeEvent())

    def test_close(self):
        b = AwBrowser(None)
        b.onClose()

    def test_installPage(self):
        pass

if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    unittest.main()