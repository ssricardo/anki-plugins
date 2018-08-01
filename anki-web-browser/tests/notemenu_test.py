# Testing code for notemenu module

import unittest
import sys
from anki_mocks_test import *

sys.path.append('/mnt/Dados/projetos/git/anki-addons/anki-plugins/anki-web-browser/anki_web_browser')

import notemenu
from notemenu import NoteMenuHandler
from PyQt4.QtGui import QMenu, QApplication

class FakeBrowser:
    def open(self, website, query):
        pass

class Tester(unittest.TestCase):

    @classmethod
    def setUpClass(clz):
        b = FakeBrowser()
        NoteMenuHandler.setWebBrowser(b)

    def test_providers(self):
        providers = {
            'google': 'www.google.com',
            'wiki': 'www.wikipedia.com'
        }
        NoteMenuHandler.setOptions(providers)
        m = NoteMenuHandler(None, None)
        self.assertTrue('google' in m._providers)
        self.assertFalse('yahoo' in m._providers)

    def selectedWithText(self):
        return 'teste'

    def test_menu_in_reviewer(self):
        TestWebView.selectedText = self.selectedWithText
        NoteMenuHandler.onReviewerMenu(TestWebView(), QMenu())

    def test_menu_in_editor(self):
        TestWebView.selectedText = self.selectedWithText
        NoteMenuHandler.onEditorMenu(TestWebView(), QMenu())

if __name__ == '__main__':
    notemenu.mw = mw
    app = QApplication(sys.argv)
    
    unittest.main()