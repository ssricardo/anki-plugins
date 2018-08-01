# anki-web-browser - Context menu for notes

import const
from browser import AwBrowser

from aqt import mw
from aqt.utils import showInfo, tooltip

from PyQt4.QtGui import QMenu, QAction, QApplication

class NoteMenuHandler:
    _providers = {}
    # _menu = QMenu()
    _note = None
    _searchString = ''

    def __init__(self, note, query):
        self._note = note
        if query:
            self._searchString = query.encode('utf8')

    @classmethod
    def options(clz, newValue):
        if newValue:
            clz._providers = newValue

    @staticmethod
    def onReviewerMenu(webView, menu):
        'Handles context menu event on Reviwer'

        _card = mw.reviewer.card
        _query = webView.selectedText()

        if not _query:
            return

        # _card = mw.reviewer.card
        _instance = NoteMenuHandler(_card._note, _query)  # Fixme, get search str
        _instance.showCustomMenu(menu)

    @staticmethod
    def onEditorMenu(webView, menu):
        'Handles context menu event on Editor'

        _query = webView.selectedText()

        if not _query:
            return

        _note = webView.editor.note
        _instance = NoteMenuHandler(_note, _query)    # hold the card ref  # Fixme, get search str
        _instance.showCustomMenu(menu)

    def showCustomMenu(self, parentMenu):
        'Builds the addon entry in the context menu, adding options according to the providers'

        submenu = QMenu(const.Label.CARD_MENU, parentMenu)

        for key, value in NoteMenuHandler._providers.items():
            act = QAction(key, submenu, 
                triggered=lambda: self.showInBrowser(value))
            submenu.addAction(act)

        # shortcut="Ctrl+Shift+L",
        # a1 = QAction(const.Label.MENU_LOW, submenu, 
        #         triggered=lambda: self.showInBrowser())
        # menu.addAction()

        parentMenu.addMenu(submenu)

    def showInBrowser(self, website):
        global brw

        brw = AwBrowser() # TODO: single instance
        tooltip(_("Loading..."), period=1000)
        brw.open(website, self._searchString)

brw = None

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
            NoteMenuHandler.options(providers)
            m = NoteMenuHandler(None, None)
            self.assertTrue('google' in m._providers)
            self.assertFalse('yahoo' in m._providers)

        def test_menu_in_reviewer(self):
            NoteMenuHandler.onReviewerMenu(WebView(), TMenu())

        def test_menu_in_editor(self):
            NoteMenuHandler.onEditorMenu(WebView(), TMenu())

    #app = QApplication()
    unittest.main()
else:
    from aqt import mw