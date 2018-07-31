# anki-web-browser - Context menu for notes

import const
from browser import AwBrowser

# from aqt import mw
from PyQt4.QtGui import QMenu, QAction, QApplication

class NoteMenuBuilder:
    _providers = {}
    # _menu = QMenu()
    _note = None
    _searchString = ''

    def __init__(self, note, query):
        self._note = note
        self._searchString = query

    @classmethod
    def options(clazz, newValue: dict):
        if newValue:
            clazz._providers = newValue

    @staticmethod
    def onReviewerMenu(webView, menu):
        'Handles context menu event on Reviwer'

        _card = webView.reviewer.card
        # _card = mw.reviewer.card
        _instance = NoteMenuBuilder(_card._note, None)  # Fixme, get search str
        _instance.showCustomMenu(menu)

    @staticmethod
    def onEditorMenu(webView, menu):
        'Handles context menu event on Editor'

        _note = webView.editor.note
        _instance = NoteMenuBuilder(_note, None)    # hold the card ref  # Fixme, get search str
        _instance.showCustomMenu(menu)

    def showCustomMenu(self, parentMenu):
        submenu = QMenu(const.Label.CARD_MENU, parentMenu)

        for key, value in NoteMenuBuilder._providers.items():
            target = value + self._searchString if value.endsWith('/') else ('/' + self._searchString)
            act = QAction(key, submenu, 
                triggered=lambda: self.showInBrowser(target))
            submenu.addAction(act)

        # shortcut="Ctrl+Shift+L",
        # a1 = QAction(const.Label.MENU_LOW, submenu, 
        #         triggered=lambda: self.showInBrowser())
        # menu.addAction()

        parentMenu.addMenu(submenu)

    def showInBrowser(self, website: str):
        AwBrowser() # TODO: single instance


# -------------- Self contained tests --------------

if __name__ == '__main__':
    import unittest

    class TNote:
        _tag = None

    #     def hasTag(self, str):
    #         return str == self._tag

    class TCard:
        _note = TNote()

    class TReviewer:
        card = TCard()

    class TEditor():
        _note = TNote()

    class WebView:
        editor = TEditor()
        reviewer = TReviewer()

    class TMenu:
        pass

    class Tester(unittest.TestCase):
        
        def test_providers(self):
            providers = {
                'google': 'www.google.com',
                'wiki': 'www.wikipedia.com'
            }
            NoteMenuBuilder.options(providers)
            m = NoteMenuBuilder(None, None)
            self.assertTrue('google' in m._providers)
            self.assertFalse('yahoo' in m._providers)

        def test_menu_in_reviewer(self):
            NoteMenuBuilder.onReviewerMenu(WebView(), TMenu())

        def test_menu_in_editor(self):
            NoteMenuBuilder.onEditorMenu(WebView(), TMenu())

    #app = QApplication()
    unittest.main()
else:
    from aqt import mw