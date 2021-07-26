# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

#pylint: disable=E0602,another-one

from . import core
from .core import Priority
from .core import Feedback
from .core import AppHolder
from .prioritizer import Prioritizer

from PyQt5.QtWidgets import QMenu, QAction

js_Info_Priority = """
var prStyle = `<style type="text/css">
.priorInfo {    
    position: fixed;
    bottom: 30px;
    right: 70px;
    background: rgba(176, 196, 222, 0.3);
    padding: 7px;
    font-size: 12px;
}
</style>`;

$(prStyle).appendTo('body');

function setPriority(value) {
    let pdiv = `<div class="priorInfo">
        Priority: <b>${value}</b>
    <div>`;
    $(pdiv).appendTo('#qa');
}
"""

# Responsible for schedule-priority integration with Anki UI
class PriorityCardUiHandler:

    _note = None

    def __init__(self, c):
        self._note = c

    @staticmethod
    def prepareWebview():
        reviewer = AppHolder.app.reviewer
        reviewer.web.eval(js_Info_Priority)

    @staticmethod
    def showNewPriority(value: str):
        reviewer = AppHolder.app.reviewer
        reviewer.web.eval("""
            setTimeout(function() {
                setPriority("%s")
            }, 100);
        """ % value)

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

        if not _card:
            return

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

        for index, item in enumerate(Priority.priorityList):
            act = QAction('(&' + str(index + 1) + ') ' + item.description, submenu,
                triggered=self._makeMenuAction(index))

            submenu.addAction(act)

        menu.addMenu(submenu)

    @staticmethod
    def onShowQA(**args):
        reviewer = AppHolder.app.reviewer
        if not reviewer.card:
            return
        note = reviewer.card._note

        customPriority = None
        for p in Priority.priorityList:
            if not p.tagName:
                continue

            if note.hasTag(p.tagName):
                customPriority = p.description

        if customPriority:
            PriorityCardUiHandler.showNewPriority(customPriority)
