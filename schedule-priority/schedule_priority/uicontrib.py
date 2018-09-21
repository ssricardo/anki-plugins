#pylint: disable=E0602,another-one

# import anki
# from aqt import mw
# from aqt.utils import showInfo
# from aqt.qt import *

from . import core
from .core import Priority
from .core import Feedback
from .core import AppHolder
from .priority import Prioritizer

from PyQt5.QtWidgets import QMenu, QAction

# Responsible for schedule-priority integration with Anki UI
class PriorityCardUiHandler:     

    _note = None

    def __init__(self, c):
        self._note = c

    def setNewPriority(self, value):
        Prioritizer.setPriority(self._note, value)
        AppHolder.app.reset()

    @staticmethod
    def onEditorCtxMenu(webView, menu):
        'Handles context menu event on Editor'

        _note = webView.editor.note
        _instance = PriorityCardUiHandler(_note)    # hold the card ref
        _instance.showCustomMenu(menu)

    @staticmethod
    def onReviewCtxMenu(webView, menu):
        'Handles context menu event on Reviewer'

        _card = AppHolder.app.reviewer.card
        _instance = PriorityCardUiHandler(_card._note)
        _instance.showCustomMenu(menu)

    def _makeMenuAction(self, value):
        """
            Creates correct action for the context menu selection.
            Otherwise, it would repeat only the last element
        """

        return lambda: self.setNewPriority(value)

    def showCustomMenu(self, menu):
        submenu = QMenu(core.Label.CARD_MENU, menu)

        # shortcut="Ctrl+Shift+L",
        a1 = QAction(core.Label.MENU_LOW, submenu, 
                triggered=lambda: self.onClickLow())
        a2 = QAction(core.Label.MENU_NORMAL, submenu, 
                triggered=lambda: self.onClickNormal())
        a3 = QAction(core.Label.MENU_HIGH, submenu,
                triggered=lambda: self.onClickHigh())

        for index, item in enumerate(Priority.priorityList):
            act = QAction(item.description, submenu,
                triggered=self._makeMenuAction(index))

            submenu.addAction(act)

        menu.addMenu(submenu)
