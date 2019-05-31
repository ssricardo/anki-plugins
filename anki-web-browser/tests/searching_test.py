# Testing code for notemenu module

import unittest
import sys
import os
from anki_mocks_test import *

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import src.searching as searching
from src.searching import SearchingContext

from PyQt5.QtWidgets import QMenu, QAction, QApplication

class FakeBrowser:
    def open(self, website, query):
        pass


class Tester(unittest.TestCase):

    def test_providers(self):
        sc = SearchingContext(None, None, FakeBrowser.open)
        try:
            sc.showCustomMenu(None) # no parent
        except AttributeError:
            pass

    def test_showMenu(self):
        sc = SearchingContext(None, None, FakeBrowser.open)
        class Parent(QMenu):
            done = False
            def addMenu(self, m):
                self.done = True

        p = Parent()
        sc.showCustomMenu(p)
        self.assertTrue(p.done)

    def selectedWithText(self):
        return 'teste'

    # def test_menu_in_reviewer(self):
    #     TestWebView.selectedText = self.selectedWithText
    #     builder.createReviewerMenu(TestWebView(), QMenu(), TestNote(), FakeBrowser.open)

    # def test_menu_in_editor(self):
    #     TestWebView.selectedText = self.selectedWithText
    #     builder.createEditorMenu(TestWebView(), QMenu(), FakeBrowser.open)

if __name__ == '__main__':
    # searching.mw = mw
    app = QApplication(sys.argv)
    
    unittest.main()