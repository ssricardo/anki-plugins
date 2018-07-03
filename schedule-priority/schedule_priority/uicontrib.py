#pylint: disable=E0602,another-one

import anki
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

import const
from priority import Prioritizer

# Responsible for schedule-priority integration with Anki UI
class PriorityCardUiHandler:     

    _note = None

    def __init__(self, c):
        self._note = c

    def onClickLow(self):
        Prioritizer.setPriority(self._note, const.Priority.LOW)
        mw.reset()

    def onClickHigh(self):
        Prioritizer.setPriority(self._note, const.Priority.HIGH)
        mw.reset()

    def onClickNormal(self):
        Prioritizer.setPriority(self._note, 0)
        mw.reset()

    @staticmethod
    def onEditorCtxMenu(webView, menu):
        'Handles context menu event on Editor'

        _note = webView.editor.note
        _instance = PriorityCardUiHandler(_note)    # hold the card ref
        _instance.showCustomMenu(menu)

    @staticmethod
    def onReviewCtxMenu(webView, menu):
        'Handles context menu event on Reviwer'

        _card = mw.reviewer.card
        _instance = PriorityCardUiHandler(_card._note)
        _instance.showCustomMenu(menu)    

    def showCustomMenu(self, menu):
        submenu = QMenu(const.Label.CARD_MENU, menu)

        # shortcut="Ctrl+Shift+L",
        a1 = QAction(const.Label.MENU_LOW, submenu, 
                triggered=lambda: self.onClickLow())
        a2 = QAction(const.Label.MENU_NORMAL, submenu, 
                triggered=lambda: self.onClickNormal())
        a3 = QAction(const.Label.MENU_HIGH, submenu,
                triggered=lambda: self.onClickHigh())
        submenu.addAction(a1)
        submenu.addAction(a2)
        submenu.addAction(a3)

        menu.addMenu(submenu)


# ----------------------------------------- init ----------------------------------------

def init():
    anki.hooks.addHook('EditorWebView.contextMenuEvent', PriorityCardUiHandler.onEditorCtxMenu)
    anki.hooks.addHook('AnkiWebView.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)