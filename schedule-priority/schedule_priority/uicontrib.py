import anki
#from anki.cards import Card
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

import const
from priority import Prioritizer

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
    def onContextMenu(webView, menu):

        _note = webView.editor.note
        _instance = PriorityCardUiHandler(_note)    # hold the card ref

        submenu = QMenu(const.Label.CARD_MENU, menu)

        # shortcut="Ctrl+Shift+L",
        a1 = QAction(const.Label.MENU_LOW, submenu, 
                triggered=_instance.onClickLow)
        submenu.addAction(a1)

        # submenu.addAction(const.Label.MENU_LOW, 
        #     _instance.onClickLow)
        submenu.addAction(const.Label.MENU_NORMAL, 
            lambda: _instance.onClickNormal())
        submenu.addAction(const.Label.MENU_HIGH, 
            lambda: _instance.onClickHigh())

        menu.addMenu(submenu)


# ----------------------------------------- init ----------------------------------------

def init():
    anki.hooks.addHook('EditorWebView.contextMenuEvent', PriorityCardUiHandler.onContextMenu)