# Testing code for browser module

import unittest
import sys
from anki_mocks_test import *
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../anki_web_browser')

import browser
from browser import AwBrowser
from PyQt4.QtGui import QMenu, QApplication
from PyQt4.QtCore import QPoint

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

    def test_textSelection(self):
        pass

    def test_setNote(self):
        b = AwBrowser(None)
        b.setNote(TestNote())
        self.assertTrue(b._note)
        self.assertTrue(b._note.fields)

    def test_onContextMenu(self):
        b = AwBrowser(None)
        b.onContextMenu(FakeEvent())

    def test_close(self):
        b = AwBrowser(None)
        b.onClose()

    def test_installPage(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    unittest.main()