# Testing code for browser module

import unittest
import sys
from anki_mocks_test import *
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import src.browser
from src.browser import AwBrowser
from PyQt5.QtWidgets import QMenu, QApplication, QMainWindow
from PyQt5.QtCore import QPoint
from src.core import Feedback

def testLog(*args, **vargs):
    print(args, vargs)

Feedback.log = testLog

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
        b.setSelectionHandler(lambda a, b, c: print(a, b, c))
        b.selectedText = self.customSelected
        b.contextMenuEvent(FakeEvent())

    def test_setFields(self):
        b = AwBrowser(None)
        b.setFields(TestNote().fields)
        self.assertTrue(b._fields)

    def test_onContextMenu(self):
        b = AwBrowser(None)
        b.contextMenuEvent(FakeEvent())

    def test_repeatableAction(self):
        b = AwBrowser(None)
        b.setFields([
            {'name': 'Test'},
            {'name': 'Item2'}
        ])
        b.setSelectionHandler(lambda a, b, c: print(a, b, c))

        self.assertFalse (b._assignToLastField('Novo', False))
        menuFn = b._makeMenuAction(b._fields[1], 'Test', False)
        menuFn()
        b._tryRepeat = True
        self.assertTrue (b._assignToLastField('Novo', False))


    def test_close(self):
        b = AwBrowser(None)
        b.onClose()

    def test_installPage(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)    
    if '-view' in sys.argv:        
        main = QMainWindow()
        view = AwBrowser(main)
        view.setFields({0: 'Example', 1: 'Other'})
        view.infoList = ['No action available']

        def handlerFn(f, v, l):
            print('Field: %s' % (f))
            print('Link/Value: %s / %s' % (l, v))

        view._selectionHandler = handlerFn
        view.open('https://www.google.com/search?tbm=isch&tbs=isz:i&q={}', 'calendar')
        sys.exit(app.exec_())
    else:
        unittest.main()