# -*- coding: utf-8 -*-
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData
from PyQt5.QtWidgets import *

from .core import Label, Feedback


class StandardMenuOption:

    def __init__(self, name: str, fn):
        self.name = name
        self.fn = fn


class AwBrowserMenu:
    """
        Manages context menu, considering whether options should enabled and actions
    """

    infoList = tuple()
    _fields = []
    _selectionHandler = None
    _lastAssignedField = None

    def __init__(self, defaultOptions: List[StandardMenuOption]):
        self._web = None
        self.generationOptions = defaultOptions

    def setCurrentWeb(self, webReference: QWebEngineView):
        self._web = webReference

    def _makeMenuAction(self, field, value, isLink):
        """
            Creates correct operations for the context menu selection.
            Only with lambda, it would repeat only the last element
        """

        def _processMenuSelection():
            self._lastAssignedField = field
            self._selectionHandler(field, value, isLink)

        return _processMenuSelection

    def contextMenuEvent(self, evt):
        """
            Handles the context menu in the web view.
            Shows and handle options (from field list), only if in edit mode.
        """

        if not (self._fields and self._selectionHandler):
            Feedback.log("No fields assigned" if not self._fields else "No selectionHandler assigned")
            return self.createInfoMenu(evt)

        isLink = False
        value = None
        if self._web.selectedText():
            isLink = False
            value = self._web.selectedText()
        else:
            if (self._web.page().contextMenuData().mediaType() == QWebEngineContextMenuData.MediaTypeImage
                    and self._web.page().contextMenuData().mediaUrl()):
                isLink = True
                value = self._web.page().contextMenuData().mediaUrl()
                Feedback.log('Link: ' + value.toString())
                Feedback.log('toLocal: ' + value.toLocalFile())

                if not self._checkSuffix(value):
                    return

        if not value:
            Feedback.log('No value')
            return self.createInfoMenu(evt)

        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if self._assignToLastField(value, isLink):
                return

        self.createCtxMenu(value, isLink, evt)

    def _checkSuffix(self, value):
        if value and not value.toString().endswith(("jpg", "jpeg", "png", "gif")):
            msgLink = value.toString()
            if len(value.toString()) < 80:
                msgLink = msgLink[:50] + '...' + msgLink[50:]
            answ = QMessageBox.question(self._web, 'Anki support',
                                        """This link may not be accepted by Anki: \n\n "%s" \n
                        Usually the suffix should be one of 
                        (jpg, jpeg, png, gif).
                        Try it anyway? """ % msgLink, QMessageBox.Yes | QMessageBox.No)

            if answ != QMessageBox.Yes:
                return False

        return True

    def createCtxMenu(self, value, isLink, evt):
        """ Creates and configures the menu itself """

        m = QMenu(self._web)
        m.addAction(QAction('Copy', m,
                            triggered=lambda: self._copy(value)))
        if isLink:
            Feedback.log('isLink!')
            for op in self.generationOptions:
                m.addAction(QAction(op.name, m, triggered=lambda: op.fn(value)))
            m.addSeparator()

        labelAct = QAction(Label.BROWSER_ASSIGN_TO, m)
        labelAct.setDisabled(True)
        m.addAction(labelAct)
        m.setTitle(Label.BROWSER_ASSIGN_TO)
        for index, label in self._fields.items():
            act = QAction(label, m,
                          triggered=self._makeMenuAction(index, value, isLink))
            m.addAction(act)

        action = m.exec_(self._web.mapToGlobal(evt.pos()))

    def createInfoMenu(self, evt):
        """ Creates and configures a menu with only some information """

        m = QMenu(self._web)
        linkUrl = self._web.page().contextMenuData().linkUrl()
        if linkUrl and len(self.generationOptions) > 0:
            for op in self.generationOptions:
                m.addAction(QAction(op.name, m, triggered=lambda: op.fn(linkUrl)))
            m.addSeparator()

        for item in self.infoList:
            act = QAction(item)
            act.setEnabled(False)
            m.addAction(act)


        action = m.exec_(self._web.mapToGlobal(evt.pos()))

    def _copy(self, value):
        if not value:
            return
        clip = QApplication.clipboard()
        clip.setText(value if isinstance(value, str) else value.toString())

    def _assignToLastField(self, value, isLink) -> bool:
        """Tries to set the new value to the same field used before, if set..."""

        if self._lastAssignedField:
            if self._lastAssignedField in self._fields:
                self._selectionHandler(self._lastAssignedField, value, isLink)
                return True
            else:
                self._lastAssignedField = None
        return False
