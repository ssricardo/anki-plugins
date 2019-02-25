# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of anki-markdown-formatter addon
# @author ricardo saturnino
# ------------------------------------------------

from .config import ConfigKey, ConfigService
from .core import Feedback, AppHolder, Style
from .converter import Converter

import anki
import os

from aqt.editor import Editor
from aqt.reviewer import Reviewer
from aqt.qt import QAction
from PyQt5.QtWidgets import QMenu, QAction
from aqt.utils import showInfo, tooltip, showWarning
from anki.hooks import addHook

# Holds references so GC does kill them
controllerInstance = None

CWD = os.path.dirname(os.path.realpath(__file__))
ICON_FILE = 'icons/markdown-3.png'

# -------------------------- WEB --------------------------------

EDITOR_STYLES = """
        var prStyle = `<style type="text/css">
            pre.amd {    
                border-left: 3px solid #050766;
                margin: 0px;
            }

            .amd_toggler {
                background-color: red;
            }

            .amd_enabled {
                background-color: green;
            }

            .amd_edit_notice {
                float: right;
                color: orange;
            }
            </style>`;

        $(prStyle).appendTo('#fields');
        """

# Prevent default Enter behavior if as Markdown enabled
EDITOR_SCRIPTS = """
        function handleMdKey(evt) {
            if (evt.keyCode === 13 && ! evt.shiftKey) {

                if (currentField) {
                    console.log('currentField');
                    document.execCommand("insertHTML", false, "\\n\\n");
                }
                return false;
            }
        }

        $('.field').wrap('<pre class=\"amd\"></pre>');
        $('.field').keypress(handleMdKey);
        """

EDITOR_MD_NOTICE = """<div class=\"amd_edit_notice\" title=\"This addon tries to prevent Anki from formatting as HTML\">Markdown ON</div>"""

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
    
    from aqt import mw  

    Feedback.log('Setting anki-markdown controller')
    Feedback.showInfo = _ankiShowInfo
    Feedback.showError = _ankiShowError
    
    AppHolder.app = mw
    ConfigService._f = _ankiConfigRead

    controllerInstance = Controller()
    controllerInstance.setupBindings()


class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    _converter = Converter()
    _showButton = None
    _shortcut = None

    _trimConfig = None
    _replaceSpaceConfig = None
    _editAsMarkdownEnabled = False

    def __init__(self):
        self._showButton = ConfigService.read(ConfigKey.SHOW_MARKDOWN_BUTTON, bool)
        self._shortcut = ConfigService.read(ConfigKey.SHORTCUT, str)
        self._trimConfig = ConfigService.read(ConfigKey.TRIM_LINES, bool)
        self._replaceSpaceConfig = ConfigService.read(ConfigKey.REPLACE_SPACES, bool)

    # ------------------- Hooks / entry points -------------------------

    def setupBindings(self):
        
        # Review
        addHook("prepareQA", self.processField)

        # Editing
        addHook("setupEditorButtons", self.setupButtons)
        addHook("setupEditorShortcuts", self.setupShortcuts)
        addHook("loadNote", self.onLoadNote)        
        addHook('EditorWebView.contextMenuEvent', self._showCustomMenu)

        Editor.setupWeb = self._wrapEditorSetupWeb(Editor.setupWeb)


    def _wrapEditorSetupWeb(self, f):
        def wrapper(instance):
            f(instance)
            self.setEditAsMarkdownEnabled(self._editAsMarkdownEnabled)  # initialization

        return wrapper


    # --------------------------- Editing ----------------------------

    def toggleMarkdown(self, editor = None):
        print("toggleMarkdown")
        self.setEditAsMarkdownEnabled(not self._editAsMarkdownEnabled)
        self._editorReference.loadNoteKeepingFocus()

    def _showCustomMenu(self, webview, menu):
        submenu = QMenu('&Markdown', menu)

        act1 = QAction('(&1) Convert to HTML', submenu,
            triggered=lambda: self._convertToHTML())
        submenu.addAction(act1)

        act2 = QAction('(&2) Convert to MD', submenu,
            triggered=lambda: self._clearHTML())
        submenu.addAction(act2)

        menu.addMenu(submenu)


    def onLoadNote(self, editor):
        note = editor.note

        mdCssClass = 'amd_enabled' if self._editAsMarkdownEnabled else 'amd_toggler'
        self._editorReference.web.eval("$('#bt_tg_md').addClass('{}');".format(mdCssClass))
        self._editorReference.web.eval("console.log($('#bt_tg_md').class());")

        if self._editAsMarkdownEnabled:
            editor.web.eval(EDITOR_STYLES)
            editor.web.eval("$('#fields').prepend('{}');".format(EDITOR_MD_NOTICE))
            editor.web.eval(EDITOR_SCRIPTS)


    def setupButtons(self, buttons, editor):        
        """Add buttons to editor"""        

        if not self._showButton:
            return buttons

        self._editorReference = editor
        editor._links['apply-markdown'] = self._wrapAsMarkdown
        editor._links['toggle-md'] = self.toggleMarkdown

        return buttons + [editor._addButton(
            CWD + '/' + ICON_FILE,
            "apply-markdown",  "Apply Markdown ({})".format(self._shortcut)),
            editor._addButton(
            None,
            "toggle-md",  "Edit as Markdown?", "Markdown", toggleable = True, id='bt_tg_md')]


    def setupShortcuts(self, scuts:list, editor):
        scuts.append((self._shortcut, self._wrapAsMarkdown))
        

    def _clearHTML(self, editor = None):
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
        self._editorReference.web.eval('editAsMarkdownEnabled = {};'.format(str(value).lower())) # TODO precisa?


    def _wrapAsMarkdown(self, editor = None):
        if not editor:
            if not self._editorReference:
                return
            editor = self._editorReference

        editor.web.eval("wrap('<amd>', '</amd>');")
        Feedback.showInfo('Anki Markdown :: Added successfully')


    def _isEditing(self):
        'Checks anki current state. Whether is editing or not'

        return True if (self._ankiMw and self._editorReference) else False

    # ------------------------------ Review ------------------------------------------

    def processField(self, inpt, card, phase, *args):
        # inpt = inpt
        print("processField: " + inpt)
        res = self._converter.convertAmdAreasToMD(inpt)
        print(res)
        res = '<span class="amd">{}</span>'.format(res)        
        return Style.MARKDOWN + os.linesep + res


# ---------------------------------- Events listeners ---------------------------------
