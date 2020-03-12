# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of anki-markdown-formatter addon
# @author ricardo saturnino
# ------------------------------------------------

from .config import ConfigKey, ConfigService
from .core import Feedback, AppHolder, Style
from .converter import Converter
from .batch import BatchService
from .field_ctrl import NoteFieldControler

import anki
import os
import json

from aqt.editor import Editor, EditorWebView
from aqt.reviewer import Reviewer
from aqt.qt import *
from aqt import mw
from PyQt5.QtWidgets import QMenu, QAction, QApplication
from aqt.utils import showInfo, tooltip, showWarning
from anki.hooks import addHook
from aqt import gui_hooks


# Holds references so GC does kill them
controllerInstance = None

CWD = os.path.dirname(os.path.realpath(__file__))
ICON_FILE = 'icons/markdown-3.png'

# -------------------------- WEB --------------------------------

EDITOR_STYLES = """
        var prStyle = `{}`;

        $(prStyle).appendTo('body');
        """.format(Style.MARKDOWN)

EDITOR_STYLE_APPENDER = """
    <style type="text/css">
        var prStyle = `{}`;

        $(prStyle).appendTo('body');
    </style>
        """

# ---------------------------- Injected functions -------------------
@staticmethod
def _ankiShowInfo(*args):
    tooltip(args)

@staticmethod
def _ankiShowError(*args):
    showWarning(str(args))

def _ankiConfigRead(key):
    return AppHolder.app.addonManager.getConfig(__name__)[key]

# ------------------------ Init ---------------------------------

def run():
    global controllerInstance

    Feedback.log('Setting anki-markdown controller')
    Feedback.showInfo = _ankiShowInfo
    Feedback.showError = _ankiShowError

    AppHolder.app = mw
    ConfigService._f = _ankiConfigRead

    controllerInstance = Controller()
    controllerInstance.setupBindings()

    # noteFieldCtrl = NoteFieldControler(controllerInstance._converter)
    # noteFieldCtrl.setup()


class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    JS_LOCATION = CWD + '/a-md.js'
    CSS_LOCATION = CWD + '/a-md.css'

    _converter = Converter()
    _batchService = BatchService(_converter)
    _showButton = None
    _shortcutMenu = None
    _shortcutButton = None
    _editAsMarkdownEnabled = False
    _jsContent = None
    _cssContent = None

    def __init__(self):
        self._showButton = ConfigService.read(ConfigKey.SHOW_MARKDOWN_BUTTON, bool)
        self._shortcutMenu = ConfigService.read(ConfigKey.SHORTCUT, str)
        self._shortcutButton = ConfigService.read(ConfigKey.SHORTCUT_EDIT, str)
        self._enablePreview = ConfigService.read(ConfigKey.ENABLE_PREVIEW, bool)

        try:
            with open(Controller.JS_LOCATION, 'r') as f:
                self._jsContent = f.read()

            with open(Controller.CSS_LOCATION, 'r') as fCss:
                self._cssContent = fCss.read()

        except Exception as e:
            print(e)
            Feedback.showError('An error occoured on loading Markdown Preview. You may need to restart Anki.')


    # ------------------- Hooks / entry points -------------------------

    def setupBindings(self):
        """
            Register the entry points / interface with Anki
        """
        
        # Review

        gui_hooks.card_will_show.append(self.processField)
        Feedback.log('Review Hook set')

        # Editing
        addHook("setupEditorButtons", self.setupButtons)
        addHook("setupEditorShortcuts", self.setupShortcuts)
        addHook("loadNote", self.onLoadNote)
        addHook('EditorWebView.contextMenuEvent', self._setupContextMenu)
        addHook('browser.setupMenus', self._setupBrowserMenu)
        addHook('editTimer', lambda n: self._updatePreview())

        Editor.setupWeb = self._wrapEditorSetupWeb(Editor.setupWeb)
        try:
            EditorWebView._onPaste = self._wrapOnPaste(EditorWebView._onPaste)
        except:
            Feedback.log('Markdown: Handling "Paste" is disabled duo to an error')
        

    def _wrapEditorSetupWeb(self, fn):
        def wrapper(editor):
            fn(editor)

            # editor.web.eval(EDITOR_STYLES)

            print("""
        var prStyle = `{}`;

        $(prStyle).appendTo('body');
        """.format(self._cssContent))

            editor.web.eval();

            editor.web.eval("console.log('After styles');")

            editor.web.eval("""
                %s
            """ % self._jsContent)

            if self._enablePreview:
                editor.web.eval('setPreviewUp()')

        return wrapper


    def _wrapOnPaste(self, fn):
        ref = self
        
        def _onPaste(self, mode):
            extended = self.editor.mw.app.queryKeyboardModifiers() & Qt.ShiftModifier
            mime = self.editor.mw.app.clipboard().mimeData(mode=mode)

            if ref._editAsMarkdownEnabled:
                if not (mime.html() and mime.html().startswith("<!--anki-->")):
                    cur = self.editor.currentField                    
                    self.eval("pasteAmdContent(%s);" % json.dumps(mime.text()))

                    return

            html, internal = self._processMime(mime)

            if not html:
                return
            self.editor.doPaste(html, internal, extended)

        return _onPaste


    # --------------------------- Editing ----------------------------

    def toggleMarkdown(self, editor = None):
        self.setEditAsMarkdownEnabled(not self._editAsMarkdownEnabled)
        self._editorReference.loadNoteKeepingFocus()


    def _setupContextMenu(self, webview, menu):
        submenu = self._showCustomMenu(menu)
        menu.addMenu(submenu)


    def _showCustomMenu(self, parent = None):
        if not parent:
            parent = self._editorReference.web

        submenu = QMenu('&Markdown', parent)

        act1 = QAction('(&1) Convert to HTML', submenu,
            triggered=lambda: self._convertToHTML())
        submenu.addAction(act1)

        act2 = QAction('(&2) Convert to MD', submenu,
            triggered=lambda: self._clearHTML())
        submenu.addAction(act2)

        act3 = QAction('(&3) Mark as Markdown block', submenu,
            triggered=lambda: self._wrapAsMarkdown())
        submenu.addAction(act3)

        if not isinstance(parent, QMenu):
            submenu.popup(parent.mapToGlobal( parent.pos() ))
        return submenu


    def onLoadNote(self, editor):
        note = editor.note

        if self._editAsMarkdownEnabled:

            # Prevent default Enter behavior if as Markdown enabled
            self.setEditAsMarkdownEnabled(self._editAsMarkdownEnabled)  # initialization
            editor.web.eval("showMarkDownNotice();")
            editor.web.eval("handleNoteAsMD();")

        self._updatePreview()


    def setupButtons(self, buttons, editor):
        """Add buttons to editor"""        

        if not self._showButton:
            return buttons

        self._editorReference = editor
        editor._links['amd-menu'] = self.toggleMarkdown

        return buttons + [
            editor._addButton(
            CWD + '/' + ICON_FILE,
            "amd-menu",  "Edit as Markdown? ({})".format(self._shortcutButton), 
            toggleable = True, id='bt_tg_md')]


    def setupShortcuts(self, scuts:list, editor):
        scuts.append((self._shortcutButton, self.toggleMarkdown))
        scuts.append((self._shortcutMenu, self._showCustomMenu))


    def _clearHTML(self, editor = None):
        """
            Convert to Text (MD)
        """
        
        Feedback.log('_convertToMD')

        cur = self._editorReference.currentField
        note = self._editorReference.note
        newValue = self._converter.getTextFromHtml(note.fields[cur])
        note.fields[cur] = newValue
        self._editorReference.setNote(note)


    def _convertToHTML(self, editor = None):
        Feedback.log('_convertToHTML')

        cur = self._editorReference.currentField
        note = self._editorReference.note
        newValue = self._converter.convertMarkdown(note.fields[cur])
        note.fields[cur] = newValue
        self._editorReference.setNote(note)
   

    def setEditAsMarkdownEnabled(self, value: bool):
        self._editAsMarkdownEnabled = value
        self._editorReference.web.eval('editAsMarkdownEnabled = {};'.format(str(value).lower())) # check is it needed?


    def _wrapAsMarkdown(self, editor = None):
        if not editor:
            if not self._editorReference:
                return
            editor = self._editorReference

        editor.web.eval("wrap('<amd>', '</amd>');")
        Feedback.showInfo('Anki Markdown :: Added successfully')


    def _updatePreview(self):
        if not (self._editorReference and self._editorReference.note):
            return
        note = self._editorReference.note       
        self._editorReference.web.eval('cleanPreview();')
        for fld, val in list(note.items()):
            self._editorReference.web.eval('setFieldPreview("%s", `%s`);' % (fld, 
                self._converter.convertMarkdown(val)))

    def _isEditing(self):
        'Checks anki current state. Whether is editing or not'

        return True if (self._editorReference) else False

    # ------------------------------ Review ------------------------------------------

    def processField(self, inpt:str, card, kind: str) -> str:
        Feedback.log('processField')
        if self._converter.isAmdAreaPresent(inpt):
            res = self._converter.convertAmdAreasToMD(inpt, isTypeMode=True)

            return Style.MARKDOWN + os.linesep + res            
        return inpt


    # --------------------------------------- Browser ------------------------------------
    def _setupBrowserMenu(self, browser):
        submenu = QMenu('&Markdown Addon', browser.form.menu_Notes)

        # submenu = QMenu()
        act1 = QAction('(&1) Convert to HTML', submenu,
            triggered=lambda: self._batchConvertHTML(browser))
        submenu.addAction(act1)

        act2 = QAction('(&2) Convert to MD', submenu,
            triggered=lambda: self._batchConvertMD(browser))
        submenu.addAction(act2)

        browser.form.menu_Notes.addMenu(submenu)
        

    def _batchConvertHTML(self, browser):
        selectedItens = browser.selectedNotes()
        print('_batchConvertHTML - selected: ' + str(selectedItens))
        self._batchService.convertNotesToHTML(selectedItens)


    def _batchConvertMD(self, browser):
        selectedItens = browser.selectedNotes()
        print('_batchConvertMD - selected: ' + str(selectedItens))
        self._batchService.convertNotesToMD(selectedItens)


# ---------------------------------- Events listeners ---------------------------------
