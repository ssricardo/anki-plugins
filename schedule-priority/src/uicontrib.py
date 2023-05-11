# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

#pylint: disable=E0602,another-one

from . import core
from .core import Priority
from .core import AppHolder
from .prioritizer import get_priority_tag_command, set_priority_tag

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


    @staticmethod
    def onEditorCtxMenu(webView, menu):
        """Handles context menu event on Editor"""

        if not webView or not webView.editor:
            return

        PriorityCardUiHandler.show_menu_for_editor(menu, webView.editor)

    @staticmethod
    def onReviewCtxMenu(webView, menu):
        """Handles context menu event on Reviewer"""

        _card = AppHolder.app.reviewer.card

        if not _card:
            return

        PriorityCardUiHandler.show_menu_reviewer(menu, AppHolder.app.reviewer)

    def _makeMenuAction(self, value, anki_editor):
        """
            Creates correct action for the context menu selection.
            Otherwise, it would repeat only the last element
        """

        def set_new_priority():
            tag_command = get_priority_tag_command(anki_editor.note, value)
            anki_editor.onBridgeCmd(tag_command)

        return set_new_priority

    @staticmethod
    def show_menu_reviewer(menu, reviewer):
        submenu = QMenu(core.Label.CARD_MENU, menu)

        def make_menu_action(value: int):
            def set_new_priority():
                set_priority_tag(reviewer.card.note(), value)
                AppHolder.app.reset()

            return set_new_priority

        for index, item in enumerate(Priority.priorityList):
            act = QAction('(&' + str(index + 1) + ') ' + item.description, submenu,
                triggered=make_menu_action(index))

            submenu.addAction(act)

        menu.addMenu(submenu)

    @staticmethod
    def show_menu_for_editor(menu, editor):
        submenu = QMenu(core.Label.CARD_MENU, menu)

        def make_menu_action(value: int):
            def set_new_priority():
                tag_command = get_priority_tag_command(editor.note, value)
                editor.onBridgeCmd(tag_command)
                AppHolder.app.reset()

            return set_new_priority

        for index, item in enumerate(Priority.priorityList):
            act = QAction('(&' + str(index + 1) + ') ' + item.description, submenu,
                          triggered=make_menu_action(index))

            submenu.addAction(act)

        menu.addMenu(submenu)

    @staticmethod
    def onShowQA():
        reviewer = AppHolder.app.reviewer
        if not reviewer.card:
            return
        note = reviewer.card._note

        customPriority = None
        for p in Priority.priorityList:
            if not p.tagName:
                continue

            if note.has_tag(p.tagName):
                customPriority = p.description

        if customPriority:
            PriorityCardUiHandler.showNewPriority(customPriority)
