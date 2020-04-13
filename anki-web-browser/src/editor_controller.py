# -*- coding: utf-8 -*-
# Interface between Anki's Editor and this addon's components

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------

# ---------------------------------- Editor Control -----------------------------------
# ---------------------------------- ================ ---------------------------------

import json

from PyQt5.QtWidgets import QWidget
from anki.hooks import addHook
from aqt.editor import Editor

from .base_controller import BaseController
from .config import service as cfg
from .core import Feedback
from .no_selection import NoSelectionResult


class EditorController(BaseController):
    _editorReference = None
    _lastProvider = None

    def __init__(self, ankiMw):
        super(EditorController, self).__init__(ankiMw)

        self.setupBindings()

# ------------------------ Anki interface ------------------

    def setupBindings(self):
        addHook('EditorWebView.contextMenuEvent', self.onEditorHandle)
        addHook("setupEditorShortcuts", self.setupShortcuts)
        addHook("loadNote", self.newLoadNote)

    def newLoadNote(self, editor: Editor):
        """ Listens when the current showed card is changed.
            Send msg to browser to cleanup its state"""

        Feedback.log('loadNote')

        self._editorReference = editor
        if not self.browser:
            return

        if self._currentNote == self._editorReference.note:
            return

        self._currentNote = self._editorReference.note
        self.browser.clearContext()
        if not cfg.getConfig().keepBrowserOpened:
            self.browser.close()


    def onEditorHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the editor;
            Also holds a reference to the editor
        """

        self._editorReference = webView.editor
        self.createEditorMenu(menu, self.handleProviderSelection)


    def setupShortcuts(self, scuts:list, editor):
        self._editorReference = editor
        scuts.append((cfg.getConfig().menuShortcut, self._showBrowserMenu))
        scuts.append((cfg.getConfig().repeatShortcut, self._repeatProviderOrShowMenu))

# ------------------------ Addon operation -------------------------

    def _showBrowserMenu(self, parent=None):
        if not parent:
            parent = self._editorReference
        if not isinstance(parent, QWidget):
            if parent.web:
                parent = parent.web
            else:
                parent = self._ankiMw.web

        self.createEditorMenu(parent, self.handleProviderSelection)

    def _repeatProviderOrShowMenu(self):
        webView = self._editorReference.web
        if not self._lastProvider:
            return self.createEditorMenu(webView, self.handleProviderSelection)

        super()._repeatProviderOrShowMenu(webView)

    
    def createEditorMenu(self, parent, menuFn):
        """ Deletegate the menu creation and work related to providers """

        return self._providerSelection.showCustomMenu(parent, menuFn)

    def handleProviderSelection(self, result):
        if not self._editorReference:
            raise Exception('Illegal state found. It was not possible to recover the reference to Anki editor')
        webview = self._editorReference.web
        query = self._getQueryValue(webview)
        self._lastProvider = result
        if not query:
            return
        Feedback.log('Query: %s' % query)
        self._currentNote = self._editorReference.note
        self.openInBrowser(query)

    def _getQueryValue(self, webview):
        if webview.hasSelection():
            return self._filterQueryValue(webview.selectedText())

        if self._noSelectionHandler.isRepeatOption():
            noSelectionResult = self._noSelectionHandler.getValue()
            if noSelectionResult.resultType == NoSelectionResult.USE_FIELD:
                self._editorReference.currentField = noSelectionResult.value
                if noSelectionResult.value < len(self._currentNote.fields):
                    Feedback.log('USE_FIELD {}: {}'.format(noSelectionResult.value, self._currentNote.fields[noSelectionResult.value]))
                    return self._filterQueryValue(self._currentNote.fields[noSelectionResult.value])

        self.browser.setSelectionHandler(self.handleSelection)
        note = webview.editor.note
        fieldList = note.model()['flds']
        fieldsNames = {ind: val for ind, val in enumerate(map(lambda i: i['name'], fieldList))}
        self._noSelectionHandler.setFields(fieldsNames)
        self._noSelectionHandler.handle(self.handleNoSelectionResult)

        return None

    def handleNoSelectionResult(self, resultValue: NoSelectionResult):
        if not resultValue or \
                resultValue.resultType in (NoSelectionResult.NO_RESULT, NoSelectionResult.SELECTION_NEEDED):
            Feedback.showInfo('No value selected')
            return
        value = resultValue.value
        if resultValue.resultType == NoSelectionResult.USE_FIELD:
            self._editorReference.currentField = resultValue.value    # fieldIndex
            value = self._currentNote.fields[resultValue.value]
            value = self._filterQueryValue(value)
            Feedback.log('USE_FIELD {}: {}'.format(resultValue.value, value))

        return self.openInBrowser(value)

# ---------------------------------- --------------- ---------------------------------
    def beforeOpenBrowser(self):
        self.browser.setSelectionHandler(self.handleSelection)
        note = self._currentNote
        fieldList = note.model()['flds']
        fieldsNames = {ind: val for ind, val in enumerate(map(lambda i: i['name'], fieldList))}
        self.browser.infoList = ['No action available', 'Required: Text selected or link to image']
        self.browser.setFields(fieldsNames)

    def handleSelection(self, fieldIndex, value, isUrl=False):
        """
            Callback from the web browser. 
            Invoked when there is a selection coming from the browser. It needs to be delivered to a given field
        """

        if self._editorReference and self._currentNote != self._editorReference.note:
            Feedback.showWarn("""Inconsistent state found. 
            The current note is not the same as the Web Browser reference. 
            Try closing and re-opening the browser""")
            return

        self._editorReference.currentField = fieldIndex

        if isUrl:
            self.handleUrlSelection(fieldIndex, value)
        else:
            self.handleTextSelection(fieldIndex, value)

    def handleUrlSelection(self, fieldIndex, value):
        """
        Imports an image from the link 'value' to the collection. 
        Adds this new img tag to the given field in the current note"""

        url = value.toString() if value else ''
        Feedback.log("Selected from browser: {} || ".format(url))

        imgReference = self._editorReference.urlToLink(url)        

        if (not imgReference) or not imgReference.startswith('<img'):
            Feedback.showWarn('URL invalid! Only URLs with references to image files are supported (ex: http://images.com/any.jpg,  any.png)')
            return

        Feedback.log('handleUrlSelection.imgReference: ' + imgReference)

        self._editorReference.web.eval("focusField(%d);" % fieldIndex)
        self._editorReference.web.eval("setFormat('inserthtml', %s);" % json.dumps(imgReference))

    def handleTextSelection(self, fieldIndex, value):
        """Adds the selected value to the given field of the current note"""

        newValue = self._currentNote.fields[fieldIndex] + '\n ' + value
        self._currentNote.fields[fieldIndex] = newValue
        self._editorReference.setNote(self._currentNote)
